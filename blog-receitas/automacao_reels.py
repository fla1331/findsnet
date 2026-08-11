# ============================================================
# automacao_reels.py - SISTEMA DE AUTOMAÇÃO DE REELS
# ============================================================
# 
# FUNÇÃO: Gerar Reels para artigos já publicados no blog
# 
# COMO USAR:
# 1. Escreve o artigo no CSV
# 2. Roda: python gerador.py (publica o blog)
# 3. Roda: python automacao_reels.py (gera os Reels)
# ============================================================

import os
import re
import csv
import shutil
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from moviepy.editor import ImageClip, concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# ============================================================
# 🔧 CONFIGURAÇÕES
# ============================================================

load_dotenv()

# ===== USANDO OPENROUTER (IGUAL AO GERADOR.PY) =====
IA_API_KEY = os.getenv("OPENROUTER_API_KEY")
IA_URL = "https://openrouter.ai/api/v1/chat/completions"
IA_MODEL = "deepseek/deepseek-chat"  # Ou outro modelo que você usa

PASTA_DOCS = "docs"
PASTA_REELS = "reels_automaticos"
ARQUIVO_CSV = "artigos.csv"

IGNORAR = [
    'index.html', 'sobre.html', 'contato.html', 
    'cookies.html', 'politica-privacidade.html',
    'sitemap.xml', 'robots.txt', 'busca.html'
]

# ============================================================
# 1. FUNÇÃO DE IA (USANDO OPENROUTER - IGUAL AO GERADOR)
# ============================================================

def chamar_ia(prompt, max_tokens=300, temperatura=0.8):
    """Chama a API da OpenRouter (igual ao gerador.py)"""
    if not IA_API_KEY:
        print("   ⚠️ OPENROUTER_API_KEY não configurada!")
        return None
    
    headers = {
        "Authorization": f"Bearer {IA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": IA_MODEL,
        "messages": [
            {"role": "system", "content": "Você é um especialista em marketing digital e criação de conteúdo."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperatura
    }
    
    try:
        response = requests.post(IA_URL, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            print(f"   ⚠️ Erro na IA: {response.status_code}")
            return None
    except Exception as e:
        print(f"   ⚠️ Erro na IA: {e}")
        return None

# ============================================================
# 2. FUNÇÕES AUXILIARES
# ============================================================

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def ler_artigo_html(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        html = f.read()
    match_titulo = re.search(r'<h1[^>]*>(.*?)</h1>', html)
    titulo = match_titulo.group(1).strip() if match_titulo else "Título não encontrado"
    texto = re.sub(r'<[^>]+>', ' ', html)
    texto = re.sub(r'\s+', ' ', texto).strip()[:1000]
    return titulo, texto

def carregar_historico():
    if not os.path.exists(ARQUIVO_CSV):
        return []
    with open(ARQUIVO_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def salvar_historico(artigos):
    if not artigos:
        return
    campos = ['titulo', 'categoria', 'data_publicacao', 'status', 'reels_gerado']
    with open(ARQUIVO_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(artigos)

def encontrar_artigos_na_pasta():
    """Encontra todos os artigos HTML na pasta docs/, em qualquer subpasta"""
    artigos = []
    
    # Verifica se a pasta docs existe
    if not os.path.exists(PASTA_DOCS):
        print(f"⚠️ Pasta '{PASTA_DOCS}' não encontrada!")
        return artigos
    
    for root, dirs, files in os.walk(PASTA_DOCS):
        # Ignora pastas de assets e netlify
        if any(ignorar in root for ignorar in ['assets', 'netlify']):
            continue
            
        for file in files:
            if file.endswith('.html') and file not in IGNORAR:
                caminho = os.path.join(root, file)
                
                # Pega a categoria e o nome do artigo a partir da estrutura
                caminho_relativo = os.path.relpath(caminho, PASTA_DOCS)
                partes = caminho_relativo.split(os.sep)
                
                # Se o arquivo está em uma subpasta (ex: receitas/bolo/index.html)
                if len(partes) >= 2:
                    categoria = partes[0]  # Ex: "receitas"
                    # O nome é o nome da pasta do artigo (ex: "bolo-de-caneca-rapido")
                    # Se o arquivo é "index.html", pegamos o nome da pasta pai
                    if file == "index.html":
                        nome = os.path.basename(root)
                    else:
                        nome = os.path.splitext(file)[0]
                else:
                    # Arquivo na raiz da docs (ex: sobre.html)
                    categoria = "geral"
                    nome = os.path.splitext(file)[0]
                
                # Tenta extrair o título do HTML para exibir
                titulo, _ = ler_artigo_html(caminho)
                
                artigos.append({
                    'caminho': caminho,
                    'categoria': categoria,
                    'nome': nome,
                    'titulo': titulo
                })
    
    # Ordena por título
    artigos.sort(key=lambda x: x['titulo'])
    
    # Debug: mostra quantos artigos encontrou
    if artigos:
        print(f"🔍 Encontrados {len(artigos)} artigos na pasta docs/")
    else:
        print("⚠️ Nenhum artigo encontrado na pasta docs/")
    
    return artigos

def listar_categorias():
    categorias = []
    for item in os.listdir(PASTA_DOCS):
        caminho = os.path.join(PASTA_DOCS, item)
        if os.path.isdir(caminho) and item not in ['assets', 'netlify']:
            categorias.append(item)
    return categorias

# ============================================================
# 3. FUNÇÕES DE CRIAÇÃO DE REELS (COM IA VIA OPENROUTER)
# ============================================================

def criar_roteiro_isca(titulo, texto):
    """Gera roteiro de Reels usando OpenRouter"""
    prompt = f"""
    Crie um roteiro de Reels de 30 segundos que seja uma ISCA para levar o público ao blog.
    Artigo: "{titulo}"
    Resumo: "{texto}"

    Estrutura:
    [GANCHO] (3-5s) - Frase impactante
    [CONTEXTO] (10s) - Apresenta o problema
    [PONTE] (10s) - Gera mistério
    [CTA] (5s) - "Comente QUERO que eu te envio o artigo completo"
    """
    
    resultado = chamar_ia(prompt, max_tokens=300, temperatura=0.8)
    return resultado if resultado else f"""
[GANCHO] Você sabia que {titulo} é mais simples do que parece?
[CONTEXTO] A maioria das pessoas comete erros básicos...
[PONTE] Existe um segredo que poucos conhecem...
[CTA] Comente QUERO que eu te envio o artigo completo!
"""

def criar_post_facebook(titulo, link):
    return f"""🧵 {titulo}

Descubra como transformar isso com dicas práticas:

👉 Leia o artigo completo:
{link}

Comente 'QUERO' que eu te envio as dicas extras! 🚀
"""

def gerar_video_reels(roteiro, titulo, pasta_destino):
    os.makedirs(pasta_destino, exist_ok=True)
    nome_limpo = re.sub(r'[^a-zA-Z0-9 ]', '', titulo)[:40].replace(' ', '_')
    caminho_video = os.path.join(pasta_destino, f"reels_{nome_limpo}.mp4")
    
    blocos = re.split(r'\[GANCHO\]|\[CONTEXTO\]|\[PONTE\]|\[CTA\]', roteiro)
    blocos = [b.strip() for b in blocos if b.strip()]
    
    if len(blocos) < 4:
        blocos = [roteiro]
    
    duracao_por_bloco = max(4, min(10, 30 // len(blocos)))
    clips = []
    
    for bloco in blocos:
        img = Image.new('RGB', (1080, 1920), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 80)
        except:
            font = ImageFont.load_default()
        
        linhas = []
        palavras = bloco.split()
        linha = ""
        for p in palavras:
            if len(linha + p) < 40:
                linha += p + " "
            else:
                linhas.append(linha.strip())
                linha = p + " "
        if linha:
            linhas.append(linha.strip())
        
        y = 800
        for linha in linhas:
            draw.text((100, y), linha, fill=(255, 255, 255), font=font)
            y += 100
        
        img_np = np.array(img)
        clip = ImageClip(img_np).set_duration(duracao_por_bloco)
        clips.append(clip)
    
    video_final = concatenate_videoclips(clips, method="compose")
    video_final.write_videofile(caminho_video, fps=24, verbose=False, logger=None)
    return caminho_video

# ============================================================
# 4. FUNÇÕES DE PROCESSAMENTO
# ============================================================

def processar_artigo(artigo, historico):
    caminho = artigo['caminho']
    categoria = artigo['categoria']
    nome = artigo['nome']
    titulo = artigo.get('titulo', nome)
    
    print(f"\n📄 Processando: {categoria}/{nome}")
    print(f"   📌 Título: {titulo}")
    
    # Usa o título extraído para o roteiro
    if titulo == "Título não encontrado":
        titulo = nome.replace('-', ' ').title()
    
    # Verifica se já existe Reels
    existente = next((h for h in historico if h['titulo'] == titulo), None)
    if existente and existente.get('reels_gerado') == 'sim':
        print("   ⏭️ Reels já gerado para este artigo.")
        return
    
    # Pega o texto do artigo
    _, texto = ler_artigo_html(caminho)
    
    # Gera Reels
    print("   🧠 Gerando roteiro...")
    pasta_destino = os.path.join(PASTA_REELS, categoria, nome)
    os.makedirs(pasta_destino, exist_ok=True)
    
    roteiro = criar_roteiro_isca(titulo, texto)
    with open(os.path.join(pasta_destino, 'roteiro.txt'), 'w', encoding='utf-8') as f:
        f.write(roteiro)
    
    link_blog = f"https://homedecor.brightnest.blog/{categoria}/{nome}"
    post = criar_post_facebook(titulo, link_blog)
    with open(os.path.join(pasta_destino, 'post_facebook.txt'), 'w', encoding='utf-8') as f:
        f.write(post)
    
    print("   🎬 Gerando vídeo...")
    caminho_video = gerar_video_reels(roteiro, titulo, pasta_destino)
    
    # Atualiza histórico
    if existente:
        existente['reels_gerado'] = 'sim'
        existente['status'] = 'publicado'
    else:
        historico.append({
            'titulo': titulo,
            'categoria': categoria,
            'data_publicacao': datetime.now().strftime('%Y-%m-%d'),
            'status': 'publicado',
            'reels_gerado': 'sim'
        })
    
    salvar_historico(historico)
    print(f"   ✅ Reels gerado em: {pasta_destino}")

def deletar_reels(categoria, nome_artigo):
    caminho = os.path.join(PASTA_REELS, categoria, nome_artigo)
    if os.path.exists(caminho):
        shutil.rmtree(caminho)
        print(f"🗑️ Reels deletado: {caminho}")
        return True
    print(f"❌ Reels não encontrado: {caminho}")
    return False

# ============================================================
# 5. MENU PRINCIPAL
# ============================================================

def menu():
    while True:
        limpar_tela()
        print("\n" + "="*60)
        print("🎬 SISTEMA DE AUTOMAÇÃO DE REELS - HOMEDECOR")
        print("="*60)
        print("1. 🔍 Listar artigos e status dos Reels")
        print("2. 🆕 Gerar Reels para um artigo específico")
        print("3. 📦 Gerar Reels para TODOS os artigos de uma categoria")
        print("4. 🚀 Gerar Reels para TODOS os artigos (automático)")
        print("5. 📈 Ver relatório geral")
        print("6. 🗑️ Deletar Reels de um artigo")
        print("7. ❌ Sair")
        print("="*60)
        
        opcao = input("\n👉 Escolha uma opção: ")
        
        if opcao == "1":
            listar_artigos()
        elif opcao == "2":
            gerar_reels_especifico()
        elif opcao == "3":
            gerar_reels_por_categoria()
        elif opcao == "4":
            gerar_reels_todos()
        elif opcao == "5":
            relatorio_geral()
        elif opcao == "6":
            deletar_reels_menu()
        elif opcao == "7":
            print("\n👋 Saindo...")
            break
        else:
            print("\n❌ Opção inválida!")
        
        input("\n⏎ Pressione Enter para continuar...")

# ============================================================
# 6. FUNÇÕES DO MENU
# ============================================================

def listar_artigos():
    historico = carregar_historico()
    if not historico:
        print("\n📭 Nenhum artigo no histórico.")
        return
    
    print("\n📊 ARTIGOS E STATUS DOS REELS:")
    print("-"*60)
    for h in historico:
        reels = h.get('reels_gerado', 'nao')
        icone = "✅" if reels == 'sim' else "❌"
        print(f"   {icone} {h['titulo'][:45]} | {h.get('status', 'desconhecido')}")

def gerar_reels_especifico():
    artigos = encontrar_artigos_na_pasta()
    if not artigos:
        print("\n❌ Nenhum artigo encontrado.")
        return
    
    print("\n📄 ESCOLHA UM ARTIGO:")
    for i, a in enumerate(artigos, 1):
        titulo = a.get('titulo', a['nome'])
        print(f"   {i}. {titulo[:50]} ({a['categoria']})")
    
    try:
        escolha = int(input("\n👉 Número do artigo: ")) - 1
        artigo = artigos[escolha]
    except:
        print("❌ Opção inválida!")
        return
    
    historico = carregar_historico()
    processar_artigo(artigo, historico)

def gerar_reels_por_categoria():
    categorias = listar_categorias()
    if not categorias:
        print("\n❌ Nenhuma categoria encontrada.")
        return
    
    print("\n📂 ESCOLHA UMA CATEGORIA:")
    for i, cat in enumerate(categorias, 1):
        print(f"   {i}. {cat}")
    
    try:
        escolha = int(input("\n👉 Número da categoria: ")) - 1
        categoria = categorias[escolha]
    except:
        print("❌ Opção inválida!")
        return
    
    artigos = [a for a in encontrar_artigos_na_pasta() if a['categoria'] == categoria]
    if not artigos:
        print(f"❌ Nenhum artigo em {categoria}")
        return
    
    print(f"\n📄 Processando {len(artigos)} artigos de {categoria}...")
    historico = carregar_historico()
    for artigo in artigos:
        processar_artigo(artigo, historico)

def gerar_reels_todos():
    artigos = encontrar_artigos_na_pasta()
    if not artigos:
        print("\n❌ Nenhum artigo encontrado.")
        return
    
    print(f"\n🚀 Processando {len(artigos)} artigos...")
    historico = carregar_historico()
    for artigo in artigos:
        processar_artigo(artigo, historico)

def relatorio_geral():
    historico = carregar_historico()
    if not historico:
        print("\n📭 Nenhum artigo no histórico.")
        return
    
    total = len(historico)
    reels_gerados = sum(1 for h in historico if h.get('reels_gerado') == 'sim')
    publicados = sum(1 for h in historico if h.get('status') == 'publicado')
    
    print("\n📊 RELATÓRIO GERAL")
    print("="*60)
    print(f"   Total de artigos: {total}")
    print(f"   ✅ Publicados: {publicados}")
    print(f"   🎬 Reels gerados: {reels_gerados}")
    print(f"   ⏳ Pendentes: {total - reels_gerados}")

def deletar_reels_menu():
    if not os.path.exists(PASTA_REELS):
        print("\n❌ Nenhum Reels encontrado.")
        return
    
    print("\n🗑️ DELETAR REELS")
    print("Digite a categoria e o nome do artigo separados por /")
    print("Exemplo: sala-de-estar/estilo-escandinavo")
    
    caminho = input("\n👉 Caminho: ").strip()
    if '/' in caminho:
        categoria, nome = caminho.split('/')
        if deletar_reels(categoria, nome):
            historico = carregar_historico()
            for h in historico:
                if h['categoria'] == categoria and h['titulo'].lower().replace(' ', '_') == nome:
                    h['reels_gerado'] = 'nao'
                    h['status'] = 'deletado'
                    break
            salvar_historico(historico)

# ============================================================
# 7. EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    menu()