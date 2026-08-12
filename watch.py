#!/usr/bin/env python3
"""
WATCH MODE — atualização automática e incremental do site
================================================================================
Roda em segundo plano observando:
  - artigos/artigos_pt.csv   -> ao aparecer artigo novo: traduz para EN/ES
                                 automaticamente, publica nos 3 idiomas e
                                 sincroniza sitemap. Ao editar um artigo
                                 existente: só aquela página é regenerada.
  - artigos/artigos_en.csv,
    artigos/artigos_es.csv   -> mesma lógica, mas sem tradução automática
                                 (edição manual é respeitada como está).
  - templates/*.html          -> qualquer template alterado regenera as
                                 páginas que o usam, em TODOS os idiomas
                                 (o conteúdo dos artigos é preservado, só
                                 o layout/head é recriado).
  - config.json               -> muda algo global (cores, nome do site,
                                 idiomas ativos etc): regera tudo.

Também sobe um servidor HTTP local em paralelo servindo a pasta docs/, então
basta deixar isso rodando e ir editando os arquivos — o navegador só precisa
ser atualizado (F5) para ver o resultado.

USO:
    pip install watchdog
    python watch.py                 # observa + serve em http://localhost:8000
    python watch.py --sem-servidor  # só observa, sem subir servidor
    python watch.py --porta 5500    # muda a porta do servidor local
================================================================================
"""

import argparse
import functools
import http.server
import socketserver
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("❌ Falta instalar a dependência do watch mode. Rode:")
    print("   pip install watchdog")
    sys.exit(1)

from gerador import Gerador


def log(msg):
    hora = datetime.now().strftime("%H:%M:%S")
    print(f"[{hora}] {msg}")


# ================================================================
# ===== LÓGICA DE SINCRONIZAÇÃO INCREMENTAL =====================
# ================================================================

def artigo_ja_publicado(g: Gerador, artigo: dict, idioma: str) -> bool:
    """Verifica no disco (não recalculando slug) se o artigo já tem página."""
    slug = (artigo.get('slug') or '').strip()
    if not slug:
        return False
    categoria = artigo.get('categoria', 'geral')
    cat_traduzida = g.get_categoria_traduzida(categoria, idioma)
    caminho = g.docs / idioma / cat_traduzida / slug / "index.html"
    return caminho.exists()


def criar_traducao_automatica(g: Gerador, artigo_pt: dict):
    """Quando um artigo novo aparece no CSV de PT, cria a versão traduzida
    (com slug próprio, gerado uma única vez) em cada idioma ativo != pt."""
    titulo_pt = artigo_pt.get('artigo', '').strip()
    if not titulo_pt:
        return

    for idioma in g.idiomas_ativos:
        if idioma == 'pt':
            continue

        artigos_lang = g.ler_csv(idioma)
        titulo_trad = g.traduzir_titulo(titulo_pt, idioma) or titulo_pt
        slug_trad = g.criar_slug(titulo_trad)

        # já existe uma tradução com esse slug? não duplica.
        if any((a.get('slug') or '').strip() == slug_trad for a in artigos_lang):
            continue

        categoria_pt = artigo_pt.get('categoria', 'geral')
        categoria_trad = g.get_categoria_traduzida(categoria_pt, idioma)

        novo = {
            'artigo': titulo_trad,
            'slug': slug_trad,
            'links_afiliados': artigo_pt.get('links_afiliados', '#'),
            'status': 'publicado',
            'categoria': categoria_trad,
            'palavras_chave': g.traduzir_titulo(artigo_pt.get('palavras_chave', ''), idioma) or '',
            'descricao': g.traduzir_titulo(artigo_pt.get('descricao', ''), idioma) or '',
            'tipo': artigo_pt.get('tipo', 'review'),
            'data_publicacao': datetime.now().strftime("%Y-%m-%d"),
            'autor': g.config.get('autor', 'Autor'),
            'links_internos': '',
            'links_externos': '',
        }
        artigos_lang.append(novo)
        g.salvar_csv(artigos_lang, idioma)
        log(f"   🌐 Traduzido para {idioma.upper()}: {titulo_trad[:50]}")
        g.criar_artigo(novo, forcar=True, revisar=False, idioma=idioma)


def sincronizar_idioma(g: Gerador, idioma: str, auto_traduzir: bool):
    """Sincroniza um único idioma a partir do CSV dele: cria o que for novo,
    regenera (preservando conteúdo) o que foi editado, e atualiza
    index/categorias/páginas estáticas desse idioma."""
    artigos = g.ler_csv(idioma)
    publicados = [a for a in artigos if a.get('status', '').lower() == 'publicado']

    if not publicados:
        return

    algo_mudou = False
    for a in publicados:
        if artigo_ja_publicado(g, a, idioma):
            # já existe -> regenera preservando o conteúdo (marcadores),
            # útil quando o título/categoria/descrição foi editado no CSV
            g.criar_artigo(a, forcar=True, revisar=False, idioma=idioma)
        else:
            # artigo novo
            log(f"   🆕 Novo artigo em {idioma.upper()}: {a.get('artigo', '')[:50]}")
            g.criar_artigo(a, forcar=True, revisar=True, idioma=idioma)
            if auto_traduzir and idioma == 'pt':
                criar_traducao_automatica(g, a)
        algo_mudou = True

    if algo_mudou:
        g.criar_todas_categorias(idioma=idioma)
        g.criar_index(idioma=idioma)
        g.criar_paginas_estaticas(idioma=idioma)


def sincronizar_apos_mudanca(g: Gerador, csvs_mudaram: set, templates_mudaram: bool, config_mudou: bool):
    if config_mudou:
        log("⚙️  config.json mudou -> recarregando config e regenerando TUDO")
        g.config = g.carregar_config()
        templates_mudaram = True
        csvs_mudaram = set(g.idiomas_ativos)

    if templates_mudaram:
        log("🎨 Template mudou -> regenerando páginas em todos os idiomas")
        for idioma in g.idiomas_ativos:
            sincronizar_idioma(g, idioma, auto_traduzir=False)
    else:
        for idioma in sorted(csvs_mudaram):
            if idioma not in g.idiomas_ativos:
                continue
            log(f"📄 artigos_{idioma}.csv mudou -> sincronizando {idioma.upper()}")
            sincronizar_idioma(g, idioma, auto_traduzir=(idioma == 'pt'))

    g.criar_sitemap()
    g.criar_index_raiz()
    log("✅ Site sincronizado.")


# ================================================================
# ===== OBSERVADOR DE ARQUIVOS (DEBOUNCED) =======================
# ================================================================

class Handler(FileSystemEventHandler):
    def __init__(self, gerador: Gerador):
        self.g = gerador
        self._lock = threading.Lock()
        self._timer = None
        self._csvs_pendentes = set()
        self._templates_pendente = False
        self._config_pendente = False

    def _agendar_processamento(self):
        if self._timer:
            self._timer.cancel()
        self._timer = threading.Timer(1.0, self._processar)
        self._timer.daemon = True
        self._timer.start()

    def _processar(self):
        with self._lock:
            csvs = self._csvs_pendentes
            templates = self._templates_pendente
            config = self._config_pendente
            self._csvs_pendentes = set()
            self._templates_pendente = False
            self._config_pendente = False

        if not csvs and not templates and not config:
            return

        try:
            sincronizar_apos_mudanca(self.g, csvs, templates, config)
        except Exception as e:
            log(f"❌ Erro ao sincronizar: {e}")

    def _marcar(self, path: str):
        p = Path(path)

        if p.name == "config.json" and p.parent == self.g.base:
            with self._lock:
                self._config_pendente = True
            self._agendar_processamento()
            return

        if p.suffix == ".csv" and p.parent.name == "artigos":
            # artigos_pt.csv -> pt / artigos_en.csv -> en / etc.
            stem = p.stem  # artigos_pt
            idioma = stem.replace("artigos_", "")
            with self._lock:
                self._csvs_pendentes.add(idioma)
            self._agendar_processamento()
            return

        if self.g.templates in p.parents and p.suffix == ".html":
            with self._lock:
                self._templates_pendente = True
            self._agendar_processamento()
            return

    def on_modified(self, event):
        if not event.is_directory:
            self._marcar(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self._marcar(event.src_path)


# ================================================================
# ===== SERVIDOR LOCAL ===========================================
# ================================================================

def subir_servidor(pasta_docs: Path, porta: int):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(pasta_docs))
    with socketserver.TCPServer(("", porta), handler) as httpd:
        log(f"🌐 Servidor local rodando em http://localhost:{porta}")
        httpd.serve_forever()


# ================================================================
# ===== MAIN ======================================================
# ================================================================

def main():
    parser = argparse.ArgumentParser(description="Watch mode do gerador de blog")
    parser.add_argument("--sem-servidor", action="store_true", help="não sobe o servidor HTTP local")
    parser.add_argument("--porta", type=int, default=8000, help="porta do servidor local (padrão 8000)")
    args = parser.parse_args()

    print("=" * 70)
    print("  👀 WATCH MODE — atualização automática do site")
    print("=" * 70)

    g = Gerador()

    log("🔄 Rodando sincronização inicial completa...")
    sincronizar_apos_mudanca(g, set(g.idiomas_ativos), templates_mudaram=False, config_mudou=False)

    if not args.sem_servidor:
        t = threading.Thread(target=subir_servidor, args=(g.docs, args.porta), daemon=True)
        t.start()

    handler = Handler(g)
    observer = Observer()
    observer.schedule(handler, str(g.base / "artigos"), recursive=False)
    observer.schedule(handler, str(g.templates), recursive=True)
    observer.schedule(handler, str(g.base), recursive=False)  # para pegar config.json

    observer.start()
    log("👀 Observando artigos/, templates/ e config.json — edite à vontade.")
    log("   (Ctrl+C para parar)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        log("🛑 Watch mode encerrado.")
    observer.join()


if __name__ == "__main__":
    main()
