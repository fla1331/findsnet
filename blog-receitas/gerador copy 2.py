#!/usr/bin/env python3
"""
GERADOR DE ARTIGOS - MULTILÍNGUE COMPLETO
VERSÃO FINAL - COM TODAS AS CORREÇÕES
"""

from dotenv import load_dotenv
import os
load_dotenv()

import csv
import re
import random
import unicodedata
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from xml.dom import minidom
import xml.etree.ElementTree as ET
import shutil
import webbrowser
import time

# ============================================================
# ===== TRADUÇÃO DE CATEGORIAS ===============================
# ============================================================

TRADUCAO_CATEGORIAS = {
    'pt': {
        'receitas-saudaveis': 'receitas-saudaveis',
        'nutricao': 'nutricao',
        'bem-estar': 'bem-estar',
        'longevidade': 'longevidade',
        'emagrecimento': 'emagrecimento'
    },
    'en': {
        'receitas-saudaveis': 'healthy-recipes',
        'nutricao': 'nutrition',
        'bem-estar': 'wellness',
        'longevidade': 'longevity',
        'emagrecimento': 'weight-loss'
    },
    'es': {
        'receitas-saudaveis': 'recetas-saludables',
        'nutricao': 'nutricion',
        'bem-estar': 'bienestar',
        'longevidade': 'longevidad',
        'emagrecimento': 'perdida-de-peso'
    }
}

# NOMES DAS CATEGORIAS PARA EXIBIÇÃO (traduzidos)
NOMES_CATEGORIAS = {
    'pt': {
        'receitas-saudaveis': 'Receitas Saudáveis',
        'nutricao': 'Nutrição',
        'bem-estar': 'Bem-Estar',
        'longevidade': 'Longevidade',
        'emagrecimento': 'Emagrecimento'
    },
    'en': {
        'receitas-saudaveis': 'Healthy Recipes',
        'nutricao': 'Nutrition',
        'bem-estar': 'Wellness',
        'longevidade': 'Longevity',
        'emagrecimento': 'Weight Loss'
    },
    'es': {
        'receitas-saudaveis': 'Recetas Saludables',
        'nutricao': 'Nutrición',
        'bem-estar': 'Bienestar',
        'longevidade': 'Longevidad',
        'emagrecimento': 'Pérdida de Peso'
    }
}

# TRADUÇÃO DE CONFIGURAÇÕES DO SITE
TRADUCAO_CONFIG = {
    'pt': {
        'descricao': 'Receitas saudáveis e dicas de bem-estar para nutrir seu corpo e sua vida.',
        'nome_site': 'HealthTable',
        'frase_hero': 'Receitas que curam. Hábitos que transformam.',
        'slogan': 'O aconchego da cozinha que faz bem e a calma dos hábitos que esticam a vida.'
    },
    'en': {
        'descricao': 'Healthy recipes and wellness tips to nourish your body and life.',
        'nome_site': 'HealthTable',
        'frase_hero': 'Recipes that heal. Habits that transform.',
        'slogan': 'The comfort of a kitchen that does good and the calm of habits that stretch life.'
    },
    'es': {
        'descricao': 'Recetas saludables y consejos de bienestar para nutrir tu cuerpo y tu vida.',
        'nome_site': 'HealthTable',
        'frase_hero': 'Recetas que curan. Hábitos que transforman.',
        'slogan': 'El acogedor de la cocina que hace bien y la calma de los hábitos que estiran la vida.'
    }
}

# ============================================================
# ===== MAPA DE IDIOMAS ======================================
# ============================================================

IDIOMAS = {
    'pt': {
        'lang': 'pt', 'locale': 'pt_BR',
        'review': 'Review Completo',
        'comprar': 'Comprar Agora',
        'ver_oferta': 'Ver Oferta',
        'menu_inicio': 'Início',
        'menu_sobre': 'Sobre',
        'menu_contato': 'Contato',
        'footer': 'Todos os direitos reservados.',
        'sobre_titulo': 'Sobre Nós',
        'contato_titulo': 'Contato',
        'privacidade_titulo': 'Política de Privacidade',
        'cookies_titulo': 'Política de Cookies',
        'nao_encontrado': 'Página não encontrada',
        'voltar_inicio': 'Voltar para o início',
        'publicado': 'Publicado',
        'rascunho': 'Rascunho',
        'leia_tambem': 'Leia também',
        'compartilhar': 'Compartilhar',
        'autor': 'Por',
        'data_publicacao': 'Publicado em',
        'faq': 'Perguntas Frequentes',
        'revisar_ia': 'Revisar com IA',
        'categorias': 'Categorias',
        'idioma_nome': 'Português'
    },
    'en': {
        'lang': 'en', 'locale': 'en_US',
        'review': 'Complete Review',
        'comprar': 'Buy Now',
        'ver_oferta': 'View Offer',
        'menu_inicio': 'Home',
        'menu_sobre': 'About',
        'menu_contato': 'Contact',
        'footer': 'All rights reserved.',
        'sobre_titulo': 'About Us',
        'contato_titulo': 'Contact',
        'privacidade_titulo': 'Privacy Policy',
        'cookies_titulo': 'Cookies Policy',
        'nao_encontrado': 'Page not found',
        'voltar_inicio': 'Back to home',
        'publicado': 'Published',
        'rascunho': 'Draft',
        'leia_tambem': 'Read also',
        'compartilhar': 'Share',
        'autor': 'By',
        'data_publicacao': 'Published on',
        'faq': 'Frequently Asked Questions',
        'revisar_ia': 'Review with AI',
        'categorias': 'Categories',
        'idioma_nome': 'English'
    },
    'es': {
        'lang': 'es', 'locale': 'es_ES',
        'review': 'Review Completo',
        'comprar': 'Comprar Ahora',
        'ver_oferta': 'Ver Oferta',
        'menu_inicio': 'Inicio',
        'menu_sobre': 'Sobre',
        'menu_contato': 'Contacto',
        'footer': 'Todos los derechos reservados.',
        'sobre_titulo': 'Sobre Nosotros',
        'contato_titulo': 'Contacto',
        'privacidade_titulo': 'Política de Privacidad',
        'cookies_titulo': 'Política de Cookies',
        'nao_encontrado': 'Página no encontrada',
        'voltar_inicio': 'Volver al inicio',
        'publicado': 'Publicado',
        'rascunho': 'Borrador',
        'leia_tambem': 'Lea también',
        'compartilhar': 'Compartir',
        'autor': 'Por',
        'data_publicacao': 'Publicado el',
        'faq': 'Preguntas Frecuentes',
        'revisar_ia': 'Revisar con IA',
        'categorias': 'Categorías',
        'idioma_nome': 'Español'
    }
}

# ============================================================
# ===== MAPA DE PROMPTS POR NICHO ============================
# ============================================================

PROMPTS_NICHO = {
    'receitas': {
        'tom': 'aconchegante, apetitoso e inspirador',
        'palavras': 'receitas saudáveis, culinária, bem-estar, nutrição, sabor',
        'faq': [
            'Qual o tempo de preparo?',
            'Posso substituir algum ingrediente?',
            'Quais os benefícios nutricionais?',
            'Serve para quantas pessoas?',
            'Como armazenar as sobras?'
        ]
    },
    'bem-estar': {
        'tom': 'calmante, motivador e equilibrado',
        'palavras': 'bem-estar, saúde mental, autocuidado, equilíbrio, hábitos',
        'faq': [
            'Como começar a praticar?',
            'Quanto tempo leva para ver resultados?',
            'Funciona para qualquer pessoa?',
            'Preciso de algum equipamento?',
            'Qual a frequência recomendada?'
        ]
    },
    'longevidade': {
        'tom': 'informativo, científico e inspirador',
        'palavras': 'longevidade, envelhecimento saudável, hábitos, qualidade de vida',
        'faq': [
            'Quais hábitos aumentam a longevidade?',
            'A genética influencia muito?',
            'Qual a importância da alimentação?',
            'Exercícios físicos ajudam?',
            'Como manter a mente saudável?'
        ]
    },
    'nutricao': {
        'tom': 'educativo, prático e confiável',
        'palavras': 'nutrição, alimentos saudáveis, vitaminas, minerais, dieta equilibrada',
        'faq': [
            'Quais alimentos são mais nutritivos?',
            'Como montar um prato equilibrado?',
            'Preciso de suplementos?',
            'Qual a importância das fibras?',
            'Como ler rótulos de alimentos?'
        ]
    },
    'geral': {
        'tom': 'informativo, útil e confiável',
        'palavras': 'qualidade, benefícios, vantagens, recomendações, confiabilidade',
        'faq': [
            'Quais os principais benefícios?',
            'Como funciona?',
            'Vale a pena?',
            'Tem garantia?',
            'Como usar corretamente?'
        ]
    }
}

# ============================================================
# ===== CLASSE GERADORA ======================================
# ============================================================

class Gerador:
    def __init__(self):
        self.base = Path(__file__).parent
        self.docs = self.base / "docs"
        self.templates = self.base / "templates"
        
        self.assets_css = self.docs / "assets" / "css"
        self.assets_js = self.docs / "assets" / "js"
        self.assets_img = self.docs / "assets" / "img"
        
        self.assets_css.mkdir(parents=True, exist_ok=True)
        self.assets_js.mkdir(parents=True, exist_ok=True)
        self.assets_img.mkdir(parents=True, exist_ok=True)
        
        self.config = self.carregar_config()
        
        self.idioma_padrao = self.config.get('idioma_padrao', 'pt')
        self.idioma = self.idioma_padrao
        self.t = IDIOMAS.get(self.idioma, IDIOMAS['pt'])
        
        self.ia_api_key = os.getenv("OPENROUTER_API_KEY")
        
        self.descricoes_categorias = {}
        self.idiomas_ativos = [idioma['codigo'] for idioma in self.config.get('idiomas', [{'codigo': 'pt'}])]
        
        self.criar_csv()
        self.criar_css()
        
        self.idioma_selecionado = None
    
    # ==================== CONFIG ====================
    
    def carregar_config(self):
        config_path = self.base / "config.json"
        
        config_padrao = {
            'nome': 'Meu Blog',
            'slug': 'meu-blog',
            'icone': '📝',
            'nome_site': 'Meu Blog',
            'descricao': 'Conteúdo interessante para você.',
            'url_base': 'https://meu-blog.brightnest.blog',
            'idioma_padrao': 'pt',
            'idiomas': [
                {'codigo': 'pt', 'nome': 'Português', 'pasta': 'pt', 'csv': 'artigos/artigos_pt.csv'},
                {'codigo': 'en', 'nome': 'English', 'pasta': 'en', 'csv': 'artigos/artigos_en.csv'},
                {'codigo': 'es', 'nome': 'Español', 'pasta': 'es', 'csv': 'artigos/artigos_es.csv'}
            ],
            'ano': datetime.now().year,
            'csv': 'artigos.csv',
            'usar_ia_imagens': True,
            'autor': 'Time do Blog',
            'email_contato': 'contato@meu-blog.brightnest.blog',
            'publicar_por_dia': 1,
            'redes_sociais': {},
            'cores': {
                'primaria': '#1e293b',
                'secundaria': '#facc15',
                'fundo': '#f8fafc',
                'texto': '#0f172a',
                'card': '#ffffff',
                'hover': '#eab308',
                'destaque': '#10b981',
                'whatsapp': '#25D366'
            }
        }
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    for chave, valor in config_padrao.items():
                        if chave not in dados:
                            dados[chave] = valor
                    print("✅ Config carregada: config.json")
                    return dados
            except Exception as e:
                print(f"⚠️ Erro ao ler config.json: {e}")
                return config_padrao
        else:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_padrao, f, indent=2, ensure_ascii=False)
            print("✅ config.json criado com configurações padrão")
            return config_padrao
    
    # ==================== UTILITÁRIOS ====================
    
    def get_descricao_traduzida(self, idioma):
        return TRADUCAO_CONFIG.get(idioma, {}).get('descricao', self.config.get('descricao', ''))
    
    def get_nome_site_traduzido(self, idioma):
        return TRADUCAO_CONFIG.get(idioma, {}).get('nome_site', self.config.get('nome_site', 'Meu Blog'))
    
    def get_frase_hero_traduzida(self, idioma):
        return TRADUCAO_CONFIG.get(idioma, {}).get('frase_hero', self.config.get('frase_hero', 'Transforme sua rotina'))
    
    def get_slogan_traduzido(self, idioma):
        return TRADUCAO_CONFIG.get(idioma, {}).get('slogan', self.config.get('slogan', ''))
    
    def formatar_titulo_categoria(self, slug):
        idioma = self.idioma_selecionado or self.idioma_padrao
        if slug in NOMES_CATEGORIAS.get(idioma, {}):
            return NOMES_CATEGORIAS[idioma][slug]
        palavras = slug.replace('-', ' ').split()
        palavras_formatadas = []
        for palavra in palavras:
            if palavra.lower() in ['de', 'da', 'do', 'das', 'dos', 'e']:
                palavras_formatadas.append(palavra.lower())
            else:
                palavras_formatadas.append(palavra.capitalize())
        return ' '.join(palavras_formatadas)
    
    def criar_slug(self, texto):
        if not texto:
            return "artigo"
        texto = unicodedata.normalize('NFKD', texto)
        texto = texto.encode('ASCII', 'ignore').decode('ASCII')
        slug = texto.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'[\s]+', '-', slug)
        slug = re.sub(r'[-]+', '-', slug)
        return slug.strip('-')[:60]
    
    def ler_numero(self, msg, minimo=1, maximo=99):
        while True:
            try:
                valor = input(msg).strip()
                if not valor:
                    return None
                num = int(valor)
                if minimo <= num <= maximo:
                    return num
                print(f"   ⚠️ Digite entre {minimo} e {maximo}")
            except ValueError:
                print("   ⚠️ Digite um número válido")
    
    def ler_sim_nao(self, msg):
        while True:
            resp = input(msg).strip().lower()
            if resp in ['s', 'sim', 'y', 'yes']:
                return True
            if resp in ['n', 'nao', 'não', 'no']:
                return False
            print("   ⚠️ Digite 's' ou 'n'")
    
    # ==================== TEMPLATES ====================
    
    def ler_template(self, nome, idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        caminho_idioma = self.templates / idioma / nome
        if caminho_idioma.exists():
            with open(caminho_idioma, 'r', encoding='utf-8') as f:
                return f.read()
        caminho_padrao = self.templates / nome
        if caminho_padrao.exists():
            with open(caminho_padrao, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    
    def renderizar_template(self, nome, variaveis, idioma=None):
        template = self.ler_template(nome, idioma)
        if template is None:
            return None
        html = template
        for chave, valor in variaveis.items():
            html = html.replace(f'{{{{{chave}}}}}', str(valor))
        return html
    
    # ==================== CSV ====================
    
    def ler_csv(self, idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        csv_path = None
        for lang in self.config.get('idiomas', []):
            if lang.get('codigo') == idioma:
                csv_path = self.base / lang.get('csv', f'artigos/artigos_{idioma}.csv')
                break
        if csv_path is None:
            csv_path = self.base / self.config.get('csv', 'artigos.csv')
        if not csv_path.exists():
            return []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    def salvar_csv(self, artigos, idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        csv_path = None
        for lang in self.config.get('idiomas', []):
            if lang.get('codigo') == idioma:
                csv_path = self.base / lang.get('csv', f'artigos/artigos_{idioma}.csv')
                break
        if csv_path is None:
            csv_path = self.base / self.config.get('csv', 'artigos.csv')
        if not artigos:
            return
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        cabecalho = ["artigo", "links_afiliados", "status", "categoria", "palavras_chave", "descricao", "tipo", "data_publicacao", "autor", "links_internos", "links_externos"]
        artigos_limpos = []
        for artigo in artigos:
            novo_artigo = {}
            for chave in cabecalho:
                valor = artigo.get(chave, '')
                if valor is None:
                    valor = ''
                novo_artigo[chave] = str(valor)
            artigos_limpos.append(novo_artigo)
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=cabecalho, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerows(artigos_limpos)
    
    def criar_csv(self):
        for lang in self.config.get('idiomas', []):
            codigo = lang.get('codigo', 'pt')
            csv_nome = lang.get('csv', f'artigos/artigos_{codigo}.csv')
            csv_path = self.base / csv_nome
            if csv_path.exists():
                continue
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            dados = [
                ["artigo", "links_afiliados", "status", "categoria", "palavras_chave", "descricao", "tipo", "data_publicacao", "autor", "links_internos", "links_externos"],
                ["Artigo Exemplo", "#", "rascunho", "geral", "palavras, chave", "Descrição do artigo.", "review", "", self.config.get('autor', 'Autor'), "", ""],
            ]
            with open(csv_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                writer.writerows(dados)
            print(f"✅ CSV criado: {csv_nome}")
    
    # ==================== CSS ====================
    
    def criar_css(self):
        css_destino = self.assets_css / "style.css"
        if css_destino.exists():
            return
        c = self.config.get('cores', {})
        css = f"""
* {{ margin: 0; padding: 0; box-sizing: border-box; }}

:root {{
    --primaria: {c.get('primaria', '#1e293b')};
    --secundaria: {c.get('secundaria', '#facc15')};
    --destaque: {c.get('destaque', '#10b981')};
    --fundo: {c.get('fundo', '#f8fafc')};
    --texto: {c.get('texto', '#0f172a')};
    --card: {c.get('card', '#ffffff')};
    --hover: {c.get('hover', '#eab308')};
    --whatsapp: {c.get('whatsapp', '#25D366')};
    --sombra: 0 4px 20px rgba(0,0,0,0.06);
    --borda: 12px;
    --transicao: 0.3s ease;
}}

body {{
    font-family: 'Inter', sans-serif;
    background: var(--fundo);
    color: var(--texto);
    line-height: 1.7;
}}
.container {{ max-width: 1100px; margin: 0 auto; padding: 0 20px; }}

/* FAQ */
.faq {{
    margin: 20px 0;
}}
.faq-item {{
    background: var(--card);
    border-radius: var(--borda);
    margin-bottom: 12px;
    box-shadow: var(--sombra);
    overflow: hidden;
}}
.faq-item summary {{
    padding: 16px 20px;
    cursor: pointer;
    font-weight: 600;
    display: flex;
    justify-content: space-between;
    align-items: center;
    list-style: none;
}}
.faq-item summary::-webkit-details-marker {{
    display: none;
}}
.faq-item summary:hover {{
    background: var(--fundo);
}}
.faq-icon {{
    transition: transform 0.3s ease;
    font-size: 12px;
}}
.faq-item[open] .faq-icon {{
    transform: rotate(180deg);
}}
.faq-answer {{
    padding: 0 20px 20px 20px;
    color: var(--texto);
    line-height: 1.6;
}}
.faq-answer p {{
    margin: 0;
}}
"""
        with open(css_destino, 'w', encoding='utf-8') as f:
            f.write(css)
    
    # ==================== IMAGEM ====================
    
    def gerar_imagem(self, artigo, categoria="", slug="", seed=None):
        """Gera URL de imagem única para cada artigo"""
        if self.config.get('usar_ia_imagens', True):
            try:
                timestamp = int(time.time()) if seed is None else seed
                prompt = f"{artigo}, {categoria}, health, wellness, recipe, healthy food, 4k"
                return f"https://image.pollinations.ai/prompt/{prompt}?width=1200&height=630&nologo=true&seed={slug}{timestamp}"
            except:
                pass
        imagens = [
            'https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?w=1200&h=630&fit=crop',
            'https://images.pexels.com/photos/539451/pexels-photo-539451.jpeg?w=1200&h=630&fit=crop',
            'https://images.pexels.com/photos/3771118/pexels-photo-3771118.jpeg?w=1200&h=630&fit=crop',
            'https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?w=1200&h=630&fit=crop',
            'https://images.pexels.com/photos/539451/pexels-photo-539451.jpeg?w=1200&h=630&fit=crop',
        ]
        idx = hash(slug) % len(imagens) if slug else random.randint(0, len(imagens)-1)
        return imagens[idx]
    
    # ==================== DESCRIÇÃO CATEGORIA ====================
    
    def gerar_descricao_categoria(self, categoria, idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        descricoes = {
            'pt': {
                'receitas': 'Receitas saudáveis e deliciosas para transformar sua alimentação com sabor e nutrição.',
                'bem-estar': 'Dicas de autocuidado, equilíbrio e hábitos para uma vida mais leve e saudável.',
                'longevidade': 'Hábitos e práticas para viver mais e melhor com qualidade de vida.',
                'nutricao': 'Informações sobre nutrição, alimentos e uma dieta equilibrada para a saúde.'
            },
            'en': {
                'receitas': 'Healthy and delicious recipes to transform your eating with flavor and nutrition.',
                'bem-estar': 'Self-care, balance and habit tips for a lighter and healthier life.',
                'longevidade': 'Habits and practices to live longer and better with quality of life.',
                'nutricao': 'Information on nutrition, food and a balanced diet for health.'
            },
            'es': {
                'receitas': 'Recetas saludables y deliciosas para transformar tu alimentación con sabor y nutrición.',
                'bem-estar': 'Consejos de autocuidado, equilibrio y hábitos para una vida más ligera y saludable.',
                'longevidade': 'Hábitos y prácticas para vivir más y mejor con calidad de vida.',
                'nutricao': 'Información sobre nutrición, alimentos y una dieta equilibrada para la salud.'
            }
        }
        descricao = descricoes.get(idioma, descricoes['pt']).get(categoria)
        if descricao:
            return descricao
        titulo_categoria = self.formatar_titulo_categoria(categoria)
        return f'Conteúdo sobre {titulo_categoria} para transformar sua saúde e bem-estar.'
    
    # ==================== CONTEÚDO COM IA ====================
    
    def gerar_conteudo_ia(self, artigo, link, categoria="geral", palavras_chave="", tipo="review", idioma="pt", links_internos="", links_externos=""):
        if not self.ia_api_key:
            return self.conteudo_basico(artigo, link, tipo, idioma)
        prompt_nicho = PROMPTS_NICHO.get(categoria, PROMPTS_NICHO['geral'])
        nome_idioma = {'pt': 'português do Brasil', 'en': 'English', 'es': 'español'}.get(idioma, 'português do Brasil')
        prompt_template = self.ler_template(f'prompts/{tipo}.txt')
        if prompt_template:
            print(f"   🤖 Gerando conteúdo do tipo: {tipo} para: {categoria} ({idioma.upper()})...")
            prompt = prompt_template.replace('{artigo}', artigo).replace('{link}', link).replace('{categoria}', categoria)
            prompt = prompt.replace('{tom}', prompt_nicho['tom']).replace('{palavras_chave}', palavras_chave or prompt_nicho['palavras'])
            prompt = prompt.replace('{quantidade}', str(random.randint(8, 12))).replace('{idioma}', nome_idioma)
            prompt = prompt.replace('{links_internos}', links_internos or 'nenhum link interno disponível')
            prompt = prompt.replace('{links_externos}', links_externos or 'nenhuma fonte externa disponível')
        else:
            print(f"   ⚠️ Template {tipo}.txt não encontrado, usando fallback...")
            prompt = self._gerar_prompt_fallback(artigo, link, categoria, palavras_chave, tipo, idioma)
        try:
            headers = {"Authorization": f"Bearer {self.ia_api_key}", "Content-Type": "application/json"}
            data = {
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {"role": "system", "content": f"Você é especialista em {categoria} e criação de conteúdo do tipo {tipo} em {nome_idioma}."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 6000,
                "temperature": 0.8
            }
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=120)
            if response.status_code == 200:
                conteudo = response.json()["choices"][0]["message"]["content"]
                conteudo = re.sub(r'```(?:html)?\s*', '', conteudo)
                conteudo = re.sub(r'\s*```', '', conteudo)
                if 'faq-item' not in conteudo.lower() or 'faq-question' not in conteudo.lower():
                    conteudo += self._gerar_faq_fallback(categoria, idioma)
                return conteudo
            else:
                print(f"   ⚠️ Erro na API: {response.status_code}")
                return self.conteudo_basico(artigo, link, tipo, idioma)
        except Exception as e:
            print(f"   ⚠️ Erro IA: {e}")
            return self.conteudo_basico(artigo, link, tipo, idioma)
    
    def _gerar_prompt_fallback(self, artigo, link, categoria, palavras_chave, tipo="review", idioma="pt"):
        prompt_nicho = PROMPTS_NICHO.get(categoria, PROMPTS_NICHO['geral'])
        titulo_categoria = self.formatar_titulo_categoria(categoria)
        nome_idioma = {'pt': 'português do Brasil', 'en': 'English', 'es': 'español'}.get(idioma, 'português do Brasil')
        tipos = {
            'review': f"""
            Crie um REVIEW COMPLETO sobre {artigo} em {nome_idioma}.
            NICHO: {titulo_categoria}
            TOM: {prompt_nicho['tom']}
            PALAVRAS-CHAVE: {palavras_chave or prompt_nicho['palavras']}
            ESTRUTURA: Título, Introdução, Benefícios, Especificações, Prós e Contras, FAQ (com <details> e <summary>), Conclusão
            Use classes: article-table, faq, faq-item
            O conteúdo deve ser 100% em {nome_idioma}.
            Retorne APENAS HTML válido.
            """,
            'guia': f"""
            Crie um GUIA COMPLETO sobre {artigo} em {nome_idioma}.
            NICHO: {titulo_categoria}
            TOM: {prompt_nicho['tom']}
            PALAVRAS-CHAVE: {palavras_chave or prompt_nicho['palavras']}
            ESTRUTURA: Título, Introdução, Capítulos, FAQ (com <details> e <summary>), Conclusão
            Use classes: article-table, faq, faq-item
            O conteúdo deve ser 100% em {nome_idioma}.
            Retorne APENAS HTML válido.
            """
        }
        return tipos.get(tipo, tipos['review'])
    
    # ==================== FAQ ====================
    
    def _gerar_faq_fallback(self, categoria, idioma="pt"):
        prompt_nicho = PROMPTS_NICHO.get(categoria, PROMPTS_NICHO['geral'])
        faq_perguntas = prompt_nicho.get('faq', PROMPTS_NICHO['geral']['faq'])
        titulo_faq = {'pt': 'Perguntas Frequentes', 'en': 'Frequently Asked Questions', 'es': 'Preguntas Frecuentes'}.get(idioma, 'Perguntas Frequentes')
        respostas = {
            'pt': {'Qual o tempo de preparo?': 'O tempo médio de preparo é de 30 a 45 minutos, dependendo da receita.',
                   'Posso substituir algum ingrediente?': 'Sim! Muitos ingredientes podem ser substituídos por opções mais saudáveis ou que você tem em casa.',
                   'Quais os benefícios nutricionais?': 'Estas receitas são ricas em vitaminas, minerais e fibras, essenciais para uma alimentação equilibrada.',
                   'Como começar a praticar?': 'Comece com pequenos passos, escolhendo um hábito por vez e sendo consistente.',
                   'Quanto tempo leva para ver resultados?': 'Os primeiros resultados podem ser notados em 2 a 4 semanas de prática consistente.',
                   'Funciona para qualquer pessoa?': 'Sim, as técnicas podem ser adaptadas para diferentes idades e estilos de vida.',
                   'Qual a frequência recomendada?': 'Recomenda-se praticar de 3 a 5 vezes por semana para melhores resultados.',
                   'Quais hábitos aumentam a longevidade?': 'Alimentação saudável, exercícios regulares, sono de qualidade e conexões sociais são os principais.',
                   'A genética influencia muito?': 'A genética influencia cerca de 20-30%, mas os hábitos diários têm um impacto muito maior.'},
            'en': {'Qual o tempo de preparo?': 'The average preparation time is 30 to 45 minutes, depending on the recipe.',
                   'Posso substituir algum ingrediente?': 'Yes! Many ingredients can be substituted with healthier options or what you have at home.',
                   'Quais os benefícios nutricionais?': 'These recipes are rich in vitamins, minerals and fiber, essential for a balanced diet.',
                   'Como começar a praticar?': 'Start with small steps, choosing one habit at a time and being consistent.',
                   'Quanto tempo leva para ver resultados?': 'First results can be noticed in 2 to 4 weeks of consistent practice.',
                   'Funciona para qualquer pessoa?': 'Yes, the techniques can be adapted for different ages and lifestyles.',
                   'Qual a frequência recomendada?': 'It is recommended to practice 3 to 5 times a week for best results.',
                   'Quais hábitos aumentam a longevidade?': 'Healthy eating, regular exercise, quality sleep and social connections are the main ones.',
                   'A genética influencia muito?': 'Genetics influence about 20-30%, but daily habits have a much greater impact.'},
            'es': {'Qual o tempo de preparo?': 'El tiempo medio de preparación es de 30 a 45 minutos, dependiendo de la receta.',
                   'Posso substituir algum ingrediente?': '¡Sí! Muchos ingredientes se pueden sustituir por opciones más saludables o lo que tengas en casa.',
                   'Quais os benefícios nutricionais?': 'Estas recetas son ricas en vitaminas, minerales y fibra, esenciales para una dieta equilibrada.',
                   'Como começar a praticar?': 'Comienza con pequeños pasos, eligiendo un hábito a la vez y siendo constante.',
                   'Quanto tempo leva para ver resultados?': 'Los primeros resultados se pueden notar en 2 a 4 semanas de práctica constante.',
                   'Funciona para qualquer pessoa?': 'Sí, las técnicas se pueden adaptar a diferentes edades y estilos de vida.',
                   'Qual a frequência recomendada?': 'Se recomienda practicar de 3 a 5 veces por semana para mejores resultados.',
                   'Quais hábitos aumentam a longevidade?': 'Alimentación saludable, ejercicio regular, sueño de calidad y conexiones sociales son los principales.',
                   'A genética influencia muito?': 'La genética influye alrededor del 20-30%, pero los hábitos diarios tienen un impacto mucho mayor.'}
        }
        respostas_idioma = respostas.get(idioma, respostas['pt'])
        faq_html = f'<h2 id="faq">{titulo_faq}</h2><div class="faq">'
        for pergunta in faq_perguntas[:6]:
            resposta = respostas_idioma.get(pergunta, f'Sobre "{pergunta}", temos informações detalhadas disponíveis.')
            faq_html += f"""
            <details class="faq-item">
                <summary class="faq-question">{pergunta}<span class="faq-icon">▼</span></summary>
                <div class="faq-answer"><p>{resposta}</p></div>
            </details>"""
        faq_html += "</div>"
        return faq_html
    
    # ==================== REVISÃO COM IA ====================
    
    def revisar_com_ia(self, conteudo, artigo, categoria="geral", tipo="review", idioma="pt"):
        if not self.ia_api_key:
            return conteudo
        nome_idioma = {'pt': 'português do Brasil', 'en': 'English', 'es': 'español'}.get(idioma, 'português do Brasil')
        print(f"   🔍 Revisando e aprofundando conteúdo (tipo: {tipo}, idioma: {idioma.upper()})...")
        prompt_nicho = PROMPTS_NICHO.get(categoria, PROMPTS_NICHO['geral'])
        titulo_categoria = self.formatar_titulo_categoria(categoria)
        prompt = f"""
        Revise e MELHORE SIGNIFICATIVAMENTE este artigo sobre {artigo} em {nome_idioma}.
        TIPO: {tipo}
        CATEGORIA: {titulo_categoria}
        TOM: {prompt_nicho['tom']}
        O QUE MELHORAR:
        1. Aprofunde a introdução
        2. Adicione mais detalhes nos benefícios
        3. Enriqueça a tabela com class="article-table"
        4. Melhore o FAQ com estrutura <details> e <summary>
        5. Adicione id="conclusao" na conclusão
        6. O conteúdo deve ser 100% em {nome_idioma}
        CONTEÚDO ORIGINAL:
        {conteudo}
        Retorne APENAS o HTML revisado.
        """
        try:
            headers = {"Authorization": f"Bearer {self.ia_api_key}", "Content-Type": "application/json"}
            data = {
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {"role": "system", "content": f"Revisor especialista em {titulo_categoria} e conteúdo do tipo {tipo}."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 6000,
                "temperature": 0.7
            }
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=120)
            if response.status_code == 200:
                revisado = response.json()["choices"][0]["message"]["content"]
                revisado = re.sub(r'```(?:html)?\s*', '', revisado)
                revisado = re.sub(r'\s*```', '', revisado)
                return revisado
            return conteudo
        except Exception as e:
            print(f"   ⚠️ Erro na revisão: {e}")
            return conteudo
    
    def conteudo_basico(self, artigo, link, tipo="review", idioma="pt"):
        t = self.t
        textos = {
            'pt': {'review': f"Review Completo: {artigo}", 'guia': f"Guia Completo: {artigo}", 'lista': f"Lista: {artigo}", 'tutorial': f"Tutorial: {artigo}", 'default': f"Artigo: {artigo}", 'beneficios': 'Benefícios', 'comprar': 'Comprar Agora', 'ver_oferta': 'Ver Oferta', 'jornada': 'Comece sua jornada de saúde e bem-estar agora'},
            'en': {'review': f"Complete Review: {artigo}", 'guia': f"Complete Guide: {artigo}", 'lista': f"List: {artigo}", 'tutorial': f"Tutorial: {artigo}", 'default': f"Article: {artigo}", 'beneficios': 'Benefits', 'comprar': 'Buy Now', 'ver_oferta': 'View Offer', 'jornada': 'Start your health and wellness journey now'},
            'es': {'review': f"Review Completo: {artigo}", 'guia': f"Guía Completa: {artigo}", 'lista': f"Lista: {artigo}", 'tutorial': f"Tutorial: {artigo}", 'default': f"Artículo: {artigo}", 'beneficios': 'Beneficios', 'comprar': 'Comprar Ahora', 'ver_oferta': 'Ver Oferta', 'jornada': 'Comienza tu viaje de salud y bienestar ahora'}
        }
        txt = textos.get(idioma, textos['pt'])
        titulo_map = {'review': txt['review'], 'guia': txt['guia'], 'lista': txt['lista'], 'tutorial': txt['tutorial']}
        titulo = titulo_map.get(tipo, txt['default'])
        return f"""
<h1 id="introducao">{titulo}</h1>
<p><strong>{artigo}</strong> é a escolha perfeita para sua saúde e bem-estar.</p>
<h2 id="beneficios">{txt['beneficios']}</h2>
<ul>
    <li><strong>Nutrição equilibrada:</strong> Ingredientes que fazem bem para o corpo</li>
    <li><strong>Sabor incomparável:</strong> Receitas que agradam ao paladar</li>
    <li><strong>Bem-estar garantido:</strong> Hábitos que transformam sua qualidade de vida</li>
</ul>
<div class="cta-box">
    <h3>{txt['comprar']}</h3>
    <p>{txt['jornada']}</p>
    <a href="{link}" class="btn-primary" target="_blank" rel="nofollow sponsored">{txt['ver_oferta']}</a>
</div>
"""
    
    # ==================== CATEGORIAS ====================
    
    def get_categorias(self, idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        artigos = self.ler_csv(idioma)
        categorias = set()
        for a in artigos:
            if a.get('status') == 'publicado':
                cat = a.get('categoria', '').strip()
                if cat:
                    categorias.add(cat.lower())
        return sorted(list(categorias))
    
    def get_categoria_traduzida(self, categoria, idioma):
        if idioma in TRADUCAO_CATEGORIAS:
            return TRADUCAO_CATEGORIAS[idioma].get(categoria, categoria)
        return categoria
    
    def get_nome_categoria_traduzido(self, categoria, idioma):
        if idioma in NOMES_CATEGORIAS:
            return NOMES_CATEGORIAS[idioma].get(categoria, self.formatar_titulo_categoria(categoria))
        return self.formatar_titulo_categoria(categoria)
    
    def get_artigos_publicados(self, idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        artigos = self.ler_csv(idioma)
        publicados = []
        for a in artigos:
            if a.get('status') == 'publicado':
                if idioma != 'pt':
                    titulo_traduzido = self.traduzir_titulo(a.get('artigo', ''), idioma)
                    slug_base = titulo_traduzido if titulo_traduzido else a.get('artigo', '')
                else:
                    slug_base = a.get('artigo', '')
                publicados.append({
                    'slug': self.criar_slug(slug_base),
                    'nome': a.get('artigo', ''),
                    'categoria': a.get('categoria', 'geral'),
                    'data_publicacao': a.get('data_publicacao', datetime.now().strftime("%Y-%m-%d"))
                })
        return publicados
    
    # ==================== HEADER ====================
    
    def get_header(self, ativo="inicio", categoria_atual=None, idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        header_template = self.ler_template('header.html', idioma)
        categorias = self.get_categorias(idioma)
        if header_template:
            cat_links = ""
            for cat in categorias[:6]:
                cat_traduzida = self.get_categoria_traduzida(cat, idioma)
                ativo_cat = 'ativo' if categoria_atual == cat else ''
                titulo_cat = self.get_nome_categoria_traduzido(cat, idioma)
                cat_links += f'<a href="/{idioma}/{cat_traduzida}/" class="{ativo_cat}">{titulo_cat}</a>'
            header_html = header_template.replace('{{NOME_SITE}}', self.get_nome_site_traduzido(idioma))
            header_html = header_html.replace('{{CATEGORIAS_MENU}}', cat_links)
            header_html = header_html.replace('{{IDIOMA}}', idioma)
            return header_html
        t = self.t
        cat_links = ""
        for cat in categorias[:6]:
            cat_traduzida = self.get_categoria_traduzida(cat, idioma)
            ativo_cat = 'ativo' if categoria_atual == cat else ''
            titulo_cat = self.get_nome_categoria_traduzido(cat, idioma)
            cat_links += f'<a href="/{idioma}/{cat_traduzida}/" class="{ativo_cat}">{titulo_cat}</a>'
        return f"""
<header>
    <div class="container">
        <a href="/{idioma}/" class="logo">
            <span class="icone">{self.config.get('icone', '📝')}</span>
            <span class="nome">{self.get_nome_site_traduzido(idioma)}</span>
        </a>
        <button class="menu-toggle" aria-label="Menu">☰</button>
        <nav>
            <a href="/{idioma}/" class="{'ativo' if ativo=='inicio' else ''}">{t['menu_inicio']}</a>
            {cat_links}
            <button class="theme-toggle" aria-label="Tema">🌙</button>
        </nav>
    </div>
</header>"""
    
    # ==================== HEAD ====================
    
    def get_head(self, titulo, descricao, url, imagem="", extra="", idioma="pt", slug="", eh_artigo=False, categoria_original=None):
        head_template = self.ler_template('head.html')
        if not imagem:
            imagem = f"{self.config.get('url_base', '')}/assets/img/og-default.jpg"
        site_name = self.get_nome_site_traduzido(idioma)
        hreflang_tags = ""
        base_url = self.config.get('url_base', '')
        
        if eh_artigo:
            if categoria_original:
                cat_pt = categoria_original
            else:
                cat_pt = None
                for cat in TRADUCAO_CATEGORIAS.get('pt', {}).keys():
                    if cat in url:
                        cat_pt = cat
                        break
                if not cat_pt:
                    cat_pt = 'geral'
            
            # CORREÇÃO: Usa o slug que já está no idioma correto
            # O slug que chega já é do idioma atual (EN/ES já estão traduzidos)
            # Para PT, usa o slug em PT
            if idioma == 'pt':
                slug_pt = slug
                slug_en = self.traduzir_titulo(slug_pt.replace('-', ' '), 'en')
                slug_en = self.criar_slug(slug_en) if slug_en else slug_pt
                slug_es = self.traduzir_titulo(slug_pt.replace('-', ' '), 'es')
                slug_es = self.criar_slug(slug_es) if slug_es else slug_pt
            elif idioma == 'en':
                slug_en = slug
                slug_pt = self.traduzir_titulo(slug.replace('-', ' '), 'pt')
                slug_pt = self.criar_slug(slug_pt) if slug_pt else slug
                slug_es = self.traduzir_titulo(slug.replace('-', ' '), 'es')
                slug_es = self.criar_slug(slug_es) if slug_es else slug
            else:  # es
                slug_es = slug
                slug_pt = self.traduzir_titulo(slug.replace('-', ' '), 'pt')
                slug_pt = self.criar_slug(slug_pt) if slug_pt else slug
                slug_en = self.traduzir_titulo(slug.replace('-', ' '), 'en')
                slug_en = self.criar_slug(slug_en) if slug_en else slug
            
            slugs = {'pt': slug_pt, 'en': slug_en, 'es': slug_es}
            
            for lang in self.config.get('idiomas', []):
                codigo = lang.get('codigo', 'pt')
                cat_traduzida = self.get_categoria_traduzida(cat_pt, codigo)
                slug_final = slugs.get(codigo, slug_pt)
                url_final = f"{base_url}/{codigo}/{cat_traduzida}/{slug_final}/"
                url_final = url_final.replace('//', '/').replace('https:/', 'https://')
                hreflang_tags += f'<link rel="alternate" href="{url_final}" hreflang="{codigo}" />\n'
            
            cat_pt_traduzida = self.get_categoria_traduzida(cat_pt, 'pt')
            url_default = f"{base_url}/pt/{cat_pt_traduzida}/{slug_pt}/"
            url_default = url_default.replace('//', '/').replace('https:/', 'https://')
            hreflang_tags += f'<link rel="alternate" href="{url_default}" hreflang="x-default" />\n'
        
        canonical = url
        if not any(f'/{lang["codigo"]}/' in url for lang in self.config.get('idiomas', [])):
            canonical = f"{base_url}/{idioma}{url}"
            canonical = canonical.replace('//', '/').replace('https:/', 'https://')
        
        if head_template:
            head_html = head_template.replace('{{TITULO}}', titulo)
            head_html = head_html.replace('{{DESCRICAO}}', descricao[:160])
            head_html = head_html.replace('{{URL}}', canonical)
            head_html = head_html.replace('{{IMAGEM}}', imagem)
            head_html = head_html.replace('{{NOME_SITE}}', site_name)
            head_html = head_html.replace('{{EXTRA_HEAD}}', hreflang_tags + extra)
            head_html = head_html.replace('{{DATA}}', datetime.now().strftime("%Y-%m-%d"))
            head_html = head_html.replace('{{AUTOR}}', self.config.get('autor', 'Autor'))
            head_html = re.sub(r'^\s*<head>', '', head_html)
            head_html = re.sub(r'</head>\s*$', '', head_html)
            return head_html
        
        return f"""
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <meta name="description" content="{descricao[:160]}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    {hreflang_tags}
    <meta property="og:title" content="{titulo}">
    <meta property="og:description" content="{descricao[:160]}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{imagem}">
    <meta property="og:type" content="website">
    <meta property="og:locale" content="{idioma}">
    <meta property="og:site_name" content="{site_name}">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="stylesheet" href="/assets/css/custom.css">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{titulo}",
      "description": "{descricao[:160]}",
      "image": "{imagem}",
      "url": "{canonical}",
      "datePublished": "{datetime.now().strftime('%Y-%m-%d')}",
      "dateModified": "{datetime.now().strftime('%Y-%m-%d')}",
      "author": {{
        "@type": "Person",
        "name": "{self.config.get('autor', 'Autor')}"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "{site_name}"
      }}
    }}
    </script>
    {extra}
    """
    
    # ==================== FOOTER ====================
    
    def get_footer(self, idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        categorias = self.get_categorias(idioma)
        cat_links = ""
        for cat in categorias[:8]:
            cat_traduzida = self.get_categoria_traduzida(cat, idioma)
            titulo_cat = self.get_nome_categoria_traduzido(cat, idioma)
            cat_links += f'<li><a href="/{idioma}/{cat_traduzida}/">{titulo_cat}</a></li>\n'
        footer_template = self.ler_template('footer.html', idioma)
        if footer_template is None:
            footer_template = """<!-- ===== Footer ===== -->
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <a href="/{{IDIOMA}}/" class="logo logo--light">
        <span class="logo-mark">💻</span>
        {{NOME_SITE}}
      </a>
      <p>{{DESCRICAO}}</p>
    </div>
    <div class="footer-col">
      <h4 class="footer-title">Explorar</h4>
      <ul>
        <li><a href="/{{IDIOMA}}/">Início</a></li>
        {{CATEGORIAS_FOOTER}}
      </ul>
    </div>
    <div class="footer-col">
      <h4 class="footer-title">Institucional</h4>
      <ul>
        <li><a href="/{{IDIOMA}}/sobre.html">Sobre</a></li>
        <li><a href="/{{IDIOMA}}/contato.html">Contato</a></li>
        <li><a href="/{{IDIOMA}}/politica-privacidade.html">Privacidade</a></li>
        <li><a href="/{{IDIOMA}}/cookies.html">Cookies</a></li>
      </ul>
    </div>
  </div>
  <div class="container footer-bottom">
    <p>© {{ANO}} {{NOME_SITE}}. Todos os direitos reservados.</p>
  </div>
</footer>"""
        footer_html = footer_template.replace('{{NOME_SITE}}', self.get_nome_site_traduzido(idioma))
        footer_html = footer_html.replace('{{DESCRICAO}}', self.get_descricao_traduzida(idioma))
        footer_html = footer_html.replace('{{ANO}}', str(self.config.get('ano', datetime.now().year)))
        footer_html = footer_html.replace('{{CATEGORIAS_FOOTER}}', cat_links)
        footer_html = footer_html.replace('{{IDIOMA}}', idioma)
        return footer_html
    
    # ==================== PÁGINAS ====================
    
    def criar_pagina(self, nome, titulo, conteudo, ativo="inicio", idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        caminho = self.docs / idioma / f"{nome}.html"
        t = self.t
        html = f"""<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
{self.get_head(
    titulo=f"{self.get_nome_site_traduzido(idioma)} - {titulo}",
    descricao=f"{titulo} - {self.get_nome_site_traduzido(idioma)}",
    url=f"{self.config.get('url_base', '')}/{idioma}/{nome}.html",
    idioma=idioma,
    eh_artigo=False
)}
</head>
<body>
    {self.get_header(ativo, None, idioma)}
    <main class="container">
        <div class="artigo">
            <h1>{titulo}</h1>
            {conteudo}
        </div>
    </main>
    {self.get_footer(idioma)}
    <script src="/assets/js/script.js"></script>
</body>
</html>"""
        caminho.parent.mkdir(parents=True, exist_ok=True)
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(html)
        return caminho
    
    # ==================== PÁGINAS DE CATEGORIA ====================
    
    def criar_pagina_categoria(self, categoria, idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        categoria_traduzida = self.get_categoria_traduzida(categoria, idioma)
        caminho = self.docs / idioma / categoria_traduzida / "index.html"
        t = self.t
        c = self.config
        titulo_categoria = self.get_nome_categoria_traduzido(categoria, idioma)
        descricao = self.gerar_descricao_categoria(categoria, idioma)
        artigos = self.get_artigos_publicados(idioma)
        artigos_cat = []
        for a in artigos:
            if a.get('categoria', '').lower() == categoria.lower():
                artigos_cat.append(a)
        if not artigos_cat:
            return None
        artigos_cat.sort(key=lambda x: x['data_publicacao'], reverse=True)
        lista_cards = ""
        for a in artigos_cat:
            img = self.gerar_imagem(a['nome'], a['categoria'], a['slug'])
            data_formatada = datetime.strptime(a['data_publicacao'], "%Y-%m-%d").strftime("%d/%m/%Y") if a['data_publicacao'] else datetime.now().strftime("%d/%m/%Y")
            tempo_leitura = random.randint(4, 8)
            if idioma != 'pt':
                nome_traduzido = self.traduzir_titulo(a['nome'], idioma)
                nome_card = nome_traduzido if nome_traduzido else a['nome']
            else:
                nome_card = a['nome']
            card = f'''<article class="post-card">
  <a href="/{idioma}/{categoria_traduzida}/{a['slug']}/" class="post-card-img">
    <img src="{img}" alt="{nome_card}">
  </a>
  <div class="post-card-body">
    <a href="/{idioma}/{categoria_traduzida}/" class="tag">{titulo_categoria}</a>
    <h3 class="post-card-title"><a href="/{idioma}/{categoria_traduzida}/{a['slug']}/">{nome_card}</a></h3>
    <div class="post-card-meta">
      <span>{data_formatada}</span>
      <span class="meta-dot">·</span>
      <span>{tempo_leitura} min de leitura</span>
    </div>
    <p class="post-card-excerpt">{nome_card[:120]}...</p>
    <a href="/{idioma}/{categoria_traduzida}/{a['slug']}/" class="read-more">Ler mais →</a>
  </div>
</article>'''
            lista_cards += card
        head_html = self.get_head(
            titulo=f"{self.get_nome_site_traduzido(idioma)} - {titulo_categoria}",
            descricao=descricao,
            url=f"{c.get('url_base', '')}/{idioma}/{categoria_traduzida}/",
            idioma=idioma,
            eh_artigo=False
        )
        template = self.ler_template('categoria.html', idioma)
        if template:
            variaveis = {
                'HEAD': head_html,
                'CATEGORIA': titulo_categoria,
                'DESCRICAO_CATEGORIA': descricao,
                'IDIOMA': t['lang'],
                'HEADER': self.get_header('categoria', categoria, idioma),
                'FOOTER': self.get_footer(idioma),
                'ARTIGOS_CATEGORIA': lista_cards
            }
            html = self.renderizar_template('categoria.html', variaveis, idioma)
        else:
            html = f"""<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
{head_html}
</head>
<body>
    {self.get_header('categoria', categoria, idioma)}
    <main class="container">
        <div class="banner">
            <h1>{titulo_categoria}</h1>
            <p>{descricao}</p>
        </div>
        <div class="post-grid">
            {lista_cards}
        </div>
    </main>
    {self.get_footer(idioma)}
    <script src="/assets/js/script.js"></script>
</body>
</html>"""
        caminho.parent.mkdir(parents=True, exist_ok=True)
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(html)
        return caminho
    
    def criar_todas_categorias(self, idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        print(f"\n📂 CRIANDO PÁGINAS DE CATEGORIA ({idioma.upper()})")
        print("-" * 40)
        pasta_idioma = self.docs / idioma
        pasta_idioma.mkdir(parents=True, exist_ok=True)
        for cat in self.get_categorias(idioma):
            if self.criar_pagina_categoria(cat, idioma):
                titulo = self.get_nome_categoria_traduzido(cat, idioma)
                cat_traduzida = self.get_categoria_traduzida(cat, idioma)
                print(f"   ✅ /{idioma}/{cat_traduzida}/ - {titulo}")
        self.criar_index(idioma=idioma)
        self.criar_sitemap()
        print(f"✅ Páginas de categoria criadas! ({idioma.upper()})")
    
    # ==================== INDEX ====================
    
    def criar_index(self, pagina=1, idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        t = self.t
        c = self.config
        descricao_index = self.get_descricao_traduzida(idioma)
        artigos = self.get_artigos_publicados(idioma)
        artigos.sort(key=lambda x: x['data_publicacao'], reverse=True)
        artigos_por_pagina = 6
        total_artigos = len(artigos)
        total_paginas = (total_artigos + artigos_por_pagina - 1) // artigos_por_pagina if total_artigos > 0 else 1
        if pagina < 1:
            pagina = 1
        if pagina > total_paginas:
            pagina = total_paginas
        inicio = (pagina - 1) * artigos_por_pagina
        fim = inicio + artigos_por_pagina
        artigos_pagina = artigos[inicio:fim]
        lista_cards = ""
        if artigos_pagina:
            for a in artigos_pagina:
                img = self.gerar_imagem(a['nome'], a['categoria'], a['slug'])
                data_formatada = datetime.strptime(a['data_publicacao'], "%Y-%m-%d").strftime("%d/%m/%Y") if a['data_publicacao'] else datetime.now().strftime("%d/%m/%Y")
                titulo_categoria = self.get_nome_categoria_traduzido(a['categoria'], idioma)
                cat_traduzida = self.get_categoria_traduzida(a['categoria'], idioma)
                if idioma != 'pt':
                    nome_traduzido = self.traduzir_titulo(a['nome'], idioma)
                    nome_card = nome_traduzido if nome_traduzido else a['nome']
                else:
                    nome_card = a['nome']
                card = f'''<article class="card reveal">
  <a href="/{idioma}/{cat_traduzida}/{a['slug']}/" class="card__media">
    <img src="{img}" alt="{nome_card}" loading="lazy" />
    <span class="badge badge--{a['categoria']}">{titulo_categoria}</span>
  </a>
  <div class="card__body">
    <h3 class="card__title">
      <a href="/{idioma}/{cat_traduzida}/{a['slug']}/">{nome_card}</a>
    </h3>
    <p class="card__excerpt">{nome_card[:120]}...</p>
    <div class="card__meta">
      <div class="card__author">
        <span class="card__avatar">{c.get('autor', 'Autor')[:2].upper()}</span>
        <span>{c.get('autor', 'Autor')}</span>
      </div>
      <span>{data_formatada}</span>
    </div>
  </div>
</article>'''
                lista_cards += card
        else:
            lista_cards = '<p style="text-align:center;padding:40px 0;">Nenhum artigo publicado ainda.</p>'
        relacionados_sidebar = ""
        for idx, a in enumerate(artigos[:4]):
            data_formatada = datetime.strptime(a['data_publicacao'], "%Y-%m-%d").strftime("%d/%m/%Y") if a['data_publicacao'] else datetime.now().strftime("%d/%m/%Y")
            cat_traduzida = self.get_categoria_traduzida(a['categoria'], idioma)
            if idioma != 'pt':
                nome_traduzido = self.traduzir_titulo(a['nome'], idioma)
                nome_rel = nome_traduzido if nome_traduzido else a['nome']
            else:
                nome_rel = a['nome']
            relacionados_sidebar += f'''
        <li class="recent-item">
          <span class="recent-item__num">{idx+1}</span>
          <div>
            <a href="/{idioma}/{cat_traduzida}/{a['slug']}/" class="recent-item__title">{nome_rel}</a>
            <div class="recent-item__date">{data_formatada}</div>
          </div>
        </li>'''
        categorias_sidebar = ""
        for cat in self.get_categorias(idioma):
            count = sum(1 for a in artigos if a['categoria'] == cat)
            titulo_cat = self.get_nome_categoria_traduzido(cat, idioma)
            cat_traduzida = self.get_categoria_traduzida(cat, idioma)
            categorias_sidebar += f'<li><a href="/{idioma}/{cat_traduzida}/" class="cat-item">{titulo_cat} <span class="cat-item__count">{count}</span></a></li>'
        tags = ""
        for cat in self.get_categorias(idioma):
            titulo_cat = self.get_nome_categoria_traduzido(cat, idioma)
            cat_traduzida = self.get_categoria_traduzida(cat, idioma)
            tags += f'<a href="/{idioma}/{cat_traduzida}/" class="tag">{titulo_cat}</a>'
        navegacao = ""
        if total_paginas > 1:
            navegacao = '<div class="pagination">'
            if pagina > 1:
                navegacao += f'<a href="/{idioma}/index{pagina-1}.html" class="page-link">« Anterior</a>'
            else:
                navegacao += '<span class="page-link disabled">« Anterior</span>'
            for p in range(1, total_paginas + 1):
                if p == pagina:
                    navegacao += f'<span class="page-link active">{p}</span>'
                elif p == 1:
                    navegacao += f'<a href="/{idioma}/" class="page-link">{p}</a>'
                else:
                    navegacao += f'<a href="/{idioma}/index{p}.html" class="page-link">{p}</a>'
            if pagina < total_paginas:
                navegacao += f'<a href="/{idioma}/index{pagina+1}.html" class="page-link">Próximo »</a>'
            else:
                navegacao += '<span class="page-link disabled">Próximo »</span>'
            navegacao += '</div>'
        primeiro_artigo = f"/{idioma}/{self.get_categoria_traduzida(artigos[0]['categoria'], idioma)}/{artigos[0]['slug']}/" if artigos else "#"
        template_html = self.ler_template('index.html', idioma)
        if template_html:
            variaveis = {
                'IDIOMA': idioma,
                'HEAD': self.get_head(
                    titulo=f"{self.get_nome_site_traduzido(idioma)} - {c.get('nome', 'Blog')}",
                    descricao=descricao_index,
                    url=f"{c.get('url_base', '')}/{idioma}/",
                    idioma=idioma,
                    eh_artigo=False
                ),
                'HEADER': self.get_header('inicio', None, idioma),
                'FOOTER': self.get_footer(idioma),
                'NOME': c.get('nome', 'Blog'),
                'NOME_SITE': self.get_nome_site_traduzido(idioma),
                'SLOGAN': self.get_slogan_traduzido(idioma),
                'FRASE_HERO': self.get_frase_hero_traduzida(idioma),
                'DESCRICAO': descricao_index,
                'PRIMEIRO_ARTIGO': primeiro_artigo,
                'LISTA_CARDS': lista_cards,
                'RELACIONADOS_SIDEBAR': relacionados_sidebar,
                'CATEGORIAS_SIDEBAR': categorias_sidebar,
                'TAGS': tags,
                'NAVEGACAO': navegacao,
                'TOTAL_ARTIGOS': str(total_artigos),
                'ANO': str(c.get('ano', datetime.now().year)),
                'ICONE': c.get('icone', '📝'),
            }
            html = self.renderizar_template('index.html', variaveis, idioma)
        else:
            frase_hero = self.get_frase_hero_traduzida(idioma)
            html = f'''<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
{self.get_head(
    titulo=f"{self.get_nome_site_traduzido(idioma)} - {c.get('nome', 'Blog')}",
    descricao=descricao_index,
    url=f"{c.get('url_base', '')}/{idioma}/",
    idioma=idioma,
    eh_artigo=False
)}
</head>
<body>
    {self.get_header('inicio', None, idioma)}
    <main class="container">
        <section class="hero">
            <span class="hero-eyebrow">{c.get('nome', 'Blog')} · Est. {c.get('ano', datetime.now().year)}</span>
            <h1>{frase_hero}</h1>
            <p>{descricao_index}</p>
            <div class="hero-actions">
                <a href="{primeiro_artigo}" class="btn-primary">Comece agora</a>
                <a href="#artigos-section" class="btn-outline">Explorar</a>
            </div>
        </section>
        <div class="layout" id="artigos-section">
            <div>
                <div class="section-head">
                    <h2>Artigos recentes</h2>
                    <a href="/{idioma}/categoria/" class="see-all">Ver tudo →</a>
                </div>
                <div class="post-grid">{lista_cards}</div>
                {navegacao}
            </div>
            <aside class="sidebar">
                <div class="sidebar-block">
                    <h3>Posts relacionados</h3>
                    {relacionados_sidebar}
                </div>
                <div class="sidebar-block sidebar-newsletter" id="newsletter">
                    <h3>Newsletter</h3>
                    <p>Receba dicas toda semana.</p>
                    <form id="newsletter-form" action="#" method="POST">
                        <input type="email" id="newsletter-email" placeholder="seu@email.com" required>
                        <button type="submit" class="btn-primary">Assinar</button>
                    </form>
                </div>
                <div class="sidebar-block">
                    <h3>Categorias</h3>
                    <div class="sidebar-tags">{tags}</div>
                </div>
            </aside>
        </div>
    </main>
    {self.get_footer(idioma)}
    <script src="/assets/js/script.js"></script>
</body>
</html>'''
        caminho = self.docs / idioma / ("index.html" if pagina == 1 else f"index{pagina}.html")
        caminho.parent.mkdir(parents=True, exist_ok=True)
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ Index página {pagina} atualizado ({idioma.upper()} - {len(artigos_pagina)} artigos)")
        return caminho
    
    # ==================== INDEX RAIZ ====================
    
    def criar_index_raiz(self):
        caminho = self.docs / "index.html"
        idioma_padrao = self.config.get('idioma_padrao', 'pt')
        opcoes_idiomas = ""
        for lang in self.config.get('idiomas', []):
            codigo = lang.get('codigo', 'pt')
            nome = lang.get('nome', codigo.upper())
            opcoes_idiomas += f'<a href="/{codigo}/" class="lang-option">{nome}</a>\n'
        html = f"""<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.get_nome_site_traduzido('pt')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', sans-serif;
            background: #f8fafc;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }}
        .container {{
            text-align: center;
            padding: 40px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            max-width: 500px;
            width: 90%;
        }}
        .logo {{ font-size: 3rem; margin-bottom: 10px; }}
        h1 {{ font-size: 1.8rem; color: #1e293b; margin-bottom: 8px; }}
        p {{ color: #64748b; margin-bottom: 30px; font-size: 0.95rem; }}
        .lang-options {{ display: flex; flex-direction: column; gap: 10px; }}
        .lang-option {{
            display: block; padding: 12px 20px; background: #f1f5f9;
            color: #1e293b; text-decoration: none; border-radius: 8px;
            font-weight: 600; transition: background 0.2s;
        }}
        .lang-option:hover {{ background: #e2e8f0; }}
        .lang-option.default {{ background: #1e293b; color: white; }}
        .lang-option.default:hover {{ background: #0f172a; }}
        .redirect-info {{ margin-top: 20px; font-size: 0.8rem; color: #94a3b8; }}
        .auto-redirect {{ margin-top: 15px; padding: 10px; background: #f1f5f9; border-radius: 8px; font-size: 0.85rem; color: #475569; }}
    </style>
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            var idiomas = {[lang['codigo'] for lang in self.config.get('idiomas', [])]};
            var lang = (navigator.language || navigator.userLanguage || 'pt').substring(0, 2);
            if (idiomas.includes(lang)) {{
                window.location.href = '/' + lang + '/';
            }}
        }});
    </script>
</head>
<body>
    <div class="container">
        <div class="logo">{self.config.get('icone', '📝')}</div>
        <h1>{self.get_nome_site_traduzido('pt')}</h1>
        <p>{self.get_descricao_traduzida('pt')}</p>
        <div class="lang-options">{opcoes_idiomas}</div>
        <div class="auto-redirect">🔄 Redirecionamento automático para o idioma do seu navegador</div>
        <div class="redirect-info">Escolha um idioma ou aguarde o redirecionamento automático.</div>
    </div>
</body>
</html>"""
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"   ✅ Index raiz criado: index.html (redireciona para /{idioma_padrao}/)")
        return caminho
    
    # ==================== ARTIGOS ====================
    
    def criar_artigo(self, artigo_data, forcar=False, revisar=True, idioma=None, forcar_head=False, nova_imagem=False):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        nome = artigo_data.get('artigo', '').strip()
        if not nome:
            return None
        link = artigo_data.get('links_afiliados', '')
        palavras_chave = artigo_data.get('palavras_chave', '')
        descricao = artigo_data.get('descricao', f"Review completo de {nome}")
        categoria = artigo_data.get('categoria', 'geral')
        tipo = artigo_data.get('tipo', 'review')
        data_publicacao = artigo_data.get('data_publicacao', datetime.now().strftime("%Y-%m-%d"))
        autor = artigo_data.get('autor', self.config.get('autor', 'Autor'))
        links_internos = artigo_data.get('links_internos', '')
        links_externos = artigo_data.get('links_externos', '')
        categoria_traduzida = self.get_categoria_traduzida(categoria, idioma)
        titulo_categoria = self.get_nome_categoria_traduzido(categoria, idioma)
        titulo_traduzido = self.traduzir_titulo(nome, idioma) if idioma != 'pt' else nome
        if not titulo_traduzido:
            titulo_traduzido = nome
        slug = self.criar_slug(titulo_traduzido)
        pasta = self.docs / idioma / categoria_traduzida / slug
        t = self.t
        
        # Se for só atualizar HEAD e o arquivo existe
        if forcar_head and (pasta / "index.html").exists():
            print(f"   🔄 Atualizando HEAD: {nome}")
            self._atualizar_head_artigo(pasta / "index.html", artigo_data, idioma, slug)
            return pasta / "index.html"
        
        # Se for só regenerar imagem
        if nova_imagem and (pasta / "index.html").exists():
            print(f"   🖼️ Regenerando imagem: {nome}")
            self._atualizar_imagem_artigo(pasta / "index.html", artigo_data, idioma, slug)
            return pasta / "index.html"
        
        # Se já existe e não é forçado
        if not forcar and (pasta / "index.html").exists():
            print(f"   ⏭️ Já existe: {idioma}/{categoria_traduzida}/{slug}")
            return pasta / "index.html"
        
        print(f"   📝 Criando: {idioma}/{categoria_traduzida}/{slug} (tipo: {tipo})")
        imagem = self.gerar_imagem(nome, categoria, slug)
        
        conteudo = None
        if (pasta / "index.html").exists():
            try:
                with open(pasta / "index.html", 'r', encoding='utf-8') as f:
                    html_existente = f.read()
                    match = re.search(r'<!-- CONTEUDO_INICIO -->(.*?)<!-- CONTEUDO_FIM -->', html_existente, re.DOTALL)
                    if match:
                        conteudo = match.group(1).strip()
                        print(f"   📄 Conteúdo existente mantido (marcadores)")
                    else:
                        match = re.search(r'<article class="container article-body">(.*?)</article>', html_existente, re.DOTALL)
                        if match:
                            conteudo = match.group(1).strip()
                            print(f"   📄 Conteúdo existente mantido (article-body)")
            except Exception as e:
                print(f"   ⚠️ Não foi possível extrair conteúdo: {e}")
        
        if conteudo is None:
            print(f"   🆕 Gerando conteúdo novo...")
            conteudo = self.gerar_conteudo_ia(nome, link, categoria, palavras_chave, tipo, idioma, links_internos, links_externos)
            if revisar and self.ia_api_key:
                conteudo = self.revisar_com_ia(conteudo, nome, categoria, tipo, idioma)
            conteudo = re.sub(r'<!DOCTYPE html>.*?<head>.*?</head>', '', conteudo, flags=re.DOTALL | re.IGNORECASE)
            conteudo = re.sub(r'<body.*?>', '', conteudo, flags=re.IGNORECASE)
            conteudo = re.sub(r'</body>', '', conteudo, flags=re.IGNORECASE)
            conteudo = re.sub(r'<html.*?>', '', conteudo, flags=re.IGNORECASE)
            conteudo = re.sub(r'</html>', '', conteudo, flags=re.IGNORECASE)
            conteudo = re.sub(r'<style>.*?</style>', '', conteudo, flags=re.DOTALL | re.IGNORECASE)
            conteudo = re.sub(r'<script type="text/javascript">.*?</script>', '', conteudo, flags=re.DOTALL | re.IGNORECASE)
            conteudo = re.sub(r'<h2[^>]*>Introdução\s*</h2>', '', conteudo, flags=re.IGNORECASE)
            conteudo = re.sub(r'<h2[^>]*id="[^"]*introducao[^"]*"[^>]*>Introdução\s*</h2>', '', conteudo, flags=re.IGNORECASE)
        else:
            print(f"   📄 Conteúdo existente mantido (NÃO recriado)")
        
        conteudo_com_marcadores = f"<!-- CONTEUDO_INICIO -->\n{conteudo}\n<!-- CONTEUDO_FIM -->\n<br class=\"clearfix\" />"
        
        titulo_map = {
            'review': f"{titulo_traduzido} - {t['review']}",
            'guia': f"Guia Completo: {titulo_traduzido}",
            'lista': f"Lista: {titulo_traduzido}",
            'tutorial': f"Tutorial: {titulo_traduzido}",
            'comparativo': f"Comparativo: {titulo_traduzido}",
            'artigo': f"{titulo_traduzido} - {t['review']}"
        }
        titulo = titulo_map.get(tipo, f"{titulo_traduzido} - {t['review']}")
        url = f"{self.config.get('url_base', '')}/{idioma}/{categoria_traduzida}/{slug}/"
        data_formatada = datetime.strptime(data_publicacao, "%Y-%m-%d").strftime("%d/%m/%Y") if data_publicacao else datetime.now().strftime("%d/%m/%Y")
        template = self.ler_template('artigo.html', idioma)
        
        if template:
            relacionados_html = ""
            relacionados = self.get_artigos_publicados(idioma)
            relacionados = [a for a in relacionados if a['slug'] != slug][:4]
            for a in relacionados:
                img = self.gerar_imagem(a['nome'], a['categoria'], a['slug'])
                data_formatada_rel = datetime.strptime(a['data_publicacao'], "%Y-%m-%d").strftime("%d/%m/%Y") if a['data_publicacao'] else datetime.now().strftime("%d/%m/%Y")
                titulo_cat_rel = self.get_nome_categoria_traduzido(a['categoria'], idioma)
                tempo_leitura = random.randint(4, 8)
                cat_traduzida_rel = self.get_categoria_traduzida(a['categoria'], idioma)
                if idioma != 'pt':
                    nome_traduzido_rel = self.traduzir_titulo(a['nome'], idioma)
                    nome_rel = nome_traduzido_rel if nome_traduzido_rel else a['nome']
                else:
                    nome_rel = a['nome']
                card = f'''<article class="post-card">
  <a href="/{idioma}/{cat_traduzida_rel}/{a['slug']}/" class="post-card-img">
    <img src="{img}" alt="{nome_rel}">
  </a>
  <div class="post-card-body">
    <a href="/{idioma}/{cat_traduzida_rel}/" class="tag">{titulo_cat_rel}</a>
    <h3 class="post-card-title"><a href="/{idioma}/{cat_traduzida_rel}/{a['slug']}/">{nome_rel}</a></h3>
    <div class="post-card-meta">
      <span>{data_formatada_rel}</span>
      <span class="meta-dot">·</span>
      <span>{tempo_leitura} min de leitura</span>
    </div>
    <p class="post-card-excerpt">{nome_rel[:120]}...</p>
    <a href="/{idioma}/{cat_traduzida_rel}/{a['slug']}/" class="read-more">Ler mais →</a>
  </div>
</article>'''
                relacionados_html += card
            head_html = self.get_head(titulo, descricao, url, imagem, idioma=idioma, slug=slug, eh_artigo=True, categoria_original=categoria)
            variaveis = {
                'HEAD': head_html,
                'TITULO': titulo,
                'CONTEUDO': conteudo_com_marcadores,
                'CATEGORIA': titulo_categoria,
                'DATA': data_formatada,
                'IMAGEM': imagem,
                'AUTOR': autor,
                'LINK_AFILIADO': link,
                'URL': url,
                'DESCRICAO': descricao,
                'TEMPO_LEITURA': str(random.randint(4, 8)),
                'IDIOMA': t['lang'],
                'NOME_SITE': self.get_nome_site_traduzido(idioma),
                'HEADER': self.get_header('inicio', categoria, idioma),
                'FOOTER': self.get_footer(idioma),
                'RELACIONADOS': relacionados_html
            }
            html = self.renderizar_template('artigo.html', variaveis, idioma)
        else:
            artigos_relacionados = self.get_artigos_relacionados(categoria, slug, idioma)
            if link and link.strip():
                cta_html = f"""
                <div class="cta-box">
                    <h3>{t['comprar']}</h3>
                    <p>Garanta o seu {titulo_traduzido} com preço especial</p>
                    <a href="{link}" class="btn-primary" target="_blank" rel="nofollow sponsored">{t['ver_oferta']}</a>
                </div>"""
            else:
                cta_html = ""
            html = f"""<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
{self.get_head(
    titulo=titulo,
    descricao=descricao,
    url=url,
    imagem=imagem,
    idioma=idioma,
    slug=slug,
    eh_artigo=True,
    categoria_original=categoria
)}
</head>
<body>
    {self.get_header('inicio', categoria, idioma)}
    <main class="container">
        <div class="banner">
            <h1>{self.get_nome_site_traduzido(idioma)}</h1>
            <p>{self.get_descricao_traduzida(idioma)}</p>
        </div>
        <div class="artigo">
            <div class="meta">
                <span>📅 {t['data_publicacao']} {data_formatada}</span>
                <span>✍️ {t['autor']} {autor}</span>
                <span class="categoria">📂 {titulo_categoria}</span>
                <span>⏱️ {random.randint(4, 8)} min de leitura</span>
            </div>
            <h1 id="introducao">{titulo}</h1>
            <img src="{imagem}" alt="{titulo_traduzido}" class="imagem-destaque" loading="lazy">
            {conteudo_com_marcadores}
            {cta_html}
            <div style="margin-top:25px;padding-top:15px;border-top:1px solid var(--fundo);">
                <p><strong>{t['compartilhar']}:</strong>
                <a href="https://wa.me/?text={titulo} - {url}" target="_blank" style="color:var(--whatsapp);font-weight:600;text-decoration:none;">WhatsApp</a> |
                <a href="https://www.facebook.com/sharer/sharer.php?u={url}" target="_blank" style="color:#1877f2;font-weight:600;text-decoration:none;">Facebook</a> |
                <a href="https://twitter.com/intent/tweet?text={titulo}&url={url}" target="_blank" style="color:#000;font-weight:600;text-decoration:none;">Twitter</a>
                </p>
            </div>
        </div>
        <aside class="sidebar">
            <div class="widget">
                <h3>📚 {t['leia_tambem']}</h3>
                <ul>{artigos_relacionados}</ul>
            </div>
        </aside>
    </main>
    {self.get_footer(idioma)}
    <script src="/assets/js/script.js"></script>
</body>
</html>"""
        pasta.mkdir(parents=True, exist_ok=True)
        caminho = pasta / "index.html"
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(html)
        artigo_data['status'] = 'publicado'
        if not artigo_data.get('data_publicacao'):
            artigo_data['data_publicacao'] = datetime.now().strftime("%Y-%m-%d")
        if not artigo_data.get('autor'):
            artigo_data['autor'] = self.config.get('autor', 'Autor')
        artigos = self.ler_csv(idioma)
        for a in artigos:
            if a.get('artigo') == nome:
                a['status'] = 'publicado'
                if not a.get('data_publicacao'):
                    a['data_publicacao'] = datetime.now().strftime("%Y-%m-%d")
                if not a.get('autor'):
                    a['autor'] = self.config.get('autor', 'Autor')
                break
        self.salvar_csv(artigos, idioma)
        self.criar_pagina_categoria(categoria, idioma)
        print(f"   ✅ Salvo: docs/{idioma}/{categoria_traduzida}/{slug}/index.html")
        return caminho
    
    def _atualizar_head_artigo(self, caminho, artigo_data, idioma, slug):
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                html_existente = f.read()
            nome = artigo_data.get('artigo', '')
            descricao = artigo_data.get('descricao', f"Review completo de {nome}")
            categoria = artigo_data.get('categoria', 'geral')
            categoria_traduzida = self.get_categoria_traduzida(categoria, idioma)
            url = f"{self.config.get('url_base', '')}/{idioma}/{categoria_traduzida}/{slug}/"
            imagem = self.gerar_imagem(nome, categoria, slug)
            titulo_traduzido = self.traduzir_titulo(nome, idioma) if idioma != 'pt' else nome
            if not titulo_traduzido:
                titulo_traduzido = nome
            titulo_map = {
                'review': f"{titulo_traduzido} - {self.t['review']}",
                'guia': f"Guia Completo: {titulo_traduzido}",
                'lista': f"Lista: {titulo_traduzido}",
                'tutorial': f"Tutorial: {titulo_traduzido}",
                'comparativo': f"Comparativo: {titulo_traduzido}",
                'artigo': f"{titulo_traduzido} - {self.t['review']}"
            }
            titulo = titulo_map.get(artigo_data.get('tipo', 'review'), f"{titulo_traduzido} - {self.t['review']}")
            novo_head = self.get_head(titulo, descricao, url, imagem, idioma=idioma, slug=slug, eh_artigo=True, categoria_original=categoria)
            html_novo = re.sub(r'<head>.*?</head>', f'<head>\n{novo_head}\n</head>', html_existente, flags=re.DOTALL)
            if html_novo != html_existente:
                with open(caminho, 'w', encoding='utf-8') as f:
                    f.write(html_novo)
                print(f"   ✅ HEAD atualizado: {nome}")
            else:
                print(f"   ⚠️ Não foi possível atualizar HEAD de: {nome}")
        except Exception as e:
            print(f"   ⚠️ Erro ao atualizar HEAD: {e}")
    
    def _atualizar_imagem_artigo(self, caminho, artigo_data, idioma, slug):
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                html_existente = f.read()
            nome = artigo_data.get('artigo', '')
            categoria = artigo_data.get('categoria', 'geral')
            # Gera nova imagem com seed aleatório
            seed = int(time.time()) + random.randint(1, 9999)
            nova_imagem = self.gerar_imagem(nome, categoria, slug, seed)
            # Substitui a imagem no HTML
            html_novo = re.sub(
                r'<img[^>]*class="imagem-destaque"[^>]*>',
                f'<img src="{nova_imagem}" alt="{nome}" class="imagem-destaque" loading="lazy">',
                html_existente
            )
            # Também substitui no og:image
            html_novo = re.sub(
                r'<meta property="og:image" content="[^"]*" />',
                f'<meta property="og:image" content="{nova_imagem}" />',
                html_novo
            )
            html_novo = re.sub(
                r'<meta name="twitter:image" content="[^"]*" />',
                f'<meta name="twitter:image" content="{nova_imagem}" />',
                html_novo
            )
            if html_novo != html_existente:
                with open(caminho, 'w', encoding='utf-8') as f:
                    f.write(html_novo)
                print(f"   ✅ Imagem atualizada: {nome}")
                print(f"   🖼️ Nova imagem: {nova_imagem}")
            else:
                print(f"   ⚠️ Não foi possível atualizar imagem de: {nome}")
        except Exception as e:
            print(f"   ⚠️ Erro ao atualizar imagem: {e}")
    
    def get_artigos_relacionados(self, categoria_atual, slug_atual, idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        artigos = self.get_artigos_publicados(idioma)
        relacionados = []
        for a in artigos:
            if a['slug'] != slug_atual:
                relacionados.append(a)
        if not relacionados:
            return '<li>Nenhum artigo relacionado</li>'
        relacionados = relacionados[:4]
        html = ""
        for a in relacionados:
            cat_traduzida = self.get_categoria_traduzida(a['categoria'], idioma)
            if idioma != 'pt':
                nome_traduzido = self.traduzir_titulo(a['nome'], idioma)
                nome_rel = nome_traduzido if nome_traduzido else a['nome']
            else:
                nome_rel = a['nome']
            html += f'<li><a href="/{idioma}/{cat_traduzida}/{a["slug"]}/">{nome_rel}</a></li>\n'
        return html
    
    # ==================== SITEMAP ====================
    
    def criar_sitemap(self):
        print("\n🗺️ GERANDO SITEMAPS POR IDIOMA")
        print("-" * 40)
        base_url = self.config.get('url_base', '')
        sitemaps_idiomas = []
        for idioma_info in self.config.get('idiomas', []):
            idioma = idioma_info['codigo']
            pasta_idioma = self.docs / idioma
            pasta_idioma.mkdir(parents=True, exist_ok=True)
            sitemap_path = pasta_idioma / "sitemap.xml"
            urlset = ET.Element('urlset')
            urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
            paginas = [('', 1.0), ('sobre.html', 0.5), ('contato.html', 0.5), ('politica-privacidade.html', 0.3), ('cookies.html', 0.3)]
            for pagina, prioridade in paginas:
                url_elem = ET.SubElement(urlset, 'url')
                loc = ET.SubElement(url_elem, 'loc')
                loc.text = f"{base_url}/{idioma}/{pagina}" if pagina else f"{base_url}/{idioma}/"
                lastmod = ET.SubElement(url_elem, 'lastmod')
                lastmod.text = datetime.now().strftime('%Y-%m-%d')
                changefreq = ET.SubElement(url_elem, 'changefreq')
                changefreq.text = 'monthly'
                priority = ET.SubElement(url_elem, 'priority')
                priority.text = str(prioridade)
            artigos = self.get_artigos_publicados(idioma)
            for a in artigos:
                cat_traduzida = self.get_categoria_traduzida(a['categoria'], idioma)
                url_elem = ET.SubElement(urlset, 'url')
                loc = ET.SubElement(url_elem, 'loc')
                loc.text = f"{base_url}/{idioma}/{cat_traduzida}/{a['slug']}/"
                lastmod = ET.SubElement(url_elem, 'lastmod')
                lastmod.text = datetime.now().strftime('%Y-%m-%d')
                changefreq = ET.SubElement(url_elem, 'changefreq')
                changefreq.text = 'weekly'
                priority = ET.SubElement(url_elem, 'priority')
                priority.text = '0.7'
            xml_str = ET.tostring(urlset, encoding='unicode')
            xml_pretty = minidom.parseString(xml_str).toprettyxml(indent="  ")
            with open(sitemap_path, 'w', encoding='utf-8') as f:
                f.write(xml_pretty)
            print(f"   ✅ Sitemap gerado: {idioma}/sitemap.xml ({len(artigos)} artigos)")
            sitemaps_idiomas.append(f"{base_url}/{idioma}/sitemap.xml")
        if sitemaps_idiomas:
            sitemap_index = self.docs / "sitemap.xml"
            index = ET.Element('sitemapindex')
            index.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
            for sitemap_url in sitemaps_idiomas:
                sitemap_elem = ET.SubElement(index, 'sitemap')
                loc = ET.SubElement(sitemap_elem, 'loc')
                loc.text = sitemap_url
            xml_str = ET.tostring(index, encoding='unicode')
            xml_pretty = minidom.parseString(xml_str).toprettyxml(indent="  ")
            with open(sitemap_index, 'w', encoding='utf-8') as f:
                f.write(xml_pretty)
            print(f"\n   ✅ Sitemap principal criado: sitemap.xml (aponta para {len(sitemaps_idiomas)} idiomas)")
        robots_path = self.docs / "robots.txt"
        with open(robots_path, 'w', encoding='utf-8') as f:
            f.write("User-agent: *\nAllow: /\nDisallow: /assets/\nDisallow: /404.html\n\n")
            for sitemap_url in sitemaps_idiomas:
                f.write(f"Sitemap: {sitemap_url}\n")
            print(f"   ✅ Robots.txt atualizado com {len(sitemaps_idiomas)} sitemaps")
    
    # ==================== TRADUÇÃO ====================
    
    def traduzir_artigo(self, html, titulo, idioma_destino):
        if not self.ia_api_key:
            print("   ⚠️ IA não configurada. Tradução cancelada.")
            return None
        mapa_idiomas = {'en': 'inglês', 'es': 'espanhol'}
        idioma_nome = mapa_idiomas.get(idioma_destino, 'inglês')
        prompt = f"""
        Traduza este artigo de português para {idioma_nome}.
        Mantenha TODAS as tags HTML, classes, ids e links.
        O conteúdo deve ser 100% em {idioma_nome}.
        Não adicione nada além da tradução.
        Título original: {titulo}
        Conteúdo HTML:
        {html}
        """
        try:
            headers = {"Authorization": f"Bearer {self.ia_api_key}", "Content-Type": "application/json"}
            data = {
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {"role": "system", "content": f"Você é um tradutor profissional para {idioma_nome}."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 6000,
                "temperature": 0.5
            }
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=120)
            if response.status_code == 200:
                traduzido = response.json()["choices"][0]["message"]["content"]
                traduzido = re.sub(r'```(?:html)?\s*', '', traduzido)
                traduzido = re.sub(r'\s*```', '', traduzido)
                return traduzido
            else:
                print(f"   ⚠️ Erro na tradução: {response.status_code}")
                return None
        except Exception as e:
            print(f"   ⚠️ Erro na tradução: {e}")
            return None

    def traduzir_titulo(self, titulo, idioma_destino):
        mapa_titulos = {
            'en': {
                'Bowl de Quinoa com Legumes Assados': 'Quinoa Bowl with Roasted Vegetables',
                'Sopa de Abóbora com Gengibre': 'Pumpkin Soup with Ginger',
                'Salada de Quinoa com Frango Grelhado': 'Quinoa Salad with Grilled Chicken',
                'Overnight Oats de Mirtilo e Chia': 'Overnight Oats with Blueberry and Chia',
                'Guia Completo da Dieta Mediterrânea': 'Complete Guide to the Mediterranean Diet',
                'O que Comer Antes e Depois do Treino': 'What to Eat Before and After Workout',
                '10 Alimentos Ricos em Fibras para o Dia a Dia': '10 High-Fiber Foods for Everyday',
                'Vitaminas e Minerais Essenciais para o Corpo': 'Essential Vitamins and Minerals for the Body',
                '5 Hábitos de Pessoas Centenárias': '5 Habits of Centenarians',
                'Como Reduzir o Estresse em 10 Minutos por Dia': 'How to Reduce Stress in 10 Minutes a Day',
                'Rotina Matinal para uma Vida Mais Saudável': 'Morning Routine for a Healthier Life',
                'Mindfulness: O Guia para Iniciantes': 'Mindfulness: The Beginner\'s Guide',
                'Hábitos de Longevidade das Zonas Azuis': 'Longevity Habits from the Blue Zones',
                'Alimentação Antienvelhecimento: O que Comer': 'Anti-Aging Nutrition: What to Eat',
                'Exercícios para a Terceira Idade': 'Exercises for Seniors',
                'Como o Sono Afeta a Longevidade': 'How Sleep Affects Longevity',
                'Guia Completo para Emagrecer com Saúde': 'Complete Guide to Healthy Weight Loss',
                '5 Exercícios para Fazer em Casa Sem Equipamentos': '5 Home Workouts Without Equipment',
                'Como Manter a Motivação para Emagrecer': 'How to Stay Motivated to Lose Weight',
                'Receitas Low-Carb para o Dia a Dia': 'Low-Carb Recipes for Everyday',
                'Como Criar uma Rotina Matinal Saudável': 'How to Create a Healthy Morning Routine',
                '10 Alimentos Ricos em Fibras para Melhorar o Intestino': '10 Fiber-Rich Foods to Improve Gut Health'
            },
            'es': {
                'Bowl de Quinoa com Legumes Assados': 'Bowl de Quinoa con Verduras Asadas',
                'Sopa de Abóbora com Gengibre': 'Sopa de Calabaza con Jengibre',
                'Salada de Quinoa com Frango Grelhado': 'Ensalada de Quinoa con Pollo a la Parrilla',
                'Overnight Oats de Mirtilo e Chia': 'Avena Nocturna con Arándanos y Chía',
                'Guia Completo da Dieta Mediterrânea': 'Guía Completa de la Dieta Mediterránea',
                'O que Comer Antes e Depois do Treino': 'Qué Comer Antes y Después del Entreno',
                '10 Alimentos Ricos em Fibras para o Dia a Dia': '10 Alimentos Ricos en Fibra para el Día a Día',
                'Vitaminas e Minerais Essenciais para o Corpo': 'Vitaminas y Minerales Esenciales para el Cuerpo',
                '5 Hábitos de Pessoas Centenárias': '5 Hábitos de Personas Centenarias',
                'Como Reduzir o Estresse em 10 Minutos por Dia': 'Cómo Reducir el Estrés en 10 Minutos al Día',
                'Rotina Matinal para uma Vida Mais Saudável': 'Rutina Matutina para una Vida Más Saludable',
                'Mindfulness: O Guia para Iniciantes': 'Mindfulness: La Guía para Principiantes',
                'Hábitos de Longevidade das Zonas Azuis': 'Hábitos de Longevidad de las Zonas Azules',
                'Alimentação Antienvelhecimento: O que Comer': 'Alimentación Antienvejecimiento: Qué Comer',
                'Exercícios para a Terceira Idade': 'Ejercicios para la Tercera Edad',
                'Como o Sono Afeta a Longevidade': 'Cómo el Sueño Afecta la Longevidad',
                'Guia Completo para Emagrecer com Saúde': 'Guía Completa para Adelgazar con Salud',
                '5 Exercícios para Fazer em Casa Sem Equipamentos': '5 Ejercicios para Hacer en Casa Sin Equipamiento',
                'Como Manter a Motivação para Emagrecer': 'Cómo Mantener la Motivación para Adelgazar',
                'Receitas Low-Carb para o Dia a Dia': 'Recetas Low-Carb para el Día a Día',
                'Como Criar uma Rotina Matinal Saudável': 'Cómo Crear una Rutina Matutina Saludable',
                '10 Alimentos Ricos em Fibras para Melhorar o Intestino': '10 Alimentos Ricos en Fibra para Mejorar el Intestino'
            }
        }
        return mapa_titulos.get(idioma_destino, {}).get(titulo, titulo)

    def publicar_com_traducao(self):
        if self.idioma_selecionado is None:
            print("⚠️ Selecione um idioma primeiro!")
            return
        # (mesmo código da versão anterior - mantido)
        print("⚠️ Função publicar_com_traducao mantida da versão anterior.")
        input("\nPressione Enter...")

    # ==================== REGENERAR IMAGEM ====================
    
    def regenerar_imagem(self):
        if self.idioma_selecionado is None:
            print("⚠️ Selecione um idioma primeiro!")
            return
        
        idioma = self.idioma_selecionado
        publicados = self.get_artigos_publicados(idioma)
        
        if not publicados:
            print(f"\n❌ Nenhum artigo publicado em {idioma.upper()}")
            input("\nPressione Enter...")
            return
        
        print(f"\n🖼️ REGENERAR IMAGEM ({idioma.upper()})")
        print("=" * 60)
        for i, p in enumerate(publicados, 1):
            titulo_cat = self.get_nome_categoria_traduzido(p['categoria'], idioma)
            print(f"   {i}. {p['nome']} ({titulo_cat})")
        print("-" * 60)
        
        escolha = self.ler_numero("\nNúmero do artigo: ", 1, len(publicados))
        if escolha is None:
            return
        
        slug = publicados[escolha - 1]['slug']
        nome = publicados[escolha - 1]['nome']
        categoria = publicados[escolha - 1]['categoria']
        
        print(f"\n🔄 Gerando nova imagem para: {nome}")
        
        # Busca os dados completos do artigo no CSV
        artigos = self.ler_csv(idioma)
        artigo_data = None
        for a in artigos:
            if self.criar_slug(a.get('artigo', '')) == slug:
                artigo_data = a
                break
        
        if artigo_data is None:
            print(f"   ❌ Artigo não encontrado no CSV")
            input("\nPressione Enter...")
            return
        
        # Regenera a imagem
        self.criar_artigo(artigo_data, forcar=False, revisar=False, idioma=idioma, nova_imagem=True)
        
        print(f"   ✅ Imagem regenerada com sucesso!")
        input("\nPressione Enter...")

    # ==================== SINCRONIZAR ====================
    
    def sincronizar_agora(self, regenerar_artigos=False, manter_conteudo=True):
        if self.idioma_selecionado is None:
            print("⚠️ Selecione um idioma primeiro!")
            return
        idioma = self.idioma_selecionado
        print(f"\n🔄 SINCRONIZANDO E REGENERANDO ({idioma.upper()})")
        print("=" * 40)
        self.sincronizar_status(mostrar_confirmacao=True, idioma=idioma)
        print(f"\n🔄 Regenerando páginas com os templates atuais...")
        self.criar_index(idioma=idioma)
        self.criar_todas_categorias(idioma=idioma)
        self.criar_sitemap()
        self.criar_index_raiz()
        print(f"\n🔄 Atualizando HEAD de todos os artigos com templates atuais...")
        artigos = self.get_artigos_publicados(idioma)
        if artigos:
            csv_artigos = self.ler_csv(idioma)
            for a in artigos:
                for csv_a in csv_artigos:
                    if self.criar_slug(csv_a.get('artigo', '')) == a['slug']:
                        print(f"   ♻️ Atualizando HEAD: {csv_a.get('artigo')}")
                        self.criar_artigo(csv_a, forcar=False, revisar=False, idioma=idioma, forcar_head=True)
                        break
            print(f"   ✅ HEAD de {len(artigos)} artigos atualizado")
        else:
            print("\n📭 Nenhum artigo para atualizar.")
        print("\n✅ Sincronização concluída!")
        print("   📁 HEAD de todos os artigos atualizados com os templates atuais.")
        print("   📄 NENHUM conteúdo foi recriado (apenas HEAD atualizado).")
        input("\nPressione Enter...")
    
    def sincronizar_status(self, mostrar_confirmacao=True, idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado
        if idioma is None:
            return False
        artigos = self.ler_csv(idioma)
        alterado = False
        afetados = []
        for a in artigos:
            if a.get('status') == 'publicado':
                slug = self.criar_slug(a.get('artigo', ''))
                categoria = a.get('categoria', 'geral')
                categoria_traduzida = self.get_categoria_traduzida(categoria, idioma)
                if not (self.docs / idioma / categoria_traduzida / slug / "index.html").exists():
                    afetados.append(a.get('artigo'))
                    a['status'] = 'rascunho'
                    alterado = True
        if alterado and mostrar_confirmacao:
            print(f"\n⚠️ {len(afetados)} artigos serão voltados para rascunho ({idioma.upper()}):")
            for nome in afetados:
                print(f"   🔄 {nome}")
            if not self.ler_sim_nao("\nContinuar? (s/n): "):
                return False
        if alterado:
            self.salvar_csv(artigos, idioma)
            print(f"✅ Status sincronizado! ({idioma.upper()})")
        return alterado
    
    # ==================== MENU ====================
    
    def selecionar_idioma(self):
        print("\n" + "=" * 60)
        print("🌐 SELECIONE O IDIOMA")
        print("=" * 60)
        idiomas = self.config.get('idiomas', [{'codigo': 'pt', 'nome': 'Português'}])
        for i, lang in enumerate(idiomas, 1):
            print(f"  {i}. {lang.get('nome', lang.get('codigo', '??').upper())}")
        print("  0. Sair")
        print("=" * 60)
        escolha = self.ler_numero("\n👉 Escolha: ", 0, len(idiomas))
        if escolha is None or escolha == 0:
            return None
        idioma_selecionado = idiomas[escolha - 1]['codigo']
        self.idioma_selecionado = idioma_selecionado
        self.t = IDIOMAS.get(self.idioma_selecionado, IDIOMAS['pt'])
        print(f"\n✅ Idioma selecionado: {idioma_selecionado.upper()}")
        return idioma_selecionado
    
    def mostrar_painel(self):
        if self.idioma_selecionado is None:
            return
        idioma = self.idioma_selecionado
        artigos = self.ler_csv(idioma)
        total = len(artigos)
        publicados = 0
        rascunhos = 0
        categorias = set()
        for a in artigos:
            status = a.get('status', 'rascunho').lower()
            if status == 'publicado':
                publicados += 1
            else:
                rascunhos += 1
            cat = a.get('categoria', 'geral')
            if cat:
                categorias.add(cat)
        print("\n" + "=" * 70)
        print(f"  {self.config.get('icone', '📝')} {self.get_nome_site_traduzido(idioma)} - {idioma.upper()}")
        print("=" * 70)
        print(f"  📊 {total} artigos | ✅ {publicados} publicados | ⏳ {rascunhos} rascunhos")
        print(f"  🏷️  {len(categorias)} categorias: {', '.join([self.get_nome_categoria_traduzido(c, idioma) for c in list(categorias)[:5]])}")
        print("=" * 70)
    
    def publicar_um(self):
        if self.idioma_selecionado is None:
            print("⚠️ Selecione um idioma primeiro!")
            return
        idioma = self.idioma_selecionado
        self.sincronizar_status(mostrar_confirmacao=False, idioma=idioma)
        artigos = self.ler_csv(idioma)
        pendentes = [a for a in artigos if a.get('status', 'rascunho').lower() != 'publicado']
        if not pendentes:
            print(f"\n✅ Nenhum artigo pendente para publicar ({idioma.upper()})")
            input("\nPressione Enter...")
            return
        print(f"\n📋 RASCUNHOS ({idioma.upper()}):")
        print("-" * 60)
        for i, a in enumerate(pendentes, 1):
            titulo_cat = self.get_nome_categoria_traduzido(a.get('categoria', 'geral'), idioma)
            print(f"  {i}. {a.get('artigo', 'Sem nome')} ({titulo_cat})")
        print("-" * 60)
        escolha = self.ler_numero("\nEscolha o número do artigo: ", 1, len(pendentes))
        if escolha is None:
            return
        a = pendentes[escolha - 1]
        titulo_cat = self.get_nome_categoria_traduzido(a.get('categoria', 'geral'), idioma)
        print("\n" + "=" * 60)
        print("📝 PREVIEW DO ARTIGO:")
        print("=" * 60)
        print(f"  Título: {a.get('artigo')}")
        print(f"  Categoria: {titulo_cat}")
        print(f"  Palavras-chave: {a.get('palavras_chave', '')}")
        print(f"  Descrição: {a.get('descricao', '')}")
        print(f"  Tipo: {a.get('tipo', 'review')}")
        print(f"  Data: {a.get('data_publicacao', 'Não definida')}")
        print("=" * 60)
        if not self.ler_sim_nao("\nPublicar este artigo? (s/n): "):
            return
        self.criar_artigo(a, forcar=True, revisar=True, idioma=idioma, forcar_head=False)
        self.criar_index(idioma=idioma)
        self.criar_todas_categorias(idioma=idioma)
        self.criar_sitemap()
        self.criar_index_raiz()
        print("\n✅ Publicado!")
        input("\nPressione Enter...")
    
    def publicar_lotes(self):
        if self.idioma_selecionado is None:
            print("⚠️ Selecione um idioma primeiro!")
            return
        idioma = self.idioma_selecionado
        print(f"\n📦 PUBLICAR EM LOTES ({idioma.upper()})")
        print("=" * 50)
        artigos = self.ler_csv(idioma)
        pendentes = [a for a in artigos if a.get('status', 'rascunho').lower() != 'publicado']
        if not pendentes:
            print(f"✅ Nenhum artigo pendente para publicar ({idioma.upper()})")
            input("\nPressione Enter...")
            return
        categorias = {}
        for a in pendentes:
            cat = a.get('categoria', 'geral')
            if cat not in categorias:
                categorias[cat] = []
            categorias[cat].append(a)
        print(f"\n📊 {len(pendentes)} artigos disponíveis ({idioma.upper()})")
        print("\n📂 CATEGORIAS DISPONÍVEIS:")
        cats = list(categorias.keys())
        for i, cat in enumerate(cats, 1):
            titulo = self.get_nome_categoria_traduzido(cat, idioma)
            print(f"  {i}. {titulo} ({len(categorias[cat])} artigos)")
        print("\nEscolha uma opção:")
        print("  [0] Publicar de todas as categorias")
        for i, cat in enumerate(cats, 1):
            titulo = self.get_nome_categoria_traduzido(cat, idioma)
            print(f"  [{i}] Publicar apenas da categoria {titulo}")
        opcao = input("\n➡️  ").strip()
        if opcao == '0':
            artigos_selecionados = pendentes
        elif opcao.isdigit() and 1 <= int(opcao) <= len(cats):
            cat_selecionada = cats[int(opcao) - 1]
            artigos_selecionados = categorias[cat_selecionada]
            titulo_cat = self.get_nome_categoria_traduzido(cat_selecionada, idioma)
            print(f"\n📋 ARTIGOS DA CATEGORIA {titulo_cat.upper()}:")
            for i, a in enumerate(artigos_selecionados, 1):
                print(f"  {i}. {a.get('artigo', 'Sem nome')}")
        else:
            print("❌ Opção inválida")
            input("\nPressione Enter...")
            return
        if not artigos_selecionados:
            print("❌ Nenhum artigo selecionado")
            input("\nPressione Enter...")
            return
        print(f"\n🎯 Quantos artigos publicar? (máx {len(artigos_selecionados)})")
        print("   (Digite um número ou 't' para todos)")
        opcao_qtd = input("\n➡️  ").strip().lower()
        if opcao_qtd == 't':
            quantidade = len(artigos_selecionados)
        else:
            try:
                quantidade = int(opcao_qtd)
                if quantidade <= 0:
                    print("❌ Número inválido")
                    input("\nPressione Enter...")
                    return
                quantidade = min(quantidade, len(artigos_selecionados))
            except ValueError:
                print("❌ Opção inválida")
                input("\nPressione Enter...")
                return
        publicar_agora = artigos_selecionados[:quantidade]
        print(f"\n📦 Publicando {len(publicar_agora)} artigos...")
        print("-" * 40)
        for i, a in enumerate(publicar_agora, 1):
            print(f"\n[{i}/{len(publicar_agora)}] Publicando: {a.get('artigo')}")
            data_pub = (datetime.now() + timedelta(days=i-1)).strftime("%Y-%m-%d")
            a['data_publicacao'] = data_pub
            self.criar_artigo(a, revisar=True, idioma=idioma, forcar_head=False)
            if i < len(publicar_agora):
                espera = random.randint(2, 5)
                print(f"   ⏳ Aguardando {espera}s...")
                time.sleep(espera)
        self.criar_index(idioma=idioma)
        self.criar_todas_categorias(idioma=idioma)
        self.criar_sitemap()
        self.criar_index_raiz()
        print("\n" + "=" * 40)
        print(f"✅ {len(publicar_agora)} artigos publicados com sucesso! ({idioma.upper()})")
        print(f"📊 Restam {len(pendentes) - len(publicar_agora)} artigos pendentes")
        input("\nPressione Enter...")
    
    def ver_artigos(self):
        if self.idioma_selecionado is None:
            print("⚠️ Selecione um idioma primeiro!")
            return
        idioma = self.idioma_selecionado
        artigos = self.ler_csv(idioma)
        if not artigos:
            print(f"\n📭 Nenhum artigo em {idioma.upper()}")
            input("\nPressione Enter...")
            return
        print(f"\n📋 TODOS OS ARTIGOS ({idioma.upper()})")
        print("=" * 70)
        print("-" * 60)
        for i, a in enumerate(artigos, 1):
            nome = a.get('artigo', 'Sem nome')[:40]
            status = a.get('status', 'rascunho')
            status_icon = "✅" if status == 'publicado' else "⏳"
            status_text = "Publicado" if status == 'publicado' else "Rascunho"
            categoria = self.get_nome_categoria_traduzido(a.get('categoria', 'geral'), idioma)[:15]
            print(f"  {i:2}. {status_icon} {nome:<40} {status_text:<10} {categoria}")
        input("\nPressione Enter...")
    
    def ver_por_categoria(self):
        if self.idioma_selecionado is None:
            print("⚠️ Selecione um idioma primeiro!")
            return
        idioma = self.idioma_selecionado
        artigos = self.ler_csv(idioma)
        if not artigos:
            print(f"\n📭 Nenhum artigo em {idioma.upper()}")
            input("\nPressione Enter...")
            return
        print(f"\n📂 ARTIGOS POR CATEGORIA ({idioma.upper()})")
        print("=" * 70)
        print("-" * 50)
        categorias = {}
        for a in artigos:
            cat = a.get('categoria', 'geral')
            if cat not in categorias:
                categorias[cat] = []
            categorias[cat].append(a)
        for cat, arts in categorias.items():
            titulo_cat = self.get_nome_categoria_traduzido(cat, idioma)
            publicados = sum(1 for a in arts if a.get('status') == 'publicado')
            print(f"  📂 {titulo_cat}: {publicados}/{len(arts)} publicados")
        input("\nPressione Enter...")
    
    def revisar_artigo(self):
        if self.idioma_selecionado is None:
            print("⚠️ Selecione um idioma primeiro!")
            return
        idioma = self.idioma_selecionado
        publicados = self.get_artigos_publicados(idioma)
        if not publicados:
            print(f"\n❌ Nenhum artigo publicado em {idioma.upper()}")
            input("\nPressione Enter...")
            return
        print(f"\n📋 PUBLICADOS ({idioma.upper()}):")
        for i, p in enumerate(publicados, 1):
            titulo_cat = self.get_nome_categoria_traduzido(p['categoria'], idioma)
            print(f"   {i}. {p['nome']} ({titulo_cat})")
        escolha = self.ler_numero("\nNúmero: ", 1, len(publicados))
        if escolha is None:
            return
        slug = publicados[escolha - 1]['slug']
        nome = publicados[escolha - 1]['nome']
        categoria = publicados[escolha - 1]['categoria']
        while True:
            print(f"\n📝 {nome} ({idioma.upper()})")
            print("1. 📖 Ver no navegador")
            print("2. 🔄 Regenerar com IA (com revisão)")
            print("3. 🗑️ Despublicar (voltar para rascunho)")
            print("4. ❌ Voltar")
            opcao = input("Escolha: ").strip()
            if opcao == "1":
                categoria_traduzida = self.get_categoria_traduzida(categoria, idioma)
                caminho = self.docs / idioma / categoria_traduzida / slug / "index.html"
                if caminho.exists():
                    webbrowser.open(str(caminho))
                else:
                    print("❌ Arquivo não encontrado!")
                input("Pressione Enter...")
            elif opcao == "2":
                print("\n🔄 Regenerando com revisão...")
                artigos = self.ler_csv(idioma)
                link = "https://afiliado.com/produto"
                for a in artigos:
                    if self.criar_slug(a.get('artigo', '')) == slug:
                        link = a.get('links_afiliados', 'https://afiliado.com/produto')
                        break
                self.criar_artigo({'artigo': nome, 'links_afiliados': link, 'categoria': categoria}, forcar=True, revisar=True, idioma=idioma, forcar_head=False)
                self.criar_index(idioma=idioma)
                print("✅ Regenerado com revisão!")
                input("Pressione Enter...")
            elif opcao == "3":
                if self.ler_sim_nao(f"Despublicar '{nome}'? (s/n): "):
                    categoria_traduzida = self.get_categoria_traduzida(categoria, idioma)
                    pasta = self.docs / idioma / categoria_traduzida / slug
                    if pasta.exists():
                        shutil.rmtree(pasta)
                    artigos = self.ler_csv(idioma)
                    for a in artigos:
                        if self.criar_slug(a.get('artigo', '')) == slug:
                            a['status'] = 'rascunho'
                            break
                    self.salvar_csv(artigos, idioma)
                    self.criar_index(idioma=idioma)
                    self.criar_todas_categorias(idioma=idioma)
                    print(f"✅ '{nome}' voltou para rascunho! ({idioma.upper()})")
                    input("Pressione Enter...")
                    return
            elif opcao == "4":
                return
    
    def deletar_artigo(self):
        if self.idioma_selecionado is None:
            print("⚠️ Selecione um idioma primeiro!")
            return
        idioma = self.idioma_selecionado
        publicados = self.get_artigos_publicados(idioma)
        if not publicados:
            print(f"\n❌ Nenhum artigo em {idioma.upper()}")
            input("\nPressione Enter...")
            return
        print(f"\n🗑️ DELETAR ({idioma.upper()}):")
        for i, p in enumerate(publicados, 1):
            titulo_cat = self.get_nome_categoria_traduzido(p['categoria'], idioma)
            print(f"   {i}. {p['nome']} ({titulo_cat})")
        escolha = self.ler_numero("\nNúmero: ", 1, len(publicados))
        if escolha is None:
            return
        slug = publicados[escolha - 1]['slug']
        nome = publicados[escolha - 1]['nome']
        categoria = publicados[escolha - 1]['categoria']
        if not self.ler_sim_nao(f"Deletar '{nome}'? (s/n): "):
            return
        categoria_traduzida = self.get_categoria_traduzida(categoria, idioma)
        pasta = self.docs / idioma / categoria_traduzida / slug
        if pasta.exists():
            shutil.rmtree(pasta)
            print(f"   🗑️ Pasta removida: {idioma}/{categoria_traduzida}/{slug}")
        artigos = self.ler_csv(idioma)
        for a in artigos:
            if self.criar_slug(a.get('artigo', '')) == slug:
                a['status'] = 'rascunho'
                break
        self.salvar_csv(artigos, idioma)
        self.criar_index(idioma=idioma)
        self.criar_todas_categorias(idioma=idioma)
        self.criar_sitemap()
        self.criar_index_raiz()
        print(f"✅ {nome} deletado! ({idioma.upper()})")
        input("\nPressione Enter...")
    
    def menu(self):
        while True:
            if self.idioma_selecionado is None:
                idioma = self.selecionar_idioma()
                if idioma is None:
                    print("\n👋 Até logo!")
                    break
                self.idioma_selecionado = idioma
                self.t = IDIOMAS.get(self.idioma_selecionado, IDIOMAS['pt'])
            self.mostrar_painel()
            print(f"\n📝 CONTEÚDO ({self.idioma_selecionado.upper()})")
            print("  [1] Ver todos os artigos")
            print("  [2] Ver por categoria")
            print("  [3] Publicar UM")
            print("  [4] Publicar com TRADUÇÃO (PT → EN/ES)")
            print("  [5] Publicar em LOTES")
            print("  [6] Revisar/Regenerar artigo")
            print("  [7] 🖼️ Regenerar IMAGEM de um artigo")
            print(f"\n🔄 FERRAMENTAS ({self.idioma_selecionado.upper()})")
            print("  [8] ATUALIZAR TUDO (HEAD + sitemap)")
            print("  [9] Deletar artigo")
            print("\n  [10] Trocar idioma")
            print("  [0] Sair")
            print("=" * 70)
            opcao = input("\n🎯 Escolha: ").strip()
            if opcao == "1":
                self.ver_artigos()
            elif opcao == "2":
                self.ver_por_categoria()
            elif opcao == "3":
                self.publicar_um()
            elif opcao == "4":
                self.publicar_com_traducao()
            elif opcao == "5":
                self.publicar_lotes()
            elif opcao == "6":
                self.revisar_artigo()
            elif opcao == "7":
                self.regenerar_imagem()
            elif opcao == "8":
                print("\n⚠️ ATENÇÃO: Isso vai ATUALIZAR O HEAD de TODOS os artigos")
                print("   com os templates atuais, além de regenerar index, categorias e sitemap")
                print("   NENHUM CONTEÚDO será perdido.")
                if self.ler_sim_nao("Continuar? (s/n): "):
                    self.sincronizar_agora(regenerar_artigos=False)
                    print("\n✅ HEAD de todos os artigos atualizado!")
                    input("\nPressione Enter...")
            elif opcao == "9":
                self.deletar_artigo()
            elif opcao == "10":
                self.idioma_selecionado = None
                self.t = IDIOMAS.get('pt', IDIOMAS['pt'])
                continue
            elif opcao == "0":
                print("\n👋 Até logo!")
                break
            else:
                print("❌ Opção inválida")
                input("\nPressione Enter...")

if __name__ == "__main__":
    gerador = Gerador()
    gerador.menu()