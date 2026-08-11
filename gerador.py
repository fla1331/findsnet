#!/usr/bin/env python3

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
import hashlib
from urllib.parse import quote

# ============================================================
# ===== CONFIGURAÇÕES PADRÃO ==================================
# ============================================================

CONFIG_PADRAO = {
    'nome': 'Finds',
    'slug': 'finds',
    'icone': '💎',
    'nicho': 'achadinhos',
    'nome_site': 'Finds',
    'tagline': 'Um lugar pra quem gosta de economizar.',
    'descricao': 'Ofertas, cupons e produtos que a gente usa e recomenda. Sem exagero.',
    'url_base': 'https://finds.brightnest.blog',
    'idioma_padrao': 'pt',
    'idiomas': [
        {'codigo': 'pt', 'nome': 'Português', 'pasta': 'pt', 'csv': 'artigos/artigos_pt.csv'},
        {'codigo': 'en', 'nome': 'English', 'pasta': 'en', 'csv': 'artigos/artigos_en.csv'},
        {'codigo': 'es', 'nome': 'Español', 'pasta': 'es', 'csv': 'artigos/artigos_es.csv'}
    ],
    'ano': datetime.now().year,
    'usar_ia_imagens': True,
    'usar_imagens_reais': True,
    'prioridade_imagens': 'reais',
    'pexels_api_key': '',
    'pixabay_api_key': '',
    'unsplash_api_key': '',
    'autor': 'Time Finds',
    'email_contato': 'contato@finds.brightnest.blog',
    'publicar_por_dia': 1,
    'redes_sociais': {
        'instagram': 'https://instagram.com/finds',
        'youtube': 'https://youtube.com/finds',
        'twitter': 'https://twitter.com/finds',
        'pinterest': 'https://pinterest.com/finds'
    },
    'cores': {
      'primaria': '#F59E0B',
      'secundaria': '#1E293B',
      'fundo': '#0F172A',
      'texto': '#F1F5F9',
      'card': '#1E293B',
      'card_hover': '#334155',
      'hover': '#FBBF24',
      'destaque': '#10B981',
      'destaque_negativo': '#EF4444',
      'whatsapp': '#25D366',
      'borda': '#334155',
      'subtitulo': '#94A3B8'
    },
    'imagem_padrao_pt': '/assets/img/og-default.jpg',
    'imagem_padrao_en': '/assets/img/og-default-en.jpg',
    'imagem_padrao_es': '/assets/img/og-default-es.jpg',
    'posts_por_pagina': 9,
    'frase_hero': 'Você também gosta de achar um bom desconto? Então tá no lugar certo.',
    'slogan': 'Finds. Achados que valem a pena.',
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
# ===== MAPA DE CATEGORIAS ===================================
# ============================================================

MAPA_CATEGORIAS = {
    # Ofertas e promoções
    'ofertas': {'en': 'offers', 'es': 'ofertas'},
    'promocoes': {'en': 'promotions', 'es': 'promociones'},
    'cupons': {'en': 'coupons', 'es': 'cupones'},
    'descontos': {'en': 'discounts', 'es': 'descuentos'},
    
    # Produtos por categoria
    'eletronicos': {'en': 'electronics', 'es': 'electronicos'},
    'informatica': {'en': 'computers', 'es': 'informatica'},
    'smartphones': {'en': 'smartphones', 'es': 'smartphones'},
    'tv-e-audio': {'en': 'tv-and-audio', 'es': 'tv-y-audio'},
    'games': {'en': 'games', 'es': 'juegos'},
    
    'casa-e-decoracao': {'en': 'home-and-decor', 'es': 'hogar-y-decoracion'},
    'cozinha': {'en': 'kitchen', 'es': 'cocina'},
    'moveis': {'en': 'furniture', 'es': 'muebles'},
    'jardim': {'en': 'garden', 'es': 'jardin'},
    
    'moda-e-acessorios': {'en': 'fashion-and-accessories', 'es': 'moda-y-accesorios'},
    'calcados': {'en': 'shoes', 'es': 'zapatos'},
    'relogios': {'en': 'watches', 'es': 'relojes'},
    'joias': {'en': 'jewelry', 'es': 'joyas'},
    
    'beleza-e-cuidados': {'en': 'beauty-and-care', 'es': 'belleza-y-cuidados'},
    'perfumes': {'en': 'perfumes', 'es': 'perfumes'},
    'maquiagem': {'en': 'makeup', 'es': 'maquillaje'},
    
    'livros': {'en': 'books', 'es': 'libros'},
    'papelaria': {'en': 'stationery', 'es': 'papeleria'},
    
    'brinquedos': {'en': 'toys', 'es': 'juguetes'},
    'infantil': {'en': 'kids', 'es': 'infantil'},
    
    'esportes': {'en': 'sports', 'es': 'deportes'},
    'academia': {'en': 'fitness', 'es': 'gimnasio'},
    'bicicletas': {'en': 'bicycles', 'es': 'bicicletas'},
    
    'automotivo': {'en': 'automotive', 'es': 'automotriz'},
    'pecas': {'en': 'parts', 'es': 'piezas'},
    
    # Serviços e assinaturas
    'streaming': {'en': 'streaming', 'es': 'streaming'},
    'cursos': {'en': 'courses', 'es': 'cursos'},
    'seguros': {'en': 'insurance', 'es': 'seguros'},
    'viagens': {'en': 'travel', 'es': 'viajes'},
    
    # Especiais
    'imperdivel': {'en': 'unmissable', 'es': 'imperdible'},
    'testamos': {'en': 'we-tested', 'es': 'probamos'},
    'comparativos': {'en': 'comparisons', 'es': 'comparativas'},
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
        
        self.nicho = self.config.get('nicho', 'viagem').lower()
        print(f"🎯 Nicho detectado: {self.nicho.upper()}")
        
        self.idioma_padrao = self.config.get('idioma_padrao', 'pt')
        self.idioma = self.idioma_padrao
        self.t = IDIOMAS.get(self.idioma, IDIOMAS['pt'])
        
        self.ia_api_key = os.getenv("OPENROUTER_API_KEY")
        
        self.idiomas_ativos = [idioma['codigo'] for idioma in self.config.get('idiomas', [{'codigo': 'pt'}])]
        
        self.criar_csv()
        self.criar_css()
        
        self.idioma_selecionado = None
        
        self.fonte_temporaria = None
        self._em_sincronizacao = False
        self._cache_traducoes = {}
    
    # ============================================================
    # 🔥 MÉTODOS DE NOME DO SITE COM TAGLINE
    # ============================================================
    
    def get_nome_site_traduzido(self, idioma):
        """Retorna o nome do site + tagline para o título"""
        nome = self.config.get('nome_site', 'Coin Wise')
        tagline = self.config.get('tagline', '')
        
        if tagline:
            return f"{nome} - {tagline}"
        return nome
    
    def get_nome_site_simples(self, idioma):
        """Retorna apenas o nome do site (sem tagline) - usado em menus, footer, etc"""
        return self.config.get('nome_site', 'Coin Wise')
    
    def get_tagline(self, idioma):
        """Retorna a tagline do site"""
        return self.config.get('tagline', '')
    
    # ============================================================
    # 🔥 MÉTODO PARA PEGAR DESCRIÇÃO DA CATEGORIA
    # ============================================================
    
    DESCRICOES_CATEGORIAS = {
        'pt': {
            'destinos': 'Descubra os melhores destinos do mundo. Lugares incríveis para sua próxima aventura.',
            'roteiros': 'Roteiros completos para você explorar cada destino. Dias, passeios e dicas imperdíveis.',
            'dicas-de-viagem': 'Dicas essenciais para viajar com segurança, economia e conforto.',
            'hoteis': 'Os melhores hotéis e hospedagens. Conforto, localização e preço para sua viagem.',
            'gastronomia': 'Sabores do mundo. Descubra a culinária local e os melhores restaurantes.',
            'aventura': 'Viagens de aventura. Esportes radicais, trilhas e experiências únicas.',
            'praias': 'As praias mais bonitas do mundo. Sol, mar e areia para relaxar.',
            'montanhas': 'Destinos de montanha. Paisagens, trilhas e natureza exuberante.',
            'cidades': 'Explorando as cidades do mundo. Cultura, arquitetura e vida urbana.',
            'ecoturismo': 'Ecoturismo e turismo sustentável. Viaje preservando a natureza.',
            'mochilao': 'Dicas para mochileiros. Viaje leve e economize sem perder o conforto.',
            'viagem-em-familia': 'Viagens em família. Diversão e conforto para todos os membros.',
            'viagem-sozinho': 'A liberdade de viajar sozinho. Dicas e destinos para explorar.',
            'viagem-de-casal': 'Viagens a dois. Destinos românticos e experiências inesquecíveis.',
            'cruzeiros': 'Cruzeiros marítimos. Luxo, lazer e destinos incríveis.',
            'road-trip': 'Road trips: viagens de carro, moto ou campervan. Liberdade sobre rodas.',
            'fotografia': 'Fotografia de viagem. Dicas para registrar suas aventuras.',
            'cultura': 'Cultura e tradições dos destinos. Festas, arte e história.',
            'natureza': 'Natureza exuberante. Destinos para se conectar com o meio ambiente.',
            'parques': 'Parques naturais e nacionais. Conservação e aventura.',
            'europa': 'A Europa dos sonhos. História, cultura e paisagens deslumbrantes.',
            'asia': 'A Ásia misteriosa e fascinante. Destinos exóticos e cultura milenar.',
            'africa': 'A África selvagem. Safáris, cultura e paisagens impressionantes.',
            'america-sul': 'Descubra a América do Sul. Paisagens, cidades e culturas únicas.',
            'america-norte': 'Explore a América do Norte. Grandes cidades e natureza selvagem.',
            'brasil': 'O Brasil é gigante. Descubra as belezas do nosso país.',
            'portugal': 'Portugal: história, sabor e paisagens encantadoras.',
            'espanha': 'Espanha: sol, cultura e gastronomia incríveis.',
            'italia': 'Itália: arte, história e a melhor gastronomia do mundo.',
            'franca': 'França: romance, cultura e paisagens de tirar o fôlego.',
        },
        'en': {
            'destinations': 'Discover the best destinations in the world. Amazing places for your next adventure.',
            'itineraries': 'Complete itineraries for you to explore each destination. Days, tours and unmissable tips.',
            'travel-tips': 'Essential tips for traveling safely, economically and comfortably.',
            'hotels': 'The best hotels and accommodations. Comfort, location and price for your trip.',
            'gastronomy': 'Flavors of the world. Discover local cuisine and the best restaurants.',
            'adventure': 'Adventure travel. Extreme sports, trails and unique experiences.',
            'beaches': 'The most beautiful beaches in the world. Sun, sea and sand to relax.',
            'mountains': 'Mountain destinations. Landscapes, trails and lush nature.',
            'cities': 'Exploring the cities of the world. Culture, architecture and urban life.',
            'ecotourism': 'Ecotourism and sustainable tourism. Travel while preserving nature.',
            'backpacking': 'Backpacking tips. Travel light and save money without losing comfort.',
            'family-travel': 'Family trips. Fun and comfort for all members.',
            'solo-travel': 'The freedom of traveling alone. Tips and destinations to explore.',
            'couple-travel': 'Trips for two. Romantic destinations and unforgettable experiences.',
            'cruises': 'Cruises. Luxury, leisure and incredible destinations.',
            'road-trip': 'Road trips: car, motorcycle or campervan. Freedom on wheels.',
            'photography': 'Travel photography. Tips for capturing your adventures.',
            'culture': 'Culture and traditions of destinations. Festivals, art and history.',
            'nature': 'Lush nature. Destinations to connect with the environment.',
            'parks': 'Natural and national parks. Conservation and adventure.',
            'europe': 'Europe of dreams. History, culture and stunning landscapes.',
            'asia': 'Mysterious and fascinating Asia. Exotic destinations and ancient culture.',
            'africa': 'Wild Africa. Safaris, culture and impressive landscapes.',
            'south-america': 'Discover South America. Unique landscapes, cities and cultures.',
            'north-america': 'Explore North America. Big cities and wild nature.',
            'brazil': 'Brazil is giant. Discover the beauties of our country.',
            'portugal': 'Portugal: history, flavor and charming landscapes.',
            'spain': 'Spain: sun, culture and incredible gastronomy.',
            'italy': 'Italy: art, history and the best gastronomy in the world.',
            'france': 'France: romance, culture and breathtaking landscapes.',
        },
        'es': {
            'destinos': 'Descubre los mejores destinos del mundo. Lugares increíbles para tu próxima aventura.',
            'itinerarios': 'Itinerarios completos para explorar cada destino. Días, paseos y consejos imperdibles.',
            'consejos-de-viaje': 'Consejos esenciales para viajar con seguridad, economía y comodidad.',
            'hoteles': 'Los mejores hoteles y alojamientos. Confort, ubicación y precio para tu viaje.',
            'gastronomia': 'Sabores del mundo. Descubre la cocina local y los mejores restaurantes.',
            'aventura': 'Viajes de aventura. Deportes extremos, senderos y experiencias únicas.',
            'playas': 'Las playas más bonitas del mundo. Sol, mar y arena para relajarse.',
            'montanas': 'Destinos de montaña. Paisajes, senderos y naturaleza exuberante.',
            'ciudades': 'Explorando las ciudades del mundo. Cultura, arquitectura y vida urbana.',
            'ecoturismo': 'Ecoturismo y turismo sostenible. Viaja preservando la naturaleza.',
            'mochilero': 'Consejos para mochileros. Viaja ligero y ahorra sin perder comodidad.',
            'viaje-en-familia': 'Viajes en familia. Diversión y confort para todos los miembros.',
            'viaje-solo': 'La libertad de viajar solo. Consejos y destinos para explorar.',
            'viaje-en-pareja': 'Viajes para dos. Destinos románticos y experiencias inolvidables.',
            'cruceros': 'Cruceros marítimos. Lujo, ocio y destinos increíbles.',
            'road-trip': 'Road trips: viajes en coche, moto o campervan. Libertad sobre ruedas.',
            'fotografia': 'Fotografía de viaje. Consejos para registrar tus aventuras.',
            'cultura': 'Cultura y tradiciones de los destinos. Fiestas, arte e historia.',
            'naturaleza': 'Naturaleza exuberante. Destinos para conectar con el medio ambiente.',
            'parques': 'Parques naturales y nacionales. Conservación y aventura.',
            'europa': 'La Europa de los sueños. Historia, cultura y paisajes deslumbrantes.',
            'asia': 'La Asia misteriosa y fascinante. Destinos exóticos y cultura milenaria.',
            'africa': 'La África salvaje. Safaris, cultura y paisajes impresionantes.',
            'america-del-sur': 'Descubre América del Sur. Paisajes, ciudades y culturas únicas.',
            'america-del-norte': 'Explora América del Norte. Grandes ciudades y naturaleza salvaje.',
            'brasil': 'Brasil es gigante. Descubre las bellezas de nuestro país.',
            'portugal': 'Portugal: historia, sabor y paisajes encantadores.',
            'espana': 'España: sol, cultura y gastronomía increíble.',
            'italia': 'Italia: arte, historia y la mejor gastronomía del mundo.',
            'francia': 'Francia: romance, cultura y paisajes de ensueño.',
        }
    }
    
    def get_descricao_categoria(self, categoria, idioma):
        """Pega a descrição personalizada da categoria ou usa fallback genérico"""
        if idioma in self.DESCRICOES_CATEGORIAS:
            if categoria in self.DESCRICOES_CATEGORIAS[idioma]:
                return self.DESCRICOES_CATEGORIAS[idioma][categoria]
        
        titulo = self.get_nome_categoria_traduzido(categoria, idioma)
        return f'Artigos sobre {titulo} - {self.get_nome_site_simples(idioma)}'
    
    # ==================== CONFIG ====================
    
    def carregar_config(self):
        config_path = self.base / "config.json"
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    # Adiciona campos novos se não existirem
                    for chave, valor in CONFIG_PADRAO.items():
                        if chave not in dados:
                            dados[chave] = valor
                    print(f"✅ Config carregada: config.json ({dados.get('nome_site', 'Blog')})")
                    return dados
            except Exception as e:
                print(f"⚠️ Erro ao ler config.json: {e}")
                return CONFIG_PADRAO
        else:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(CONFIG_PADRAO, f, indent=2, ensure_ascii=False)
            print("✅ config.json criado com configurações padrão")
            return CONFIG_PADRAO
    
    # ==================== UTILITÁRIOS ====================
    
    def _parse_data_segura(self, data_str):
        if not data_str or not isinstance(data_str, str):
            return datetime.now()
        
        data_str = data_str.strip()
        data_str = re.sub(r'[^0-9/\-]', '', data_str)
        
        if not data_str:
            return datetime.now()
        
        formatos = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d %H:%M:%S"]
        
        for fmt in formatos:
            try:
                return datetime.strptime(data_str, fmt)
            except (ValueError, TypeError):
                continue
        
        print(f"   ⚠️ Data inválida: '{data_str}', usando data atual")
        return datetime.now()
    
    def _is_valid_date(self, date_str):
        if not date_str or not isinstance(date_str, str):
            return False
        
        date_str = date_str.strip()
        date_str = re.sub(r'[^0-9/\-]', '', date_str)
        
        if not date_str:
            return False
        
        formatos = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d %H:%M:%S"]
        
        for fmt in formatos:
            try:
                datetime.strptime(date_str, fmt)
                return True
            except (ValueError, TypeError):
                continue
        
        return False
    
    def ler_artigo_html(self, caminho):
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                html = f.read()
            
            titulo = "Título não encontrado"
            match = re.search(r'<h1[^>]*class="[^"]*article-title[^"]*"[^>]*>(.*?)</h1>', html, re.DOTALL)
            if match:
                titulo = re.sub(r'<[^>]+>', '', match.group(1)).strip()
            
            if titulo == "Título não encontrado":
                match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
                if match:
                    titulo = re.sub(r'<[^>]+>', '', match.group(1)).strip()
            
            if titulo == "Título não encontrado":
                match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
                if match:
                    titulo = re.sub(r'<[^>]+>', '', match.group(1)).strip()
                    titulo = titulo.split(' - ')[0].split(' | ')[0].strip()
            
            match_desc = re.search(r'<meta name="description" content="([^"]+)"', html)
            descricao = match_desc.group(1).strip() if match_desc else ""
            
            texto = re.sub(r'<[^>]+>', ' ', html)
            texto = re.sub(r'\s+', ' ', texto).strip()[:500]
            
            return titulo, descricao, texto
        except Exception as e:
            print(f"   ⚠️ Erro ao ler {caminho}: {e}")
            return "Erro ao ler", "", ""
    
    # ==================== CATEGORIAS ====================
    
    def get_categorias_do_idioma(self, idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        
        categorias_pt = []
        pasta_pt = self.docs / 'pt'
        if pasta_pt.exists():
            for cat_dir in pasta_pt.iterdir():
                if cat_dir.is_dir() and cat_dir.name not in ['assets', 'netlify']:
                    tem_artigos = False
                    for artigo_dir in cat_dir.iterdir():
                        if artigo_dir.is_dir() and (artigo_dir / "index.html").exists():
                            tem_artigos = True
                            break
                    if tem_artigos:
                        categorias_pt.append(cat_dir.name)
        
        categorias_traduzidas = []
        for cat_pt in categorias_pt:
            if idioma == 'pt':
                categorias_traduzidas.append(cat_pt)
            else:
                cat_trad = MAPA_CATEGORIAS.get(cat_pt, {}).get(idioma, cat_pt)
                categorias_traduzidas.append(cat_trad)
        
        return sorted(categorias_traduzidas)
    
    def get_categorias_das_pastas(self, idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        
        pasta_idioma = self.docs / idioma
        categorias = set()
        
        if not pasta_idioma.exists():
            return []
        
        for categoria_dir in pasta_idioma.iterdir():
            if not categoria_dir.is_dir():
                continue
            if categoria_dir.name in ['assets', 'netlify']:
                continue
            
            tem_artigos = False
            for artigo_dir in categoria_dir.iterdir():
                if artigo_dir.is_dir() and (artigo_dir / "index.html").exists():
                    tem_artigos = True
                    break
            
            if tem_artigos:
                categorias.add(categoria_dir.name)
        
        return sorted(list(categorias))
    
    def get_categorias(self, idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        return self.get_categorias_do_idioma(idioma)
    
    def get_categoria_traduzida(self, categoria, idioma):
        if idioma == 'pt':
            return categoria
        
        if self._em_sincronizacao:
            return categoria
        
        if categoria in MAPA_CATEGORIAS:
            return MAPA_CATEGORIAS[categoria].get(idioma, categoria)
        
        from unidecode import unidecode
        slug = categoria.lower()
        slug = unidecode(slug)
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'[\s]+', '-', slug)
        slug = re.sub(r'[-]+', '-', slug)
        return slug.strip('-')[:60]
    
    def get_nome_categoria_traduzido(self, categoria, idioma):
        if idioma == 'pt':
            palavras = categoria.replace('-', ' ').split()
            palavras_formatadas = []
            for palavra in palavras:
                if palavra.lower() in ['de', 'da', 'do', 'das', 'dos', 'e']:
                    palavras_formatadas.append(palavra.lower())
                else:
                    palavras_formatadas.append(palavra.capitalize())
            return ' '.join(palavras_formatadas)
        
        return self.get_categoria_traduzida(categoria, idioma).replace('-', ' ').title()
    
    # ==================== TRADUÇÃO ====================
    
    def traduzir_titulo(self, titulo, idioma_destino):
        if self._em_sincronizacao:
            return titulo
        
        if idioma_destino == 'pt' or not titulo:
            return titulo
        
        cache_key = f"{titulo}_{idioma_destino}"
        if cache_key in self._cache_traducoes:
            return self._cache_traducoes[cache_key]
        
        if not self.ia_api_key:
            return titulo
        
        mapa_idiomas = {'en': 'inglês', 'es': 'espanhol'}
        idioma_nome = mapa_idiomas.get(idioma_destino, 'inglês')
        
        try:
            headers = {"Authorization": f"Bearer {self.ia_api_key}", "Content-Type": "application/json"}
            data = {
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {"role": "system", "content": f"Traduza para {idioma_nome}. Traduza apenas o texto."},
                    {"role": "user", "content": f"Traduza para {idioma_nome}: {titulo}"}
                ],
                "max_tokens": 200,
                "temperature": 0.3
            }
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            if response.status_code == 200:
                traduzido = response.json()["choices"][0]["message"]["content"].strip()
                self._cache_traducoes[cache_key] = traduzido
                return traduzido
            return titulo
        except Exception as e:
            return titulo

    def traduzir_palavras_chave(self, palavras, idioma_destino):
        if self._em_sincronizacao:
            return palavras
        
        if idioma_destino == 'pt' or not palavras:
            return palavras
        
        lista = [p.strip() for p in palavras.split(',')]
        
        if len(lista) <= 1:
            return self.traduzir_titulo(palavras, idioma_destino)
        
        traduzidas = []
        for p in lista:
            if p.strip():
                trad = self.traduzir_titulo(p.strip(), idioma_destino)
                traduzidas.append(trad if trad else p.strip())
        
        return ', '.join(traduzidas)

    def criar_registro_traduzido(self, artigo_pt, idioma_destino):
        titulo_pt = artigo_pt.get('artigo', '').strip()
        titulo_trad = self.traduzir_titulo(titulo_pt, idioma_destino) or titulo_pt
        categoria_pt = artigo_pt.get('categoria', 'geral')
        categoria_trad = self.get_categoria_traduzida(categoria_pt, idioma_destino)
        grupo = (artigo_pt.get('grupo') or '').strip() or (artigo_pt.get('slug') or '').strip() or self.criar_slug(titulo_pt)

        return {
            'artigo': titulo_trad,
            'slug': self.criar_slug(titulo_trad),
            'grupo': grupo,
            'links_afiliados': artigo_pt.get('links_afiliados', '#'),
            'status': 'publicado',
            'categoria': categoria_trad,
            'palavras_chave': self.traduzir_palavras_chave(artigo_pt.get('palavras_chave', ''), idioma_destino) or '',
            'descricao': self.traduzir_titulo(artigo_pt.get('descricao', ''), idioma_destino) or '',
            'tipo': artigo_pt.get('tipo', 'review'),
            'data_publicacao': datetime.now().strftime("%Y-%m-%d"),
            'autor': self.config.get('autor', 'Autor'),
            'links_internos': '',
            'links_externos': ''
        }
    
    # ==================== UTILITÁRIOS GERAIS ====================
    
    def get_descricao_traduzida(self, idioma):
        desc = self.config.get('descricao', '')
        if desc:
            return desc
        return 'Conteúdo interessante para você.'
    
    def get_frase_hero_traduzida(self, idioma):
        return self.config.get('frase_hero', 'Transforme sua rotina')
    
    def get_slogan_traduzido(self, idioma):
        return self.config.get('slogan', '')
    
    def formatar_titulo_categoria(self, slug):
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

    def _gravar_slug_no_csv(self, titulo_artigo, slug, idioma):
        try:
            artigos = self.ler_csv(idioma)
            mudou = False
            for a in artigos:
                if a.get('artigo') == titulo_artigo and not (a.get('slug') or '').strip():
                    a['slug'] = slug
                    mudou = True
            if mudou:
                self.salvar_csv(artigos, idioma)
        except Exception as e:
            print(f"   ⚠️ Não foi possível gravar slug no CSV: {e}")
    
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
            print(f"   ✅ Template encontrado: {caminho_idioma}")
            with open(caminho_idioma, 'r', encoding='utf-8') as f:
                return f.read()
        
        caminho_padrao = self.templates / nome
        if caminho_padrao.exists():
            print(f"   ⚠️ Template fallback: {caminho_padrao}")
            with open(caminho_padrao, 'r', encoding='utf-8') as f:
                return f.read()
        
        print(f"   ❌ Template não encontrado: {caminho_idioma}")
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
            csv_path = self.base / f'artigos/artigos_{idioma}.csv'
        
        if not csv_path.exists():
            return []
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            print(f"⚠️ Erro ao ler CSV {idioma}: {e}")
            return []
    
    def salvar_csv(self, artigos, idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao

        csv_path = None
        for lang in self.config.get('idiomas', []):
            if lang.get('codigo') == idioma:
                csv_path = self.base / lang.get('csv', f'artigos/artigos_{idioma}.csv')
                break

        if csv_path is None:
            csv_path = self.base / f'artigos/artigos_{idioma}.csv'

        if not artigos:
            return

        csv_path.parent.mkdir(parents=True, exist_ok=True)

        cabecalho = ["artigo", "slug", "grupo", "links_afiliados", "status", "categoria", "palavras_chave", "descricao", "tipo", "data_publicacao", "autor", "links_internos", "links_externos"]
        
        artigos_limpos = []
        for artigo in artigos:
            novo_artigo = {}

            slug_existente = (artigo.get('slug') or '').strip()
            if slug_existente:
                novo_artigo['slug'] = slug_existente
            else:
                novo_artigo['slug'] = self.criar_slug(artigo.get('artigo', ''))

            grupo_existente = (artigo.get('grupo') or '').strip()
            if grupo_existente:
                novo_artigo['grupo'] = grupo_existente
            else:
                novo_artigo['grupo'] = novo_artigo['slug']
            
            data = artigo.get('data_publicacao', '')
            if data:
                data_obj = self._parse_data_segura(data)
                novo_artigo['data_publicacao'] = data_obj.strftime("%Y-%m-%d")
            else:
                novo_artigo['data_publicacao'] = datetime.now().strftime("%Y-%m-%d")
            
            categoria = artigo.get('categoria', 'geral')
            if not categoria or categoria.strip() == '':
                categoria = 'geral'
            novo_artigo['categoria'] = categoria
            
            status = artigo.get('status', 'rascunho')
            if status not in ['publicado', 'rascunho']:
                status = 'rascunho'
            novo_artigo['status'] = status
            
            for chave in ['artigo', 'links_afiliados', 'palavras_chave', 'descricao', 'tipo', 'autor', 'links_internos', 'links_externos']:
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
                ["artigo", "slug", "grupo", "links_afiliados", "status", "categoria", "palavras_chave", "descricao", "tipo", "data_publicacao", "autor", "links_internos", "links_externos"],
                ["Guia: Destinos Incríveis", "guia-destinos-incriveis", "guia-destinos-incriveis", "#", "rascunho", "destinos", "destinos, viagem, turismo", "Guia completo para viajar", "guia", "", self.config.get('autor', 'Autor'), "", ""],
            ]
            
            with open(csv_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                writer.writerows(dados)
            print(f"✅ CSV criado: {csv_nome}")
    
    # ==================== CSS ====================
    
    def criar_css(self):
        css_destino = self.assets_css / "style.css"
        custom_destino = self.assets_css / "custom.css"
        
        if css_destino.exists():
            print("✅ style.css mantido (já existe)")
        else:
            c = self.config.get('cores', {})
            css = f"""
* {{ margin: 0; padding: 0; box-sizing: border-box; }}

:root {{
    --primaria: {c.get('primaria', '#0c2461')};
    --secundaria: {c.get('secundaria', '#f6b93b')};
    --destaque: {c.get('destaque', '#0c2461')};
    --fundo: {c.get('fundo', '#f8f9fa')};
    --texto: {c.get('texto', '#2d3436')};
    --card: {c.get('card', '#ffffff')};
    --hover: {c.get('hover', '#e58e26')};
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
"""
            with open(css_destino, 'w', encoding='utf-8') as f:
                f.write(css)
            print("✅ style.css criado")
        
        if custom_destino.exists():
            print("✅ custom.css mantido (já existe)")
        else:
            with open(custom_destino, 'w', encoding='utf-8') as f:
                f.write("/* Custom styles */\n")
            print("✅ custom.css criado (vazio)")
    
    # ==================== BUSCA DE IMAGENS ====================
    
    def _gerar_palavras_chave(self, tema, categoria):
        palavras_titulo = tema.lower().split()
        
        stopwords = ['como', 'para', 'o', 'a', 'os', 'as', 'de', 'da', 'do', 'das', 'dos', 
                     'em', 'por', 'com', 'sem', 'um', 'uma', 'uns', 'umas', 'e', 'ou', 'que',
                     'no', 'na', 'nos', 'nas', 'ao', 'aos', 'à', 'às']
        palavras_importantes = [p for p in palavras_titulo if p not in stopwords and len(p) > 2]
        
        palavras_chave = palavras_importantes[:5]
        
        nicho = self.nicho
        nicho_map = {
            'viagem': 'travel vacation destination tourism',
            'travel': 'travel vacation destination tourism',
            'destinos': 'travel destination tourism',
            'roteiros': 'itinerary travel route',
        }
        
        if nicho in nicho_map:
            palavras_chave.extend(nicho_map[nicho].split())
        
        palavras_chave = list(dict.fromkeys(palavras_chave))[:8]
        
        return ' '.join(palavras_chave)
    
    def _buscar_unsplash(self, keywords):
        try:
            api_key = os.getenv("UNSPLASH_API_KEY")
            if not api_key:
                return None
            
            query = quote(keywords)
            url = f"https://api.unsplash.com/photos/random?query={query}&orientation=landscape"
            
            headers = {
                "Authorization": f"Client-ID {api_key}",
                "User-Agent": "Mozilla/5.0"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data and 'urls' in data:
                    return data['urls']['regular']
            elif response.status_code == 403:
                pass
            elif response.status_code == 429:
                pass
                
        except Exception as e:
            pass
        
        return None
    
    def _buscar_pexels(self, keywords):
        try:
            api_key = os.getenv("PEXELS_API_KEY")
            if not api_key:
                return None
            
            query = quote(keywords)
            url = f"https://api.pexels.com/v1/search?query={query}&per_page=1&orientation=landscape"
            
            headers = {
                "Authorization": api_key,
                "User-Agent": "Mozilla/5.0"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data and 'photos' in data and len(data['photos']) > 0:
                    return data['photos'][0]['src']['large']
        except Exception as e:
            pass
        
        return None
    
    def _buscar_pixabay(self, keywords):
        try:
            api_key = os.getenv("PIXABAY_API_KEY")
            if not api_key:
                return None
            
            query = quote(keywords)
            url = f"https://pixabay.com/api/?key={api_key}&q={query}&image_type=photo&orientation=horizontal&per_page=1"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data and 'hits' in data and len(data['hits']) > 0:
                    return data['hits'][0]['largeImageURL']
        except Exception as e:
            pass
        
        return None
    
    def _buscar_google_images(self, keywords):
        try:
            query = quote(keywords)
            url = f"https://www.google.com/search?q={query}&tbm=isch"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                import re
                pattern = r'imgurl=([^&]+)'
                matches = re.findall(pattern, response.text)
                if matches:
                    return matches[0].replace('%3A', ':').replace('%2F', '/')
        except Exception as e:
            pass
        
        return None
    
    def buscar_imagem_real(self, tema, categoria="", fonte_especifica=None):
        if not self.config.get('usar_imagens_reais', True):
            return None
        
        keywords = self._gerar_palavras_chave(tema, categoria)
        
        fonte = fonte_especifica or getattr(self, 'fonte_temporaria', 'hibrido')
        
        fontes_disponiveis = {
            'unsplash': ("Unsplash", self._buscar_unsplash),
            'pexels': ("Pexels", self._buscar_pexels),
            'pixabay': ("Pixabay", self._buscar_pixabay),
        }
        
        if fonte in fontes_disponiveis and fonte != 'hibrido':
            nome_fonte, funcao_fonte = fontes_disponiveis[fonte]
            try:
                imagem = funcao_fonte(keywords)
                if imagem:
                    return imagem
            except Exception as e:
                pass
            return None
        
        fontes = [
            ("Unsplash", self._buscar_unsplash),
            ("Pexels", self._buscar_pexels),
            ("Pixabay", self._buscar_pixabay),
            ("Google Images", self._buscar_google_images)
        ]
        
        for nome_fonte, funcao_fonte in fontes:
            try:
                imagem = funcao_fonte(keywords)
                if imagem:
                    return imagem
            except Exception as e:
                continue
        
        return None
    
    # ==================== IMAGEM ====================
    
    def _gerar_descricao_visual(self, artigo, categoria):
        titulo_limpo = artigo[:80].strip()
        palavras = titulo_limpo.split()
        palavras_principais = ' '.join(palavras[:6])
        
        nicho_contexto = {
            # Geral
            'achadinhos': 'ofertas, promoções, descontos, cupons, produtos, compras, economia, achados',
            'finds': 'ofertas, promoções, descontos, cupons, produtos, compras, economia, achados',
            'ofertas': 'ofertas, promoções, descontos, liquidação, black friday, desconto, compras',
            'promocoes': 'promoções, ofertas, descontos, cupons, liquidação, black friday',
            'cupons': 'cupons, cupom de desconto, código promocional, ofertas, promoções',
            'descontos': 'descontos, ofertas, promoções, preço baixo, economia, barato',
            
            # Produtos
            'eletronicos': 'eletrônicos, celulares, computadores, fones de ouvido, smartwatch, tv, promoções',
            'informatica': 'computadores, notebooks, monitores, teclados, mouses, periféricos, ofertas',
            'smartphones': 'smartphones, celulares, iphone, samsung, xiaomi, motorola, ofertas',
            'tv-e-audio': 'televisão, tv, soundbar, fone de ouvido, caixa de som, home theater',
            'games': 'jogos, videogame, playstation, xbox, nintendo, pc gamer, acessórios',
            
            'casa-e-decoracao': 'casa, decoração, móveis, iluminação, tapete, cortina, organizador',
            'cozinha': 'cozinha, utensílios, panelas, facas, eletrodomésticos, geladeira, fogão',
            'moveis': 'móveis, sofá, cama, mesa, cadeira, estante, guarda-roupa',
            'jardim': 'jardim, plantas, vasos, ferramentas, paisagismo, decoração externa',
            
            'moda-e-acessorios': 'moda, roupas, acessórios, bolsas, cintos, boné, óculos, mochila',
            'calcados': 'sapatos, tênis, sandálias, botas, sapatênis, calçados',
            'relogios': 'relógios, smartwatch, relógio de pulso, relógio digital, acessórios',
            'joias': 'joias, bijuterias, colar, anel, brinco, pulseira, acessórios',
            
            'beleza-e-cuidados': 'beleza, cuidados pessoais, maquiagem, pele, cabelo, perfume, creme',
            'perfumes': 'perfumes, fragrância, colônia, desodorante, aromatizante',
            'maquiagem': 'maquiagem, base, batom, sombra, delineador, rímel',
            
            'livros': 'livros, e-books, kindle, literatura, romance, ficção, não-ficção',
            'papelaria': 'papelaria, caderno, caneta, lápis, agenda, estojo, material escolar',
            
            'brinquedos': 'brinquedos, brincadeiras, jogos, boneca, carrinho, lego, presente',
            'infantil': 'infantil, crianças, bebê, carrinho, cadeirinha, fralda, brinquedo',
            
            'esportes': 'esportes, academia, corrida, futebol, basquete, equipamentos',
            'academia': 'academia, musculação, suplemento, whey, creatina, halter, esteira',
            'bicicletas': 'bicicleta, bike, ciclismo, acessórios, capacete, segurança',
            
            'automotivo': 'carros, automotivo, peças, acessórios, pneus, óleo, manutenção',
            'pecas': 'peças automotivas, manutenção, filtro, pastilha, amortecedor, motor',
            
            # Serviços
            'streaming': 'streaming, netflix, spotify, amazon prime, disney+, hbo, assinatura',
            'cursos': 'cursos online, educação, aprendizado, ead, certificação, idiomas',
            'seguros': 'seguros, seguro de vida, seguro carro, seguro casa, proteção',
            'viagens': 'viagens, hotéis, passagens aéreas, pacotes, turismo, ofertas',
            
            # Especiais
            'imperdivel': 'imperdível, melhor oferta, promoção única, aproveite, destaque',
            'testamos': 'testamos, review, análise, experiência, opinião, recomendação',
            'comparativos': 'comparativo, comparação, vs, qual escolher, melhor preço',
        }
        
        contexto = nicho_contexto.get(self.nicho, 'viagens, paisagens, destinos turísticos, natureza, aventura')
        
        return f'"{titulo_limpo}", relacionado a {contexto}, fotografia realista, luz natural, composição equilibrada, qualidade profissional, sem pessoas'
    
    def _pegar_imagem_pt(self, slug):
        """Pega a imagem do artigo em PT pelo slug (nome da pasta) - PRIORIDADE"""
        pasta_pt = self.docs / 'pt'
        if not pasta_pt.exists():
            return None
        
        for categoria_dir in pasta_pt.iterdir():
            if not categoria_dir.is_dir():
                continue
            if categoria_dir.name in ['assets', 'netlify']:
                continue
            
            artigo_dir = categoria_dir / slug
            if artigo_dir.exists() and (artigo_dir / "index.html").exists():
                try:
                    with open(artigo_dir / "index.html", 'r', encoding='utf-8') as f:
                        html = f.read()
                    # Primeiro tenta pegar do article-cover
                    match = re.search(r'<div class="container article-cover">.*?<img[^>]*src="([^"]+)"[^>]*>.*?</div>', html, re.DOTALL)
                    if match:
                        return match.group(1)
                    # Depois tenta og:image
                    match = re.search(r'<meta property="og:image" content="([^"]+)"', html)
                    if match:
                        return match.group(1)
                except:
                    pass
        return None
    
    def _pegar_imagem_existente(self, slug, idioma):
        # PRIORIDADE: usa a imagem do PT (sincronização)
        imagem_pt = self._pegar_imagem_pt(slug)
        if imagem_pt:
            return imagem_pt
        
        # Se não encontrar em PT, tenta encontrar no idioma atual
        artigos = self.ler_csv(idioma)
        categoria = None
        for a in artigos:
            if a.get('status') != 'publicado':
                continue
            slug_a = (a.get('slug') or '').strip() or self.criar_slug(a.get('artigo', ''))
            if slug_a == slug:
                categoria = a.get('categoria', 'geral')
                break
        
        if categoria:
            categoria_traduzida = self.get_categoria_traduzida(categoria, idioma)
            caminho = self.docs / idioma / categoria_traduzida / slug / "index.html"
            
            if caminho.exists():
                try:
                    with open(caminho, 'r', encoding='utf-8') as f:
                        html = f.read()
                    
                    match = re.search(r'<div class="container article-cover">.*?<img[^>]*src="([^"]+)"[^>]*>.*?</div>', html, re.DOTALL)
                    if match:
                        return match.group(1)
                    
                    match = re.search(r'<meta property="og:image" content="([^"]+)"', html)
                    if match:
                        return match.group(1)
                except:
                    pass
        
        return None
    
    def _pegar_miniatura_atual(self, artigo_data, idioma):
        nome = artigo_data.get('artigo', '').strip()
        if not nome:
            return None
        
        slug = (artigo_data.get('slug') or '').strip() or self.criar_slug(nome)
        categoria = artigo_data.get('categoria', 'geral')
        categoria_traduzida = self.get_categoria_traduzida(categoria, idioma)
        
        caminho = self.docs / idioma / categoria_traduzida / slug / "index.html"
        
        if not caminho.exists():
            return None
        
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                html = f.read()
            
            match = re.search(r'<div class="container article-cover">.*?<img[^>]*src="([^"]+)"[^>]*>.*?</div>', html, re.DOTALL)
            if match:
                return match.group(1)
        except:
            pass
        
        return None
    
    def _pegar_imagem_interna_atual(self, artigo_data, idioma):
        nome = artigo_data.get('artigo', '').strip()
        if not nome:
            return None
        
        slug = (artigo_data.get('slug') or '').strip() or self.criar_slug(nome)
        categoria = artigo_data.get('categoria', 'geral')
        categoria_traduzida = self.get_categoria_traduzida(categoria, idioma)
        
        caminho = self.docs / idioma / categoria_traduzida / slug / "index.html"
        
        if not caminho.exists():
            return None
        
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                html = f.read()
            
            match = re.search(r'<article class="container article-body">.*?<img[^>]*src="([^"]*)"[^>]*>', html, re.DOTALL)
            if match:
                return match.group(1)
        except:
            pass
        
        return None
    
    def _aplicar_imagens(self, artigo_data, idioma, miniatura, interna):
        nome = artigo_data.get('artigo', '').strip()
        if not nome:
            return
        
        slug = (artigo_data.get('slug') or '').strip() or self.criar_slug(nome)
        categoria = artigo_data.get('categoria', 'geral')
        categoria_traduzida = self.get_categoria_traduzida(categoria, idioma)
        
        caminho = self.docs / idioma / categoria_traduzida / slug / "index.html"
        
        if not caminho.exists():
            return
        
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                html = f.read()
            
            if miniatura:
                html = re.sub(
                    r'<div class="container article-cover">.*?<img[^>]*src="[^"]*"[^>]*>.*?</div>',
                    f'<div class="container article-cover">\n            <img src="{miniatura}" alt="{nome}" loading="lazy" />\n        </div>',
                    html,
                    flags=re.DOTALL
                )
                html = re.sub(
                    r'<meta property="og:image" content="[^"]*" />',
                    f'<meta property="og:image" content="{miniatura}" />',
                    html
                )
                html = re.sub(
                    r'<meta name="twitter:image" content="[^"]*" />',
                    f'<meta name="twitter:image" content="{miniatura}" />',
                    html
                )
            
            if interna and interna != miniatura:
                match = re.search(r'<article class="container article-body">(.*?)</article>', html, re.DOTALL)
                if match:
                    corpo = match.group(1)
                    corpo = re.sub(
                        r'<img[^>]*src="[^"]*"[^>]*>',
                        f'<img src="{interna}" alt="{nome}" loading="lazy" />',
                        corpo,
                        count=1
                    )
                    html = html.replace(match.group(1), corpo)
            
            with open(caminho, 'w', encoding='utf-8') as f:
                f.write(html)
            
        except Exception as e:
            print(f"   ⚠️ Erro ao aplicar imagens: {e}")
    
    def gerar_imagem(self, artigo, categoria="", slug="", seed=None, forcar_nova=False, imagem_manual=None):
        timestamp = int(time.time() * 1000)
        
        if imagem_manual:
            return f"{imagem_manual}?t={timestamp}&cache={timestamp}"
        
        if self.config.get('usar_imagens_reais', True):
            imagem_real = self.buscar_imagem_real(artigo, categoria)
            
            if imagem_real:
                return f"{imagem_real}?t={timestamp}&cache={timestamp}"
        
        if self.config.get('usar_ia_imagens', True):
            try:
                if seed is None:
                    seed = int(time.time() * 1000) + random.randint(1, 999999)
                
                titulo_limpo = artigo[:60].strip()
                if len(titulo_limpo) < 10:
                    titulo_limpo = artigo
                
                desc_visual = self._gerar_descricao_visual(artigo, categoria)
                
                prompt = (
                    f"Fotografia realista de {titulo_limpo}, "
                    f"{desc_visual}, "
                    f"luz natural, estilo lifestyle, composição equilibrada, "
                    f"sem exageros, cores naturais, qualidade fotográfica"
                )
                
                prompt = ' '.join(prompt.split())
                
                unique_id = f"{slug}{seed}{timestamp}"
                
                url = (
                    f"https://image.pollinations.ai/prompt/{prompt}"
                    f"?width=1200&height=630&nologo=true"
                    f"&seed={unique_id}"
                    f"&_={timestamp}"
                    f"&cache={timestamp}"
                )
                
                if forcar_nova:
                    url += f"&force={timestamp + random.randint(1, 9999)}"
                
                return url
                
            except Exception as e:
                pass
        
        return f"https://picsum.photos/seed/{slug or 'default'}/1200/630?t={timestamp}&nocache={timestamp}"
    
    # ==================== UPLOAD MANUAL ====================
    
    def upload_imagem_manual(self):
        if self.idioma_selecionado is None:
            print("⚠️ Selecione um idioma primeiro!")
            return
        
        idioma = self.idioma_selecionado
        publicados = self.get_artigos_publicados(idioma)
        
        if not publicados:
            print(f"\n❌ Nenhum artigo publicado em {idioma.upper()}")
            input("\nPressione Enter...")
            return
        
        print(f"\n📋 ARTIGOS PUBLICADOS ({idioma.upper()})")
        print("=" * 60)
        for i, p in enumerate(publicados, 1):
            titulo_cat = self.get_nome_categoria_traduzido(p['categoria'], idioma)
            print(f"   {i}. {p['nome'][:50]} ({titulo_cat})")
        print("-" * 60)
        
        escolha = self.ler_numero("\nNúmero do artigo: ", 1, len(publicados))
        if escolha is None:
            return
        
        slug = publicados[escolha - 1]['slug']
        nome = publicados[escolha - 1]['nome']
        categoria = publicados[escolha - 1]['categoria']
        
        print(f"\n📤 UPLOAD DE IMAGEM PARA: {nome}")
        print("=" * 60)
        print("📁 Coloque a imagem na pasta: docs/assets/img/")
        print("📄 Exemplo: docs/assets/img/minha-imagem.jpg")
        print("⚠️  A imagem será aplicada em TODOS os idiomas!")
        print("-" * 60)
        
        caminho_imagem = input("\n📁 Nome do arquivo: ").strip()
        
        if not caminho_imagem:
            print("❌ Nome inválido!")
            input("\nPressione Enter...")
            return
        
        caminho_completo = self.assets_img / caminho_imagem
        if not caminho_completo.exists():
            print(f"❌ Arquivo não encontrado: {caminho_imagem}")
            print(f"   📁 Coloque em: {self.assets_img}")
            input("\nPressione Enter...")
            return
        
        timestamp = int(time.time() * 1000)
        imagem_url = f"/assets/img/{caminho_imagem}?t={timestamp}"
        
        print(f"\n🔄 Atualizando artigo com imagem: {caminho_imagem}")
        print("   📸 Sincronizando em TODOS os idiomas...")
        
        for lang in ['pt', 'en', 'es']:
            artigos_lang = self.ler_csv(lang)
            artigo_data = None
            for a in artigos_lang:
                if ((a.get('slug') or '').strip() or self.criar_slug(a.get('artigo', ''))) == slug:
                    artigo_data = a
                    break
            
            if artigo_data:
                self.criar_artigo(artigo_data, forcar=True, revisar=False, idioma=lang, forcar_head=True, imagem_manual=imagem_url)
                print(f"   ✅ {lang.upper()} atualizado")
        
        print(f"\n✅ Imagem manual aplicada em TODOS os idiomas!")
        
        self.criar_index(idioma=idioma)
        self.criar_todas_categorias(idioma=idioma)
        self.criar_sitemap()
        
        print("✅ Imagem sincronizada em TODO o site!")
        input("\nPressione Enter...")
    
    # ==================== ESCOLHER FONTE ====================
    
    def _escolher_fonte_imagem(self):
        print("\n📸 ESCOLHA A FONTE PARA A IMAGEM:")
        print("=" * 60)
        print("  [1] Unsplash (fotos artísticas)")
        print("  [2] Pexels (fotos comerciais)")
        print("  [3] Pixabay (fotos variadas)")
        print("  [4] IA (Pollinations)")
        print("  [5] Híbrido (ordem padrão)")
        print("  [0] Voltar")
        print("=" * 60)
        
        opcao = input("\n🎯 Escolha a fonte: ").strip()
        
        fonte_map = {
            '1': 'unsplash',
            '2': 'pexels',
            '3': 'pixabay',
            '4': 'ia',
            '5': 'hibrido'
        }
        
        if opcao == '0':
            return None
        elif opcao in fonte_map:
            return fonte_map[opcao]
        else:
            print("❌ Opção inválida!")
            return None
    
    # ==================== GERENCIAR IMAGEM - VERSÃO SIMPLIFICADA ====================
    
    def gerenciar_imagem_artigo(self):
        if self.idioma_selecionado is None:
            print("⚠️ Selecione um idioma primeiro!")
            return
        
        idioma = self.idioma_selecionado
        publicados = self.get_artigos_publicados(idioma)
        
        if not publicados:
            print(f"\n❌ Nenhum artigo publicado em {idioma.upper()}")
            input("\nPressione Enter...")
            return
        
        print(f"\n📋 ARTIGOS PUBLICADOS ({idioma.upper()})")
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
        
        artigos = self.ler_csv(idioma)
        artigo_data = None
        for a in artigos:
            if ((a.get('slug') or '').strip() or self.criar_slug(a.get('artigo', ''))) == slug:
                artigo_data = a
                break
        
        if artigo_data is None:
            print("❌ Artigo não encontrado no CSV!")
            input("\nPressione Enter...")
            return
        
        while True:
            print(f"\n📸 GERENCIAR IMAGEM: {nome}")
            print("=" * 60)
            print("  [1] 🔄 Alterar TUDO (miniatura + artigo) - SINCRONIZA TODOS")
            print("  [2] 🖼️ Alterar só a MINIATURA - SINCRONIZA TODOS")
            print("  [3] 📷 Alterar só a IMAGEM DENTRO - SINCRONIZA TODOS")
            print("  [4] 📤 Usar minha própria imagem (upload) - SINCRONIZA TODOS")
            print("  [5] 🖼️ Alterar só NESTE idioma (não sincroniza)")
            print("  [0] Voltar")
            print("=" * 60)
            print("💡 Opções 1,2,3,4 → SINCRONIZAM em todos os idiomas")
            print("💡 Opção 5 → Altera apenas no idioma atual")
            print("=" * 60)
            
            opcao = input("\n🎯 Escolha: ").strip()
            
            if opcao == "0":
                break
            
            # ============================================================
            # OPÇÃO 5: Alterar só neste idioma (NÃO sincroniza)
            # ============================================================
            if opcao == "5":
                print(f"\n🔄 Alterando APENAS no idioma {idioma.upper()}")
                print("   ⚠️ NÃO vai sincronizar com os outros idiomas!")
                
                fonte = self._escolher_fonte_imagem()
                if fonte is None:
                    continue
                
                self.fonte_temporaria = fonte
                nova_imagem = self.gerar_imagem(nome, categoria, slug, seed=int(time.time() * 1000) + random.randint(1, 9999))
                self.fonte_temporaria = None
                
                self._aplicar_imagens(artigo_data, idioma, nova_imagem, nova_imagem)
                print(f"   ✅ {idioma.upper()} atualizado (NÃO sincronizado)")
                
                self.criar_index(idioma=idioma)
                self.criar_todas_categorias(idioma=idioma)
                self.criar_sitemap()
                input("\nPressione Enter...")
                break
            
            # ============================================================
            # OPÇÕES 1,2,3,4: SINCRONIZAM em TODOS os idiomas
            # ============================================================
            if opcao in ["1", "2", "3", "4"]:
                if opcao == "4":
                    print(f"\n📤 UPLOAD DE IMAGEM PARA: {nome}")
                    print("=" * 60)
                    print("📁 Coloque a imagem na pasta: docs/assets/img/")
                    print("📄 Exemplo: docs/assets/img/minha-imagem.jpg")
                    print("⚠️  A imagem será aplicada em TODOS os idiomas!")
                    print("-" * 60)
                    
                    caminho_imagem = input("\n📁 Nome do arquivo: ").strip()
                    
                    if not caminho_imagem:
                        print("❌ Nome inválido!")
                        input("\nPressione Enter...")
                        continue
                    
                    caminho_completo = self.assets_img / caminho_imagem
                    if not caminho_completo.exists():
                        print(f"❌ Arquivo não encontrado: {caminho_imagem}")
                        print(f"   📁 Coloque em: {self.assets_img}")
                        input("\nPressione Enter...")
                        continue
                    
                    timestamp = int(time.time() * 1000)
                    imagem_url = f"/assets/img/{caminho_imagem}?t={timestamp}"
                    
                    print(f"\n🔄 Atualizando artigo com imagem: {caminho_imagem}")
                    print("   📸 SINCRONIZANDO em TODOS os idiomas...")
                    
                    for lang in ['pt', 'en', 'es']:
                        csv_lang = self.ler_csv(lang)
                        dados_lang = None
                        for a in csv_lang:
                            if ((a.get('slug') or '').strip() or self.criar_slug(a.get('artigo', ''))) == slug:
                                dados_lang = a
                                break
                        
                        if dados_lang:
                            self._aplicar_imagens(dados_lang, lang, imagem_url, imagem_url)
                            print(f"   ✅ {lang.upper()} atualizado")
                    
                    print(f"\n✅ Imagem manual aplicada em TODOS os idiomas!")
                    self.criar_index(idioma=idioma)
                    self.criar_todas_categorias(idioma=idioma)
                    self.criar_sitemap()
                    input("\nPressione Enter...")
                    break
                
                # Opções 1, 2, 3
                fonte = self._escolher_fonte_imagem()
                if fonte is None:
                    continue
                
                self.fonte_temporaria = fonte
                nova_imagem = self.gerar_imagem(nome, categoria, slug, seed=int(time.time() * 1000) + random.randint(1, 9999))
                self.fonte_temporaria = None
                
                print(f"\n🔄 SINCRONIZANDO em TODOS os idiomas...")
                
                for lang in ['pt', 'en', 'es']:
                    csv_lang = self.ler_csv(lang)
                    dados_lang = None
                    for a in csv_lang:
                        if ((a.get('slug') or '').strip() or self.criar_slug(a.get('artigo', ''))) == slug:
                            dados_lang = a
                            break
                    
                    if dados_lang:
                        if opcao == "1":
                            self._aplicar_imagens(dados_lang, lang, nova_imagem, nova_imagem)
                        elif opcao == "2":
                            imagem_interna = self._pegar_imagem_interna_atual(dados_lang, lang)
                            if not imagem_interna:
                                imagem_interna = nova_imagem
                            self._aplicar_imagens(dados_lang, lang, nova_imagem, imagem_interna)
                        elif opcao == "3":
                            miniatura_atual = self._pegar_miniatura_atual(dados_lang, lang)
                            if not miniatura_atual:
                                miniatura_atual = nova_imagem
                            self._aplicar_imagens(dados_lang, lang, miniatura_atual, nova_imagem)
                        print(f"   ✅ {lang.upper()} atualizado")
                
                print("✅ Imagem sincronizada em TODOS os idiomas!")
                self.criar_index(idioma=idioma)
                self.criar_todas_categorias(idioma=idioma)
                self.criar_sitemap()
                input("\nPressione Enter...")
                break
            
            else:
                print("❌ Opção inválida!")
                input("\nPressione Enter...")

    # ==================== DIAGNÓSTICO ====================
    
    def diagnosticar_problemas(self):
        print("\n🔍 DIAGNÓSTICO DO SITE")
        print("=" * 60)
        
        problemas = 0
        
        for idioma in ['pt', 'en', 'es']:
            pasta_idioma = self.docs / idioma
            if not pasta_idioma.exists():
                continue
            
            print(f"\n📂 {idioma.upper()}:")
            print("-" * 40)
            
            categorias = self.get_categorias_do_idioma(idioma)
            print(f"   Categorias ativas: {len(categorias)}")
            
            artigos = self.ler_csv(idioma)
            publicados_csv = [a for a in artigos if a.get('status') == 'publicado']
            rascunhos_csv = [a for a in artigos if a.get('status') != 'publicado']
            
            print(f"   Artigos no CSV: {len(artigos)} ({len(publicados_csv)} publicados, {len(rascunhos_csv)} rascunhos)")
            
            for cat in categorias:
                cat_traduzida = self.get_categoria_traduzida(cat, idioma)
                pasta_cat = pasta_idioma / cat_traduzida
                if not pasta_cat.exists():
                    continue
                
                for artigo_dir in pasta_cat.iterdir():
                    if not artigo_dir.is_dir():
                        continue
                    if not (artigo_dir / "index.html").exists():
                        continue
                    
                    slug = artigo_dir.name
                    existe_csv = False
                    for a in publicados_csv:
                        if ((a.get('slug') or '').strip() or self.criar_slug(a.get('artigo', ''))) == slug:
                            existe_csv = True
                            break
                    
                    if not existe_csv:
                        print(f"   ⚠️ Artigo na pasta sem CSV: {slug}")
                        problemas += 1
            
            for a in publicados_csv:
                slug = (a.get('slug') or '').strip() or self.criar_slug(a.get('artigo', ''))
                cat = a.get('categoria', 'geral')
                cat_traduzida = self.get_categoria_traduzida(cat, idioma)
                caminho = pasta_idioma / cat_traduzida / slug / "index.html"
                
                if not caminho.exists():
                    print(f"   ⚠️ Artigo no CSV sem pasta: {a.get('artigo', '')[:40]}")
                    problemas += 1
            
            for a in artigos:
                data = a.get('data_publicacao', '')
                if data and not self._is_valid_date(data):
                    print(f"   ⚠️ Data inválida: {a.get('artigo', '')[:40]} → '{data}'")
                    problemas += 1
        
        print("\n" + "=" * 60)
        if problemas == 0:
            print("✅ Nenhum problema encontrado!")
        else:
            print(f"⚠️ {problemas} problemas encontrados. Execute a sincronização (opção 7) para corrigir.")
        
        input("\nPressione Enter...")
    
    # ==================== GERAR TODOS OS IDIOMAS ====================
    
    def gerar_todos_idiomas(self):
        if self.idioma_selecionado is None:
            print("⚠️ Selecione um idioma primeiro!")
            return
        
        print("\n" + "=" * 70)
        print("  🚀 GERANDO IDIOMAS FALTANTES (PT → EN + ES)")
        print("=" * 70)
        
        artigos_pt = self.ler_csv('pt')
        publicados_pt = [a for a in artigos_pt if a.get('status') == 'publicado']
        
        if not publicados_pt:
            print("❌ Nenhum artigo publicado em PT!")
            input("\nPressione Enter...")
            return
        
        artigos_en_existentes = self.ler_csv('en')
        artigos_es_existentes = self.ler_csv('es')
        
        print(f"\n📊 Artigos em PT: {len(publicados_pt)}")
        print(f"📊 Artigos em EN: {len([a for a in artigos_en_existentes if a.get('status') == 'publicado'])}")
        print(f"📊 Artigos em ES: {len([a for a in artigos_es_existentes if a.get('status') == 'publicado'])}")
        print("-" * 40)
        
        criados_en = 0
        criados_es = 0
        pulados_en = 0
        pulados_es = 0
        
        for i, artigo_pt in enumerate(publicados_pt, 1):
            titulo_pt = artigo_pt.get('artigo', '')
            grupo_pt = (artigo_pt.get('grupo') or '').strip() or (artigo_pt.get('slug') or '').strip() or self.criar_slug(titulo_pt)
            
            print(f"\n[{i}/{len(publicados_pt)}] {titulo_pt[:50]}...")
            
            existe_en = False
            for a in artigos_en_existentes:
                if a.get('status') != 'publicado':
                    continue
                grupo_a = (a.get('grupo') or '').strip() or (a.get('slug') or '').strip()
                if grupo_a == grupo_pt:
                    existe_en = True
                    break
            
            if existe_en:
                print(f"   ⏭️ EN já existe, pulando...")
                pulados_en += 1
            else:
                artigo_en = self.criar_registro_traduzido(artigo_pt, 'en')
                artigos_en_existentes.append(artigo_en)
                self.salvar_csv(artigos_en_existentes, 'en')
                self.criar_artigo(artigo_en, forcar=True, revisar=False, idioma='en', forcar_head=True)
                criados_en += 1
                print(f"   ✅ EN criado: {artigo_en['artigo'][:40]}...")
            
            existe_es = False
            for a in artigos_es_existentes:
                if a.get('status') != 'publicado':
                    continue
                grupo_a = (a.get('grupo') or '').strip() or (a.get('slug') or '').strip()
                if grupo_a == grupo_pt:
                    existe_es = True
                    break
            
            if existe_es:
                print(f"   ⏭️ ES já existe, pulando...")
                pulados_es += 1
            else:
                artigo_es = self.criar_registro_traduzido(artigo_pt, 'es')
                artigos_es_existentes.append(artigo_es)
                self.salvar_csv(artigos_es_existentes, 'es')
                self.criar_artigo(artigo_es, forcar=True, revisar=False, idioma='es', forcar_head=True)
                criados_es += 1
                print(f"   ✅ ES criado: {artigo_es['artigo'][:40]}...")
            
            time.sleep(0.3)
        
        print("\n🔄 REGENERANDO SITE...")
        
        if criados_en > 0:
            self.criar_index(idioma='en')
            self.criar_todas_categorias(idioma='en')
        
        if criados_es > 0:
            self.criar_index(idioma='es')
            self.criar_todas_categorias(idioma='es')
        
        self.criar_index(idioma='pt')
        self.criar_todas_categorias(idioma='pt')
        
        self.criar_sitemap()
        self.criar_index_raiz()
        
        print("\n" + "=" * 70)
        print("✅ TRADUÇÃO CONCLUÍDA!")
        print("=" * 70)
        print(f"📊 Resumo:")
        print(f"   EN: {criados_en} criados, {pulados_en} já existiam")
        print(f"   ES: {criados_es} criados, {pulados_es} já existiam")
        print(f"\n📂 Total agora:")
        print(f"   PT: {len(publicados_pt)} artigos")
        print(f"   EN: {len([a for a in artigos_en_existentes if a.get('status') == 'publicado'])} artigos")
        print(f"   ES: {len([a for a in artigos_es_existentes if a.get('status') == 'publicado'])} artigos")
        print("=" * 70)
        
        input("\n⏎ Pressione Enter para continuar...")

    # ==================== SINCRONIZAR STATUS ====================
    
    def sincronizar_status(self, mostrar_confirmacao=True, idioma=None):
        if idioma is None:
            if self.idioma_selecionado is None:
                print("⚠️ Selecione um idioma primeiro!")
                return
            idioma = self.idioma_selecionado
        
        print(f"\n🔄 SINCRONIZANDO STATUS ({idioma.upper()})")
        print("-" * 40)
        
        if mostrar_confirmacao:
            print("📂 A PASTA DOCS É A FONTE DA VERDADE!")
            print("   Artigos na pasta → PUBLICADOS")
            print("   Rascunhos no CSV → MANTIDOS")
            print("   Publicados sem pasta → REMOVIDOS")
            print("-" * 40)
            if not self.ler_sim_nao("Continuar? (s/n): "):
                return
        
        artigos = self.ler_csv(idioma)
        pasta_idioma = self.docs / idioma
        
        if not pasta_idioma.exists():
            print("   ❌ Pasta não encontrada!")
            return
        
        slugs_na_pasta = set()
        for categoria_dir in pasta_idioma.iterdir():
            if not categoria_dir.is_dir() or categoria_dir.name in ['assets', 'netlify']:
                continue
            for artigo_dir in categoria_dir.iterdir():
                if artigo_dir.is_dir() and (artigo_dir / "index.html").exists():
                    slugs_na_pasta.add(artigo_dir.name)
        
        modificados = 0
        for a in artigos:
            slug = (a.get('slug') or '').strip() or self.criar_slug(a.get('artigo', ''))
            if slug in slugs_na_pasta:
                if a.get('status') != 'publicado':
                    a['status'] = 'publicado'
                    modificados += 1
            else:
                if a.get('status') == 'publicado':
                    a['status'] = 'rascunho'
                    modificados += 1
        
        if modificados > 0:
            self.salvar_csv(artigos, idioma)
            print(f"   ✅ {modificados} artigos atualizados")
        else:
            print("   ✅ Nenhuma alteração necessária")
        
        print(f"✅ Status sincronizado ({idioma.upper()})")
    
    # ==================== SINCRONIZAR PÁGINAS ====================
    
    def sincronizar_paginas(self, idioma=None):
        if idioma is None:
            if self.idioma_selecionado is None:
                print("⚠️ Selecione um idioma primeiro!")
                return
            idioma = self.idioma_selecionado
        
        print(f"\n🔄 REGENERANDO PÁGINAS ({idioma.upper()})")
        print("-" * 40)
        
        self.criar_index(idioma=idioma)
        self.criar_todas_categorias(idioma=idioma)
        self.criar_paginas_estaticas(idioma=idioma)
        self.criar_sitemap()
        
        print(f"✅ Páginas regeneradas ({idioma.upper()})")
    
    # ==================== SINCRONIZAR HTML ====================
    
    def sincronizar_html(self, idioma=None):
        if idioma is None:
            if self.idioma_selecionado is None:
                print("⚠️ Selecione um idioma primeiro!")
                return
            idioma = self.idioma_selecionado
        
        print(f"\n🔄 SINCRONIZANDO HTML ({idioma.upper()})")
        print("-" * 40)
        
        artigos = self.ler_csv(idioma)
        publicados = [a for a in artigos if a.get('status') == 'publicado']
        
        if not publicados:
            print("   ⚠️ Nenhum artigo publicado")
            return
        
        for a in publicados:
            self.criar_artigo(a, forcar=True, revisar=False, idioma=idioma, forcar_head=True)
        
        self.criar_index(idioma=idioma)
        self.criar_todas_categorias(idioma=idioma)
        self.criar_sitemap()
        
        print(f"✅ {len(publicados)} artigos sincronizados ({idioma.upper()})")
    
    # ==================== SINCRONIZAR TUDO ====================
    
    def sincronizar_agora(self):
        if self.idioma_selecionado is None:
            print("⚠️ Selecione um idioma primeiro!")
            return
        
        idioma = self.idioma_selecionado
        
        self._em_sincronizacao = True
        
        print(f"\n🔄 SINCRONIZANDO TUDO ({idioma.upper()})")
        print("=" * 60)
        print("📂 A PASTA DOCS É A FONTE DA VERDADE!")
        print("   Artigos na pasta → PUBLICADOS")
        print("   Rascunhos no CSV → MANTIDOS")
        print("   Publicados sem pasta → REMOVIDOS")
        print("   📄 HEADS dos artigos → REGENERADOS")
        print("=" * 60)
        
        print("\n📂 ESCANEANDO PASTAS...")
        print("-" * 40)
        
        pasta_idioma = self.docs / idioma
        artigos_na_pasta = {}
        categorias_validas = set()
        
        if not pasta_idioma.exists():
            print(f"   ❌ Pasta {idioma} não encontrada!")
            self._em_sincronizacao = False
            return
        
        for categoria_dir in pasta_idioma.iterdir():
            if not categoria_dir.is_dir():
                continue
            if categoria_dir.name in ['assets', 'netlify']:
                continue
            
            categoria = categoria_dir.name
            tem_artigos = False
            
            for artigo_dir in categoria_dir.iterdir():
                if not artigo_dir.is_dir():
                    continue
                
                index_path = artigo_dir / "index.html"
                if not index_path.exists():
                    continue
                
                titulo, descricao, texto = self.ler_artigo_html(str(index_path))
                
                if titulo in ["Título não encontrado", "Erro ao ler"]:
                    continue
                
                artigos_na_pasta[artigo_dir.name] = {
                    'nome': titulo,
                    'slug': artigo_dir.name,
                    'categoria': categoria,
                    'descricao': descricao
                }
                tem_artigos = True
                print(f"   📄 {categoria}/{artigo_dir.name}")
            
            if tem_artigos:
                categorias_validas.add(categoria)
        
        print(f"\n📊 Encontrados: {len(artigos_na_pasta)} artigos nas pastas")
        print(f"📁 Categorias ativas: {len(categorias_validas)}")
        
        csv_artigos = self.ler_csv(idioma)
        print(f"📄 Artigos no CSV: {len(csv_artigos)}")
        
        slugs_pasta = list(artigos_na_pasta.keys())
        csv_artigos_novo = []
        removidos = 0
        mantidos_rascunhos = 0
        
        for slug, dados in artigos_na_pasta.items():
            existe = False
            artigo_existente = None
            for a in csv_artigos:
                slug_csv = (a.get('slug') or '').strip() or self.criar_slug(a.get('artigo', ''))
                if slug_csv == slug:
                    existe = True
                    artigo_existente = a
                    break
            
            if existe and artigo_existente:
                if artigo_existente.get('categoria') != dados['categoria']:
                    print(f"   🔄 Atualizando categoria: {dados['nome'][:40]} → {dados['categoria']}")
                    artigo_existente['categoria'] = dados['categoria']
                if not (artigo_existente.get('slug') or '').strip():
                    artigo_existente['slug'] = slug
                artigo_existente['status'] = 'publicado'
                csv_artigos_novo.append(artigo_existente)
                print(f"   📌 Mantido: {dados['nome'][:40]}")
            else:
                novo_artigo = {
                    'artigo': dados['nome'],
                    'slug': slug,
                    'grupo': slug,
                    'links_afiliados': '#',
                    'status': 'publicado',
                    'categoria': dados['categoria'],
                    'palavras_chave': '',
                    'descricao': dados['descricao'] or f'Artigo sobre {dados["nome"]}',
                    'tipo': 'guia',
                    'data_publicacao': datetime.now().strftime("%Y-%m-%d"),
                    'autor': self.config.get('autor', 'Autor'),
                    'links_internos': '',
                    'links_externos': ''
                }
                csv_artigos_novo.append(novo_artigo)
                print(f"   ➕ Adicionado: {dados['nome'][:40]}")
        
        for a in csv_artigos:
            slug = (a.get('slug') or '').strip() or self.criar_slug(a.get('artigo', ''))
            status = a.get('status', 'rascunho').lower()
            categoria = a.get('categoria', '')
            
            if slug in slugs_pasta:
                continue
            elif status == 'rascunho':
                if categoria not in categorias_validas and categoria:
                    print(f"   ⚠️ Rascunho com categoria inválida: {a.get('artigo', '')[:40]} → '{categoria}'")
                    if categorias_validas:
                        nova_categoria = list(categorias_validas)[0]
                        print(f"   🔄 Movendo para: {nova_categoria}")
                        a['categoria'] = nova_categoria
                    else:
                        print(f"   🗑️ Removendo rascunho: {a.get('artigo', '')[:40]}")
                        continue
                csv_artigos_novo.append(a)
                mantidos_rascunhos += 1
                print(f"   📌 Mantendo rascunho: {a.get('artigo', '')[:40]}")
            else:
                ja_adicionado = False
                for existente in csv_artigos_novo:
                    slug_existente = (existente.get('slug') or '').strip() or self.criar_slug(existente.get('artigo', ''))
                    if slug_existente == slug:
                        ja_adicionado = True
                        break
                if not ja_adicionado:
                    print(f"   🗑️ Removendo publicado sem pasta: {a.get('artigo', '')[:40]}")
                    removidos += 1
        
        self.salvar_csv(csv_artigos_novo, idioma)
        print(f"\n📄 CSV atualizado: {len(csv_artigos_novo)} artigos")
        
        print("\n🔄 REGENERANDO PÁGINAS...")
        print("-" * 40)
        
        if artigos_na_pasta:
            print("   📄 REGENERANDO ARTIGOS COMPLETOS...")
            for slug, dados in artigos_na_pasta.items():
                for a in csv_artigos_novo:
                    if ((a.get('slug') or '').strip() or self.criar_slug(a.get('artigo', ''))) == slug:
                        self.criar_artigo(a, forcar=True, revisar=False, idioma=idioma, forcar_head=False)
                        break
            print("   ✅ Artigos regenerados")
        else:
            print("   ⏭️ Nenhum artigo para regenerar")
        
        self.criar_index(idioma=idioma)
        print(f"   ✅ Index regenerado")
        
        self.criar_todas_categorias(idioma=idioma)
        print(f"   ✅ Categorias regeneradas")
        
        self.criar_sitemap()
        print(f"   ✅ Sitemap regenerado")
        
        self.criar_paginas_estaticas(idioma=idioma)
        print(f"   ✅ Páginas estáticas regeneradas")
        
        self.criar_index_raiz()
        print(f"   ✅ Index raiz regenerado")
        
        print("\n" + "=" * 60)
        print("✅ SINCRONIZAÇÃO CONCLUÍDA!")
        print("=" * 60)
        print(f"📂 Artigos nas pastas: {len(artigos_na_pasta)}")
        print(f"📄 Artigos no CSV: {len(csv_artigos_novo)}")
        print(f"📌 Rascunhos mantidos: {mantidos_rascunhos}")
        print(f"🗑️ Publicados removidos: {removidos}")
        print(f"📁 Categorias ativas: {len(categorias_validas)}")
        print("=" * 60)
        
        self._em_sincronizacao = False
        input("\n⏎ Pressione Enter para continuar...")
    
    # ==================== DELETAR ARTIGO ====================
    
    def deletar_artigo(self):
        if self.idioma_selecionado is None:
            print("⚠️ Selecione um idioma primeiro!")
            return
        
        idioma = self.idioma_selecionado
        publicados = self.get_artigos_publicados(idioma)
        
        if not publicados:
            print(f"\n❌ Nenhum artigo publicado em {idioma.upper()}")
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
        
        if not self.ler_sim_nao(f"⚠️ DELETAR PERMANENTEMENTE '{nome}'? (s/n): "):
            return
        
        categoria_traduzida = self.get_categoria_traduzida(categoria, idioma)
        pasta = self.docs / idioma / categoria_traduzida / slug
        if pasta.exists():
            shutil.rmtree(pasta)
            print(f"   🗑️ Pasta removida: {pasta}")
        
        self.sincronizar_agora()
        
        print(f"\n✅ '{nome}' DELETADO COM SUCESSO!")
        input("\nPressione Enter...")

    # ==================== PÁGINAS ====================
    
    def criar_pagina(self, nome, titulo, conteudo_completo, ativo="inicio", idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        
        caminho = self.docs / idioma / f"{nome}.html"
        
        if '<!DOCTYPE html>' in conteudo_completo or '<html' in conteudo_completo:
            html = conteudo_completo
        else:
            t = self.t
            html = f"""<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
{self.renderizar_head_template(
    titulo=f"{self.get_nome_site_simples(idioma)} - {titulo}",
    descricao=f"{titulo} - {self.get_nome_site_simples(idioma)}",
    url=f"{self.config.get('url_base', '')}/{idioma}/{nome}.html",
    idioma=idioma
)}
</head>
<body>
    {self.get_header(ativo, None, idioma)}
    <main class="container">
        <div class="artigo">
            {conteudo_completo}
        </div>
    </main>
    {self.get_footer(idioma)}
    <script src="/assets/js/script.js?v={int(time.time())}"></script>
</body>
</html>"""
        
        caminho.parent.mkdir(parents=True, exist_ok=True)
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(html)
        return caminho
    
    def criar_paginas_estaticas(self, idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        
        print(f"\n📄 CRIANDO PÁGINAS ESTÁTICAS ({idioma.upper()})")
        print("-" * 40)
        
        nomes_arquivos = {
            'pt': {
                'sobre': 'sobre',
                'contato': 'contato',
                'politica-privacidade': 'politica-privacidade',
                'cookies': 'cookies',
                'faq': 'faq',
                'termos': 'termos'
            },
            'en': {
                'sobre': 'about',
                'contato': 'contact',
                'politica-privacidade': 'privacy-policy',
                'cookies': 'cookies',
                'faq': 'faq',
                'termos': 'terms'
            },
            'es': {
                'sobre': 'sobre',
                'contato': 'contacto',
                'politica-privacidade': 'politica-privacidad',
                'cookies': 'cookies',
                'faq': 'preguntas-frecuentes',
                'termos': 'terminos'
            }
        }
        
        titulos = {
            'pt': {
                'sobre': 'Sobre Nós',
                'contato': 'Contato',
                'politica-privacidade': 'Política de Privacidade',
                'cookies': 'Política de Cookies',
                'faq': 'Perguntas Frequentes',
                'termos': 'Termos de Uso'
            },
            'en': {
                'sobre': 'About Us',
                'contato': 'Contact',
                'politica-privacidade': 'Privacy Policy',
                'cookies': 'Cookies Policy',
                'faq': 'Frequently Asked Questions',
                'termos': 'Terms of Use'
            },
            'es': {
                'sobre': 'Sobre Nosotros',
                'contato': 'Contacto',
                'politica-privacidade': 'Política de Privacidad',
                'cookies': 'Política de Cookies',
                'faq': 'Preguntas Frecuentes',
                'termos': 'Términos de Uso'    
            }
        }
        
        nomes = nomes_arquivos.get(idioma, nomes_arquivos['pt'])
        titulos_idioma = titulos.get(idioma, titulos['pt'])
        
        for chave, nome_arquivo in nomes.items():
            titulo = titulos_idioma.get(chave, chave.capitalize())
            
            template_path = self.templates / idioma / f"{nome_arquivo}.html"
            
            if not template_path.exists():
                template_path = self.templates / idioma / f"{chave}.html"
            
            if not template_path.exists():
                template_path = self.templates / f"{nome_arquivo}.html"
                
            if template_path.exists():
                with open(template_path, 'r', encoding='utf-8') as f:
                    conteudo_template = f.read()
                
                html = conteudo_template
                
                html = html.replace('{{HEAD}}', self.renderizar_head_template(
                    titulo=f"{self.get_nome_site_simples(idioma)} - {titulo}",
                    descricao=f"{titulo} - {self.get_nome_site_simples(idioma)}",
                    url=f"{self.config.get('url_base', '')}/{idioma}/{nome_arquivo}.html",
                    idioma=idioma
                ))
                html = html.replace('{{HEADER}}', self.get_header(chave, None, idioma))
                html = html.replace('{{FOOTER}}', self.get_footer(idioma))
                html = html.replace('{{NOME_SITE}}', self.get_nome_site_simples(idioma))
                html = html.replace('{{TAGLINE}}', self.get_tagline(idioma))
                html = html.replace('{{DESCRICAO}}', self.get_descricao_traduzida(idioma))
                html = html.replace('{{IDIOMA}}', idioma)
                html = html.replace('{{ANO}}', str(self.config.get('ano', datetime.now().year)))
                html = html.replace('{{ICONE}}', self.config.get('icone', '✈️'))
                html = html.replace('{{EMAIL_CONTATO}}', self.config.get('email_contato', ''))
                
                html = re.sub(r'{{[^}]+}}', '', html)
                
                self.criar_pagina(nome_arquivo, titulo, html, ativo=chave, idioma=idioma)
                print(f"   ✅ {nome_arquivo}.html criado a partir do template: {template_path}")
            else:
                print(f"   ⚠️ Template não encontrado: {template_path}")
                conteudo = f"""
                <div class="page-header">
                    <h1>{titulo}</h1>
                    <p class="page-subtitle">Esta é a página {titulo} do {self.get_nome_site_simples(idioma)}.</p>
                </div>
                <div class="page-content">
                    <p>💡 Crie o arquivo <strong>templates/{idioma}/{nome_arquivo}.html</strong> com o conteúdo completo da página.</p>
                </div>
                """
                self.criar_pagina(nome_arquivo, titulo, conteudo, ativo=chave, idioma=idioma)
                print(f"   ✅ {nome_arquivo}.html criado (conteúdo básico)")
        
        print(f"✅ Páginas estáticas criadas! ({idioma.upper()})")
    
    # ==================== PÁGINAS DE CATEGORIA ====================
    
    def criar_pagina_categoria(self, categoria, idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        
        categorias_validas = self.get_categorias_do_idioma(idioma)
        if categoria not in categorias_validas:
            return None
        
        categoria_traduzida = self.get_categoria_traduzida(categoria, idioma)
        caminho = self.docs / idioma / categoria_traduzida / "index.html"
        t = self.t
        c = self.config
        
        titulo_categoria = self.get_nome_categoria_traduzido(categoria, idioma)
        
        descricao = self.get_descricao_categoria(categoria, idioma)
        
        artigos = self.get_artigos_publicados(idioma)
        artigos_cat = []
        for a in artigos:
            if a.get('categoria', '').lower() == categoria.lower():
                artigos_cat.append(a)
        
        if not artigos_cat:
            return None
        
        artigos_cat.sort(key=lambda x: x['data_publicacao'], reverse=True)
        
        artigos_html = ""
        for a in artigos_cat:
            img = self._pegar_imagem_existente(a['slug'], idioma) or self.gerar_imagem(a['nome'], a['categoria'], a['slug'])
            data_obj = self._parse_data_segura(a.get('data_publicacao', ''))
            data_formatada = data_obj.strftime("%d/%m/%Y")
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
            artigos_html += card
        
        template_html = self.ler_template('categoria.html', idioma)
        
        if template_html:
            variaveis = {
                'HEAD': self.renderizar_head_template(
                    titulo=f"{self.get_nome_site_simples(idioma)} - {titulo_categoria}",
                    descricao=descricao,
                    url=f"{c.get('url_base', '')}/{idioma}/{categoria_traduzida}/",
                    idioma=idioma
                ),
                'HEADER': self.get_header('categoria', categoria, idioma),
                'FOOTER': self.get_footer(idioma),
                'CATEGORIA': titulo_categoria,
                'DESCRICAO_CATEGORIA': descricao,
                'ARTIGOS_CATEGORIA': artigos_html,
                'NOME_SITE': self.get_nome_site_simples(idioma),
                'TAGLINE': self.get_tagline(idioma),
                'IDIOMA': idioma,
                'ICONE': self.config.get('icone', '✈️'),
                'ANO': str(self.config.get('ano', datetime.now().year)),
            }
            html = self.renderizar_template('categoria.html', variaveis, idioma)
        else:
            html = f"""<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
{self.renderizar_head_template(
    titulo=f"{self.get_nome_site_simples(idioma)} - {titulo_categoria}",
    descricao=descricao,
    url=f"{c.get('url_base', '')}/{idioma}/{categoria_traduzida}/",
    idioma=idioma
)}
</head>
<body>
    {self.get_header('categoria', categoria, idioma)}
    <main class="container">
        <div class="banner">
            <h1>{titulo_categoria}</h1>
            <p>{descricao}</p>
        </div>
        <div class="post-grid">
            {artigos_html}
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
        
        categorias = self.get_categorias_do_idioma(idioma)
        
        for cat in categorias:
            if self.criar_pagina_categoria(cat, idioma):
                titulo = self.get_nome_categoria_traduzido(cat, idioma)
                cat_traduzida = self.get_categoria_traduzida(cat, idioma)
                print(f"   ✅ /{idioma}/{cat_traduzida}/ - {titulo}")
        
        self.criar_index(idioma=idioma)
        self.criar_sitemap()
        
        print(f"✅ Páginas de categoria criadas! ({idioma.upper()})")
    
    # ==================== INDEX ====================
    
    def criar_index(self, pagina=1, idioma=None):
        """Cria a página inicial - USA O TEMPLATE COM SUBSTITUIÇÃO DIRETA"""
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        
        print(f"\n📄 GERANDO INDEX ({idioma.upper()})...")
        
        artigos = self.get_artigos_publicados(idioma)
        
        if not artigos:
            print(f"   ⚠️ Nenhum artigo encontrado")
            return
        
        artigos.sort(key=lambda x: x.get('data_publicacao', ''), reverse=True)
        
        posts_por_pagina = self.config.get('posts_por_pagina', 9)
        total_artigos = len(artigos)
        total_paginas = (total_artigos + posts_por_pagina - 1) // posts_por_pagina
        
        if pagina < 1:
            pagina = 1
        if pagina > total_paginas:
            pagina = total_paginas
        
        inicio = (pagina - 1) * posts_por_pagina
        fim = inicio + posts_por_pagina
        artigos_pagina = artigos[inicio:fim]
        
        # ============================================================
        # CONSTRÓI OS CARDS
        # ============================================================
        lista_cards = ""
        for a in artigos_pagina:
            img = self._pegar_imagem_existente(a['slug'], idioma)
            if not img:
                img = self.gerar_imagem(a['nome'], a['categoria'], a['slug'])
            if not img or img == '':
                img = f"https://picsum.photos/seed/{a['slug']}/1200/630"
            
            data_obj = self._parse_data_segura(a.get('data_publicacao', ''))
            data_formatada = data_obj.strftime("%d/%m/%Y")
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
        <span class="card__avatar">{self.config.get('autor', 'Autor')[:2].upper()}</span>
        <span>{self.config.get('autor', 'Autor')}</span>
      </div>
      <span>{data_formatada}</span>
    </div>
  </div>
</article>'''
            lista_cards += card
        
        # ============================================================
        # SIDEBAR - RELACIONADOS
        # ============================================================
        relacionados_sidebar = ""
        for a in artigos[:8]:
            cat_traduzida = self.get_categoria_traduzida(a['categoria'], idioma)
            if idioma != 'pt':
                nome_traduzido = self.traduzir_titulo(a['nome'], idioma)
                nome_rel = nome_traduzido if nome_traduzido else a['nome']
            else:
                nome_rel = a['nome']
            relacionados_sidebar += f'<li><a href="/{idioma}/{cat_traduzida}/{a["slug"]}/">{nome_rel}</a></li>\n'
        
        # ============================================================
        # SIDEBAR - CATEGORIAS
        # ============================================================
        categorias_sidebar = ""
        for cat in self.get_categorias_do_idioma(idioma):
            cat_traduzida = self.get_categoria_traduzida(cat, idioma)
            titulo_cat = self.get_nome_categoria_traduzido(cat, idioma)
            categorias_sidebar += f'<li><a href="/{idioma}/{cat_traduzida}/">{titulo_cat}</a></li>\n'
        
        # ============================================================
        # NAVEGAÇÃO
        # ============================================================
        navegacao = ""
        if total_paginas > 1:
            navegacao = '<div class="pagination">'
            if pagina > 1:
                if pagina - 1 == 1:
                    navegacao += f'<a href="/{idioma}/" class="page-link">‹ Anterior</a>'
                else:
                    navegacao += f'<a href="/{idioma}/index{pagina-1}.html" class="page-link">‹ Anterior</a>'
            for p in range(1, total_paginas + 1):
                if p == pagina:
                    navegacao += f'<span class="page-link active">{p}</span>'
                elif p == 1:
                    navegacao += f'<a href="/{idioma}/" class="page-link">{p}</a>'
                else:
                    navegacao += f'<a href="/{idioma}/index{p}.html" class="page-link">{p}</a>'
            if pagina < total_paginas:
                navegacao += f'<a href="/{idioma}/index{pagina+1}.html" class="page-link">Próximo ›</a>'
            navegacao += '</div>'
        
        # ============================================================
        # PRIMEIRO ARTIGO
        # ============================================================
        primeiro_artigo = "#"
        if artigos:
            primeiro = artigos[0]
            cat_trad = self.get_categoria_traduzida(primeiro['categoria'], idioma)
            primeiro_artigo = f"/{idioma}/{cat_trad}/{primeiro['slug']}/"
        
        # ============================================================
        # CARREGA O TEMPLATE
        # ============================================================
        template = self.ler_template('index.html', idioma)
        
        # Nome do site com tagline para o título
        nome_site_completo = self.get_nome_site_traduzido(idioma)
        nome_site_simples = self.get_nome_site_simples(idioma)
        tagline = self.get_tagline(idioma)
        
        if template is None:
            print(f"   ❌ ERRO: Template não encontrado! Verifique: templates/{idioma}/index.html")
            html = f'''<!DOCTYPE html>
<html lang="pt">
<head>
{self.renderizar_head_template(
    titulo=f"{nome_site_completo}",
    descricao=self.get_descricao_traduzida(idioma),
    url=f"{self.config.get('url_base', '')}/{idioma}/",
    idioma=idioma
)}
</head>
<body>
{self.get_header('inicio', None, idioma)}
<main class="container">
    <section class="hero">
        <h1>{self.get_frase_hero_traduzida(idioma)}</h1>
        <p>{self.get_descricao_traduzida(idioma)}</p>
    </section>
    <div class="post-grid">{lista_cards}</div>
    {navegacao}
</main>
{self.get_footer(idioma)}
<script src="/assets/js/script.js"></script>
</body>
</html>'''
        else:
            # SUBSTITUIÇÃO DIRETA DOS PLACEHOLDERS
            html = template
            
            html = html.replace('{{HEAD}}', self.renderizar_head_template(
                titulo=f"{nome_site_completo}",
                descricao=self.get_descricao_traduzida(idioma),
                url=f"{self.config.get('url_base', '')}/{idioma}/",
                idioma=idioma
            ))
            html = html.replace('{{HEADER}}', self.get_header('inicio', None, idioma))
            html = html.replace('{{FOOTER}}', self.get_footer(idioma))
            html = html.replace('{{PRIMEIRO_ARTIGO}}', primeiro_artigo)
            html = html.replace('{{LISTA_CARDS}}', lista_cards)
            html = html.replace('{{NAVEGACAO}}', navegacao)
            html = html.replace('{{RELACIONADOS_SIDEBAR}}', relacionados_sidebar)
            html = html.replace('{{CATEGORIAS_SIDEBAR}}', categorias_sidebar)
            html = html.replace('{{NOME_SITE}}', nome_site_simples)
            html = html.replace('{{TAGLINE}}', tagline)
            html = html.replace('{{IDIOMA}}', idioma)
            html = html.replace('{{ICONE}}', self.config.get('icone', '✈️'))
            html = html.replace('{{ANO}}', str(self.config.get('ano', datetime.now().year)))
            html = html.replace('{{DESCRICAO}}', self.get_descricao_traduzida(idioma))
            html = html.replace('{{FRASE_HERO}}', self.get_frase_hero_traduzida(idioma))
            html = html.replace('{{SLOGAN}}', self.get_slogan_traduzido(idioma))
            
            placeholders = re.findall(r'{{[^}]+}}', html)
            if placeholders:
                print(f"   ⚠️ Placeholders NÃO substituídos: {placeholders}")
            else:
                print(f"   ✅ Todos os placeholders substituídos com sucesso!")
        
        # SALVA
        caminho = self.docs / idioma / ("index.html" if pagina == 1 else f"index{pagina}.html")
        caminho.parent.mkdir(parents=True, exist_ok=True)
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Index {pagina}/{total_paginas} gerado ({len(artigos_pagina)} artigos)")
        
        if pagina == 1 and total_paginas > 1:
            for p in range(2, total_paginas + 1):
                self.criar_index(pagina=p, idioma=idioma)
        
        return caminho
    
    def criar_index_raiz(self):
        caminho = self.docs / "index.html"
        idioma_padrao = self.config.get('idioma_padrao', 'pt')
        nome_site = self.get_nome_site_simples('pt')
        
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
            border: 1px solid #f6b93b;
        }}
        .logo {{ font-size: 3rem; margin-bottom: 10px; }}
        h1 {{ font-size: 1.8rem; color: #0c2461; margin-bottom: 8px; }}
        p {{ color: #2d3436; margin-bottom: 30px; font-size: 0.95rem; }}
        .lang-options {{ display: flex; flex-direction: column; gap: 10px; }}
        .lang-option {{
            display: block;
            padding: 12px 20px;
            background: #f8f9fa;
            color: #0c2461;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: background 0.2s;
        }}
        .lang-option:hover {{ background: #f6b93b; color: #ffffff; }}
        .lang-option.default {{ background: #f6b93b; color: #ffffff; }}
        .lang-option.default:hover {{ background: #e58e26; }}
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
        <div class="logo">{self.config.get('icone', '✈️')}</div>
        <h1>{nome_site}</h1>
        <p>{self.get_descricao_traduzida('pt')}</p>
        <div class="lang-options">
            {opcoes_idiomas}
        </div>
    </div>
</body>
</html>"""
        
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"   ✅ Index raiz criado: index.html (redireciona para /{idioma_padrao}/)")
        return caminho

    # ==================== ARTIGOS ====================
    
    def criar_artigo(self, artigo_data, forcar=False, revisar=True, idioma=None, forcar_head=False, nova_imagem=False, imagem_manual=None):
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
        
        if idioma != 'pt':
            titulo_traduzido = self.traduzir_titulo(nome, idioma) or nome
            descricao_traduzida = self.traduzir_titulo(descricao, idioma) or descricao
        else:
            titulo_traduzido = nome
            descricao_traduzida = descricao
        
        slug = (artigo_data.get('slug') or '').strip()
        if not slug:
            slug = self.criar_slug(nome)
            artigo_data['slug'] = slug
            self._gravar_slug_no_csv(nome, slug, idioma)
        grupo = (artigo_data.get('grupo') or '').strip() or slug
        artigo_data['grupo'] = grupo
        pasta = self.docs / idioma / categoria_traduzida / slug
        t = self.t
        
        if forcar_head and (pasta / "index.html").exists():
            print(f"   🔄 Atualizando HEAD: {nome}")
            self._atualizar_head_artigo(pasta / "index.html", artigo_data, idioma, slug)
            return pasta / "index.html"
        
        if nova_imagem and (pasta / "index.html").exists():
            print(f"   🖼️ Regenerando imagem: {nome}")
            self._atualizar_imagem_artigo(pasta / "index.html", artigo_data, idioma, slug)
            return pasta / "index.html"
        
        # ===== PRIORIDADE: USA A IMAGEM DO PT (SINCRONIZAÇÃO) =====
        imagem_pt = self._pegar_imagem_pt(slug)

        if imagem_pt:
            print(f"   📸 Usando imagem do PT (sincronizada): {imagem_pt[:60]}...")
            imagem = imagem_pt
        else:
            # Fallback: imagem existente ou gera nova
            imagem_existente = self._pegar_imagem_existente(slug, idioma)
            if imagem_existente and not forcar and not nova_imagem and not imagem_manual:
                print(f"   📌 Mantendo imagem existente: {imagem_existente[:60]}...")
                imagem = imagem_existente
            else:
                print(f"   🖼️ Gerando imagem...")
                imagem = self.gerar_imagem(nome, categoria, slug, imagem_manual=imagem_manual)
        
        print(f"   📝 Criando: {idioma}/{categoria_traduzida}/{slug} (tipo: {tipo})")
        
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
            print(f"   📄 Conteúdo existente mantido (NÃO recriado pela IA)")
        
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
        data_obj = self._parse_data_segura(data_publicacao)
        data_formatada = data_obj.strftime("%d/%m/%Y")
        template = self.ler_template('artigo.html', idioma)
        
        # Nome do site para o título
        nome_site_simples = self.get_nome_site_simples(idioma)
        tagline = self.get_tagline(idioma)
        titulo_completo = f"{titulo} - {nome_site_simples}"
        if tagline:
            titulo_completo = f"{titulo} - {nome_site_simples} | {tagline}"
        
        if template:
            relacionados_html = ""
            relacionados = self.get_artigos_publicados(idioma)
            relacionados = [a for a in relacionados if a['slug'] != slug][:4]
            for a in relacionados:
                img = self._pegar_imagem_existente(a['slug'], idioma) or self.gerar_imagem(a['nome'], a['categoria'], a['slug'])
                data_obj_rel = self._parse_data_segura(a.get('data_publicacao', ''))
                data_formatada_rel = data_obj_rel.strftime("%d/%m/%Y")
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
            head_html = self.get_head(titulo, descricao_traduzida, url, imagem, idioma=idioma, slug=slug, eh_artigo=True, categoria_original=categoria, grupo=grupo)
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
                'DESCRICAO': descricao_traduzida,
                'TEMPO_LEITURA': str(random.randint(4, 8)),
                'IDIOMA': t['lang'],
                'NOME_SITE': nome_site_simples,
                'TAGLINE': tagline,
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
            
            article_lede = descricao_traduzida
            
            html = f"""<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
{self.get_head(
    titulo=titulo,
    descricao=descricao_traduzida,
    url=url,
    imagem=imagem,
    idioma=idioma,
    slug=slug,
    eh_artigo=True,
    categoria_original=categoria,
    grupo=grupo
)}
</head>
<body>
    {self.get_header('inicio', categoria, idioma)}
    <main>
        <header class="article-header">
            <div class="container article-header-inner">
                <a href="/{idioma}/" class="back-link">
                    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg>
                    {t['voltar_inicio']}
                </a>
                <span class="badge badge--{categoria}">{titulo_categoria}</span>
                <h1 class="article-title">{titulo}</h1>
                <p class="article-lede">{article_lede}</p>
                <div class="article-meta">
                    <span class="meta-item">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                        {autor}
                    </span>
                    <span class="meta-item">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>
                        {data_formatada}
                    </span>
                    <span class="meta-item">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
                        {random.randint(4, 8)} min de leitura
                    </span>
                </div>
            </div>
        </header>
        <div class="container article-cover">
            <img src="{imagem}" alt="{titulo_traduzido}" loading="lazy" />
        </div>
        <article class="container article-body">
            {conteudo_com_marcadores}
            {cta_html}
            <div style="margin-top:25px;padding-top:15px;border-top:1px solid var(--fundo);">
                <p><strong>{t['compartilhar']}:</strong>
                <a href="https://wa.me/?text={titulo} - {url}" target="_blank" style="color:var(--whatsapp);font-weight:600;text-decoration:none;">WhatsApp</a> |
                <a href="https://www.facebook.com/sharer/sharer.php?u={url}" target="_blank" style="color:#1877f2;font-weight:600;text-decoration:none;">Facebook</a> |
                <a href="https://twitter.com/intent/tweet?text={titulo}&url={url}" target="_blank" style="color:#000;font-weight:600;text-decoration:none;">Twitter</a>
                </p>
            </div>
        </article>
        <aside class="sidebar">
            <div class="widget">
                <h3>📚 {t['leia_tambem']}</h3>
                <ul>{artigos_relacionados}</ul>
            </div>
        </aside>
    </main>
    {self.get_footer(idioma)}
    <script src="/assets/js/script.js?v={int(time.time())}"></script>
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
            # SEMPRE usa a imagem do PT para sincronizar
            imagem = self._pegar_imagem_pt(slug) or self._pegar_imagem_existente(slug, idioma) or self.gerar_imagem(nome, categoria, slug)
            if idioma != 'pt':
                titulo_traduzido = self.traduzir_titulo(nome, idioma) or nome
                descricao_traduzida = self.traduzir_titulo(descricao, idioma) or descricao
            else:
                titulo_traduzido = nome
                descricao_traduzida = descricao
            titulo_map = {
                'review': f"{titulo_traduzido} - {self.t['review']}",
                'guia': f"Guia Completo: {titulo_traduzido}",
                'lista': f"Lista: {titulo_traduzido}",
                'tutorial': f"Tutorial: {titulo_traduzido}",
                'comparativo': f"Comparativo: {titulo_traduzido}",
                'artigo': f"{titulo_traduzido} - {self.t['review']}"
            }
            titulo = titulo_map.get(artigo_data.get('tipo', 'review'), f"{titulo_traduzido} - {self.t['review']}")
            grupo = (artigo_data.get('grupo') or '').strip() or slug
            novo_head = self.get_head(titulo, descricao_traduzida, url, imagem, idioma=idioma, slug=slug, eh_artigo=True, categoria_original=categoria, grupo=grupo)
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
            
            seed = int(time.time() * 1000) + random.randint(1, 999999)
            nova_imagem = self.gerar_imagem(nome, categoria, slug, seed, forcar_nova=True)
            
            html_novo = re.sub(
                r'<div class="container article-cover">.*?<img[^>]*src="[^"]*"[^>]*>.*?</div>',
                f'<div class="container article-cover">\n            <img src="{nova_imagem}" alt="{nome}" loading="lazy" />\n        </div>',
                html_existente,
                flags=re.DOTALL
            )
            
            match = re.search(r'<article class="container article-body">(.*?)</article>', html_novo, re.DOTALL)
            if match:
                corpo = match.group(1)
                corpo = re.sub(
                    r'<img[^>]*src="[^"]*"[^>]*>',
                    f'<img src="{nova_imagem}" alt="{nome}" loading="lazy" />',
                    corpo,
                    count=1
                )
                html_novo = html_novo.replace(match.group(1), corpo)
            
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

    # ==================== HEADER ====================
    
    def get_header(self, ativo="inicio", categoria_atual=None, idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        
        header_template = self.ler_template('header.html', idioma)
        
        categorias = self.get_categorias_do_idioma(idioma)
        nome_site = self.get_nome_site_simples(idioma)
        
        if header_template:
            cat_links = ""
            for cat in categorias[:6]:
                cat_traduzida = self.get_categoria_traduzida(cat, idioma)
                ativo_cat = 'ativo' if categoria_atual == cat else ''
                titulo_cat = self.get_nome_categoria_traduzido(cat, idioma)
                cat_links += f'<a href="/{idioma}/{cat_traduzida}/" class="{ativo_cat}">{titulo_cat}</a>'
            
            header_html = header_template.replace('{{NOME_SITE}}', nome_site)
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
            <span class="icone">{self.config.get('icone', '✈️')}</span>
            <span class="nome">{nome_site}</span>
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

    def renderizar_head_template(self, titulo, descricao, url, idioma, imagem=None):
        """Renderiza o HEAD a partir do template head.html (para páginas normais)"""
        head_template = self.ler_template('head.html', idioma)
        
        if not head_template:
            # Fallback: usa get_head()
            return self.get_head(
                titulo=titulo,
                descricao=descricao,
                url=url,
                imagem=imagem or self.config.get(f'imagem_padrao_{idioma}', '/assets/img/og-default.jpg'),
                idioma=idioma,
                eh_artigo=False
            )
        
        head_html = head_template
        head_html = head_html.replace('{{TITULO}}', titulo)
        head_html = head_html.replace('{{DESCRICAO}}', descricao)
        head_html = head_html.replace('{{URL}}', url)
        head_html = head_html.replace('{{IMAGEM}}', imagem or self.config.get(f'imagem_padrao_{idioma}', '/assets/img/og-default.jpg'))
        head_html = head_html.replace('{{NOME_SITE}}', self.get_nome_site_simples(idioma))
        head_html = head_html.replace('{{TAGLINE}}', self.get_tagline(idioma))
        head_html = head_html.replace('{{AUTOR}}', self.config.get('autor', 'Autor'))
        head_html = head_html.replace('{{DATA}}', datetime.now().strftime('%Y-%m-%d'))
        head_html = head_html.replace('{{EXTRA_HEAD}}', '')
        
        return head_html

    def get_head(self, titulo, descricao, url, imagem="", extra="", idioma="pt", slug="", eh_artigo=False, categoria_original=None, grupo=""):
        if not imagem:
            imagem = self.config.get(f'imagem_padrao_{idioma}', '/assets/img/og-default.jpg')

        site_name = self.get_nome_site_simples(idioma)
        tagline = self.get_tagline(idioma)
        
        # Monta o título completo
        titulo_completo = f"{titulo} - {site_name}"
        if tagline:
            titulo_completo = f"{titulo} - {site_name} | {tagline}"
        
        timestamp = int(time.time())

        cache_control = '''<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<meta name="robots" content="index, follow">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
'''

        hreflang_tags = ""
        base_url = self.config.get('url_base', '').rstrip('/')
        canonical = url

        if eh_artigo:
            grupo_atual = (grupo or slug or self.criar_slug(titulo)).strip()
            urls_por_idioma = {}

            for lang in self.config.get('idiomas', []):
                codigo = lang.get('codigo', 'pt')
                
                if codigo == idioma:
                    urls_por_idioma[codigo] = canonical
                    continue
                
                for a in self.ler_csv(codigo):
                    if a.get('status') != 'publicado':
                        continue
                    grupo_a = (a.get('grupo') or '').strip() or (a.get('slug') or '').strip()
                    if grupo_a != grupo_atual:
                        continue
                    slug_a = (a.get('slug') or '').strip() or self.criar_slug(a.get('artigo', ''))
                    cat_a = self.get_categoria_traduzida(a.get('categoria', 'geral'), codigo)
                    caminho_a = self.docs / codigo / cat_a / slug_a / "index.html"
                    if caminho_a.exists():
                        urls_por_idioma[codigo] = f"{base_url}/{codigo}/{cat_a}/{slug_a}/"
                    break

            for lang in self.config.get('idiomas', []):
                codigo = lang.get('codigo', 'pt')
                if codigo in urls_por_idioma:
                    hreflang_tags += f'<link rel="alternate" href="{urls_por_idioma[codigo]}" hreflang="{codigo}" />\n'

            idioma_default = 'pt'
            if idioma_default in urls_por_idioma:
                hreflang_tags += f'<link rel="alternate" href="{urls_por_idioma[idioma_default]}" hreflang="x-default" />\n'

        return f'''<meta charset="UTF-8">
{cache_control}<title>{titulo_completo}</title>
<meta name="description" content="{descricao[:160]}">
<link rel="canonical" href="{canonical}">
{hreflang_tags}<meta property="og:title" content="{titulo_completo}">
<meta property="og:description" content="{descricao[:160]}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{imagem}">
<meta property="og:type" content="website">
<meta property="og:locale" content="{idioma}">
<meta property="og:site_name" content="{site_name}">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css?v={timestamp}">
<link rel="stylesheet" href="/assets/css/custom.css?v={timestamp}">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
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
{extra}'''
    
    # ==================== FOOTER ====================
    
    def get_footer(self, idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        
        categorias = self.get_categorias_do_idioma(idioma)
        cat_links = ""
        for cat in categorias[:8]:
            cat_traduzida = self.get_categoria_traduzida(cat, idioma)
            titulo_cat = self.get_nome_categoria_traduzido(cat, idioma)
            cat_links += f'<li><a href="/{idioma}/{cat_traduzida}/">{titulo_cat}</a></li>\n'
        
        footer_template = self.ler_template('footer.html', idioma)
        
        nome_site = self.get_nome_site_simples(idioma)
        tagline = self.get_tagline(idioma)
        
        if footer_template is None:
            footer_template = """<!-- ===== Footer ===== -->
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <a href="/{{IDIOMA}}/" class="logo logo--light">
        <span class="logo-mark">{{ICONE}}</span>
        {{NOME_SITE}}
      </a>
      <p>{{TAGLINE}}</p>
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
        
        footer_html = footer_template.replace('{{NOME_SITE}}', nome_site)
        footer_html = footer_html.replace('{{TAGLINE}}', tagline)
        footer_html = footer_html.replace('{{DESCRICAO}}', self.get_descricao_traduzida(idioma))
        footer_html = footer_html.replace('{{ANO}}', str(self.config.get('ano', datetime.now().year)))
        footer_html = footer_html.replace('{{CATEGORIAS_FOOTER}}', cat_links)
        footer_html = footer_html.replace('{{IDIOMA}}', idioma)
        footer_html = footer_html.replace('{{ICONE}}', self.config.get('icone', '✈️'))
        
        return footer_html

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
            
            paginas = [
                ('', 1.0),
                ('sobre.html', 0.5),
                ('contato.html', 0.5),
                ('politica-privacidade.html', 0.3),
                ('cookies.html', 0.3),
                ('termos.html', 0.3)
            ]
            
            for pagina, prioridade in paginas:
                url_elem = ET.SubElement(urlset, 'url')
                loc = ET.SubElement(url_elem, 'loc')
                loc.text = f"{base_url}/{idioma}/{pagina}" if pagina else f"{base_url}/{idioma}/"
                
                lastmod = ET.SubElement(url_elem, 'lastmod')
                lastmod.text = datetime.now().strftime('%Y-%m-%d')
                
                changefreq = ET.SubElement(url_elem, 'changefreq')
                changefreq.text = 'monthly' if pagina else 'weekly'
                
                priority = ET.SubElement(url_elem, 'priority')
                priority.text = str(prioridade)
            
            categorias = self.get_categorias_do_idioma(idioma)
            for cat in categorias:
                artigos_cat = [a for a in self.get_artigos_publicados(idioma) if a.get('categoria', '').lower() == cat.lower()]
                if artigos_cat:
                    cat_traduzida = self.get_categoria_traduzida(cat, idioma)
                    url_elem = ET.SubElement(urlset, 'url')
                    loc = ET.SubElement(url_elem, 'loc')
                    loc.text = f"{base_url}/{idioma}/{cat_traduzida}/"
                    
                    lastmod = ET.SubElement(url_elem, 'lastmod')
                    lastmod.text = datetime.now().strftime('%Y-%m-%d')
                    
                    changefreq = ET.SubElement(url_elem, 'changefreq')
                    changefreq.text = 'weekly'
                    
                    priority = ET.SubElement(url_elem, 'priority')
                    priority.text = '0.6'
            
            artigos = self.get_artigos_publicados(idioma)
            for a in artigos:
                cat_traduzida = self.get_categoria_traduzida(a['categoria'], idioma)
                
                caminho_artigo = self.docs / idioma / cat_traduzida / a['slug'] / "index.html"
                if not caminho_artigo.exists():
                    continue
                
                url_elem = ET.SubElement(urlset, 'url')
                loc = ET.SubElement(url_elem, 'loc')
                loc.text = f"{base_url}/{idioma}/{cat_traduzida}/{a['slug']}/"
                
                lastmod = ET.SubElement(url_elem, 'lastmod')
                data_pub = a.get('data_publicacao', datetime.now().strftime("%Y-%m-%d"))
                try:
                    if len(data_pub) == 10:
                        lastmod.text = data_pub
                    else:
                        lastmod.text = datetime.now().strftime('%Y-%m-%d')
                except:
                    lastmod.text = datetime.now().strftime('%Y-%m-%d')
                
                changefreq = ET.SubElement(url_elem, 'changefreq')
                changefreq.text = 'weekly'
                
                priority = ET.SubElement(url_elem, 'priority')
                priority.text = '0.7'
            
            xml_str = ET.tostring(urlset, encoding='unicode')
            xml_pretty = minidom.parseString(xml_str).toprettyxml(indent="  ")
            xml_pretty = '\n'.join(xml_pretty.split('\n')[1:])
            
            with open(sitemap_path, 'w', encoding='utf-8') as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write(xml_pretty)
            
            print(f"   ✅ Sitemap gerado: {idioma}/sitemap.xml ({len(artigos)} artigos + {len(categorias)} categorias)")
            sitemaps_idiomas.append(f"{base_url}/{idioma}/sitemap.xml")
        
        if sitemaps_idiomas:
            sitemap_index = self.docs / "sitemap.xml"
            index = ET.Element('sitemapindex')
            index.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
            
            for sitemap_url in sitemaps_idiomas:
                sitemap_elem = ET.SubElement(index, 'sitemap')
                loc = ET.SubElement(sitemap_elem, 'loc')
                loc.text = sitemap_url
                
                lastmod = ET.SubElement(sitemap_elem, 'lastmod')
                lastmod.text = datetime.now().strftime('%Y-%m-%d')
            
            xml_str = ET.tostring(index, encoding='unicode')
            xml_pretty = minidom.parseString(xml_str).toprettyxml(indent="  ")
            xml_pretty = '\n'.join(xml_pretty.split('\n')[1:])
            
            with open(sitemap_index, 'w', encoding='utf-8') as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write(xml_pretty)
            
            print(f"\n   ✅ Sitemap principal criado: sitemap.xml (aponta para {len(sitemaps_idiomas)} idiomas)")
        
        robots_path = self.docs / "robots.txt"
        with open(robots_path, 'w', encoding='utf-8') as f:
            f.write("User-agent: *\n")
            f.write("Allow: /\n")
            f.write("Disallow: /assets/\n")
            f.write("Disallow: /404.html\n\n")
            
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
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=120
            )
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
    
    def publicar_com_traducao(self):
        if self.idioma_selecionado is None:
            print("⚠️ Selecione um idioma primeiro!")
            return
        
        print("\n⚠️ Esta função foi substituída pela opção 11 (GERAR TODOS OS IDIOMAS)")
        input("\nPressione Enter...")

    # ==================== VER ARTIGOS ====================
    
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
        
        rascunhos = []
        publicados = []
        for a in artigos:
            if a.get('status', 'rascunho').lower() == 'publicado':
                publicados.append(a)
            else:
                rascunhos.append(a)
        
        print("\n" + "=" * 70)
        print(f"📋 ARTIGOS ({idioma.upper()})")
        print("=" * 70)
        
        idx = 1
        if rascunhos:
            print("\n  ⏳ RASCUNHOS")
            for a in rascunhos:
                nome = a.get('artigo', 'Sem nome')[:40]
                print(f"  [{idx}] ⏳ {nome}")
                idx += 1
        
        if publicados:
            print("\n  ✅ PUBLICADOS")
            for a in publicados:
                nome = a.get('artigo', 'Sem nome')[:40]
                data = a.get('data_publicacao', '')
                if data:
                    try:
                        data_obj = self._parse_data_segura(data)
                        data = data_obj.strftime("%d/%m/%Y")
                    except:
                        pass
                print(f"  [{idx}] ✅ {nome}  {data}")
                idx += 1
        
        print("\n" + "-" * 70)
        escolha = self.ler_numero("Escolha o número (0 para voltar): ", 0, len(artigos))
        if escolha is None or escolha == 0:
            return
        
        artigo_escolhido = artigos[escolha - 1]
        nome = artigo_escolhido.get('artigo', 'Sem nome')
        categoria = artigo_escolhido.get('categoria', 'geral')
        status = artigo_escolhido.get('status', 'rascunho')
        is_publicado = status.lower() == 'publicado'
        
        while True:
            print("\n" + "=" * 70)
            print(f"📝 {nome}")
            print(f"📂 Categoria: {self.get_nome_categoria_traduzido(categoria, idioma)}")
            if is_publicado:
                print(f"📌 Status: ✅ PUBLICADO")
                print("=" * 70)
                print("  1. 📖 Ver no navegador")
                print("  2. 🖼️ Gerenciar imagem")
                print("  3. 🗑️ Despublicar")
                print("  4. ❌ Voltar")
            else:
                print(f"📌 Status: ⏳ RASCUNHO")
                print("=" * 70)
                print("  1. 📝 Publicar agora")
                print("  2. 🔄 Regenerar CONTEÚDO")
                print("  3. 🖼️ Gerenciar imagem")
                print("  4. ❌ Voltar")
            
            opcao = input("\nEscolha: ").strip()
            
            if opcao == "1":
                if is_publicado:
                    slug = (artigo_escolhido.get('slug') or '').strip() or self.criar_slug(artigo_escolhido.get('artigo', ''))
                    cat_traduzida = self.get_categoria_traduzida(categoria, idioma)
                    caminho = self.docs / idioma / cat_traduzida / slug / "index.html"
                    if caminho.exists():
                        webbrowser.open(str(caminho))
                    else:
                        print("❌ Arquivo não encontrado!")
                    input("\nPressione Enter...")
                else:
                    print(f"\n📝 Publicando: {nome}")
                    artigo_escolhido['status'] = 'publicado'
                    if not artigo_escolhido.get('data_publicacao'):
                        artigo_escolhido['data_publicacao'] = datetime.now().strftime("%Y-%m-%d")
                    artigos = self.ler_csv(idioma)
                    for a in artigos:
                        if a.get('artigo') == nome:
                            a['status'] = 'publicado'
                            if not a.get('data_publicacao'):
                                a['data_publicacao'] = datetime.now().strftime("%Y-%m-%d")
                            break
                    self.salvar_csv(artigos, idioma)
                    self.criar_artigo(artigo_escolhido, forcar=True, revisar=True, idioma=idioma, forcar_head=False)
                    self.criar_sitemap()
                    print(f"   ✅ Artigo publicado!")
                    input("\nPressione Enter...")
                    return
            elif opcao == "2":
                self.gerenciar_imagem_artigo()
            elif opcao == "3":
                if is_publicado:
                    print(f"\n🗑️ Despublicando: {nome}")
                    artigos = self.ler_csv(idioma)
                    for a in artigos:
                        if a.get('artigo') == nome:
                            a['status'] = 'rascunho'
                            break
                    self.salvar_csv(artigos, idioma)
                    self.criar_sitemap()
                    print(f"   ⏳ Status alterado para RASCUNHO")
                    input("\nPressione Enter...")
                    return
                else:
                    print(f"\n🔄 Regenerando conteúdo...")
                    self.criar_artigo(artigo_escolhido, forcar=True, revisar=True, idioma=idioma, forcar_head=False)
                    print(f"   ✅ Conteúdo regenerado!")
                    input("\nPressione Enter...")
            elif opcao == "4":
                return
            else:
                print("❌ Opção inválida")
                input("\nPressione Enter...")

    # ==================== CONTEÚDO COM IA ====================
    
    def gerar_conteudo_ia(self, artigo, link, categoria="geral", palavras_chave="", tipo="review", idioma="pt", links_internos="", links_externos=""):
        if not self.ia_api_key:
            return self.conteudo_basico(artigo, link, tipo, idioma)
        
        nome_idioma = {
            'pt': 'português do Brasil',
            'en': 'English',
            'es': 'español'
        }.get(idioma, 'português do Brasil')
        
        prompt = f"""
        Crie um {tipo} sobre {artigo} em {nome_idioma}.
        CATEGORIA: {categoria}
        PALAVRAS-CHAVE: {palavras_chave}
        LINKS INTERNOS: {links_internos}
        LINKS EXTERNOS: {links_externos}
        
        ESTRUTURA:
        1. Título (h1)
        2. Introdução (h2)
        3. Conteúdo principal com subtítulos (h2, h3)
        4. FAQ com <details> e <summary>
        5. Conclusão (h2)
        
        Use classes: article-table, faq, faq-item
        O conteúdo deve ser 100% em {nome_idioma}.
        Retorne APENAS HTML válido.
        """
        
        try:
            headers = {"Authorization": f"Bearer {self.ia_api_key}", "Content-Type": "application/json"}
            data = {
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {"role": "system", "content": f"Você é especialista em {categoria} e criação de conteúdo."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 6000,
                "temperature": 0.8
            }
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=120
            )
            if response.status_code == 200:
                conteudo = response.json()["choices"][0]["message"]["content"]
                conteudo = re.sub(r'```(?:html)?\s*', '', conteudo)
                conteudo = re.sub(r'\s*```', '', conteudo)
                return conteudo
            else:
                print(f"   ⚠️ Erro na API: {response.status_code}")
                return self.conteudo_basico(artigo, link, tipo, idioma)
        except Exception as e:
            print(f"   ⚠️ Erro IA: {e}")
            return self.conteudo_basico(artigo, link, tipo, idioma)
    
    def revisar_com_ia(self, conteudo, artigo, categoria="geral", tipo="review", idioma="pt"):
        if not self.ia_api_key:
            return conteudo
        
        nome_idioma = {
            'pt': 'português do Brasil',
            'en': 'English',
            'es': 'español'
        }.get(idioma, 'português do Brasil')
        
        prompt = f"""
        Revise e MELHORE este artigo sobre {artigo} em {nome_idioma}.
        TIPO: {tipo}
        CATEGORIA: {categoria}
        
        MELHORIAS:
        1. Aprofunde a introdução
        2. Adicione mais detalhes
        3. Enriqueça a tabela
        4. Melhore o FAQ
        5. O conteúdo deve ser 100% em {nome_idioma}
        
        CONTEÚDO:
        {conteudo}
        
        Retorne APENAS o HTML revisado.
        """
        
        try:
            headers = {"Authorization": f"Bearer {self.ia_api_key}", "Content-Type": "application/json"}
            data = {
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {"role": "system", "content": f"Revisor especialista em {categoria}."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 6000,
                "temperature": 0.7
            }
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=120
            )
            if response.status_code == 200:
                revisado = response.json()["choices"][0]["message"]["content"]
                revisado = re.sub(r'```(?:html)?\s*', '', revisado)
                revisado = re.sub(r'\s*```', '', revisado)
                return revisado
            else:
                return conteudo
        except Exception as e:
            print(f"   ⚠️ Erro na revisão: {e}")
            return conteudo
    
    def conteudo_basico(self, artigo, link, tipo="review", idioma="pt"):
        t = self.t
        
        textos = {
            'pt': {
                'review': f"Review: {artigo}",
                'guia': f"Guia: {artigo}",
                'lista': f"Lista: {artigo}",
                'tutorial': f"Tutorial: {artigo}",
                'comparativo': f"Comparativo: {artigo}",
                'default': f"Artigo: {artigo}",
                'beneficios': 'Benefícios',
                'comprar': 'Comprar Agora',
                'ver_oferta': 'Ver Oferta',
                'jornada': 'Comece sua jornada'
            },
            'en': {
                'review': f"Review: {artigo}",
                'guia': f"Guide: {artigo}",
                'lista': f"List: {artigo}",
                'tutorial': f"Tutorial: {artigo}",
                'comparativo': f"Comparison: {artigo}",
                'default': f"Article: {artigo}",
                'beneficios': 'Benefits',
                'comprar': 'Buy Now',
                'ver_oferta': 'View Offer',
                'jornada': 'Start your journey'
            },
            'es': {
                'review': f"Review: {artigo}",
                'guia': f"Guía: {artigo}",
                'lista': f"Lista: {artigo}",
                'tutorial': f"Tutorial: {artigo}",
                'comparativo': f"Comparativo: {artigo}",
                'default': f"Artículo: {artigo}",
                'beneficios': 'Beneficios',
                'comprar': 'Comprar Ahora',
                'ver_oferta': 'Ver Oferta',
                'jornada': 'Comienza tu viaje'
            }
        }
        
        txt = textos.get(idioma, textos['pt'])
        
        titulo_map = {
            'review': txt['review'],
            'guia': txt['guia'],
            'lista': txt['lista'],
            'tutorial': txt['tutorial'],
            'comparativo': txt['comparativo']
        }
        titulo = titulo_map.get(tipo, txt['default'])
        
        return f"""
<h1 id="introducao">{titulo}</h1>

<p><strong>{artigo}</strong> é a escolha perfeita.</p>

<h2 id="beneficios">{txt['beneficios']}</h2>
<ul>
    <li><strong>Qualidade:</strong> Produto de alta qualidade</li>
    <li><strong>Confiança:</strong> Garantia de satisfação</li>
    <li><strong>Resultados:</strong> Resultados comprovados</li>
</ul>

<div class="cta-box">
    <h3>{txt['comprar']}</h3>
    <p>{txt['jornada']}</p>
    <a href="{link}" class="btn-primary" target="_blank" rel="nofollow sponsored">{txt['ver_oferta']}</a>
</div>
"""
    
    # ==================== GET ARTIGOS PUBLICADOS ====================
    
    def get_artigos_publicados(self, idioma=None):
        if idioma is None:
            idioma = self.idioma_selecionado or self.idioma_padrao
        
        artigos = self.ler_csv(idioma)
        publicados = []
        for a in artigos:
            if a.get('status') == 'publicado':
                slug = (a.get('slug') or '').strip() or self.criar_slug(a.get('artigo', ''))
                categoria = a.get('categoria', 'geral')
                categoria_traduzida = self.get_categoria_traduzida(categoria, idioma)
                
                caminho = self.docs / idioma / categoria_traduzida / slug / "index.html"
                if caminho.exists():
                    publicados.append({
                        'slug': slug,
                        'nome': a.get('artigo', ''),
                        'categoria': categoria,
                        'data_publicacao': a.get('data_publicacao', datetime.now().strftime("%Y-%m-%d"))
                    })
                else:
                    print(f"   ⚠️ Pasta não encontrada: {categoria_traduzida}/{slug}")
        
        return publicados

    # ==================== PUBLICAR ====================
    
    def publicar_um(self):
        if self.idioma_selecionado is None:
            print("⚠️ Selecione um idioma primeiro!")
            return
        
        idioma = self.idioma_selecionado
        self.sincronizar_status(mostrar_confirmacao=False, idioma=idioma)
        
        artigos = self.ler_csv(idioma)
        pendentes = [a for a in artigos if a.get('status', 'rascunho').lower() != 'publicado']
        
        if not pendentes:
            print(f"\n✅ Nenhum artigo pendente")
            input("\nPressione Enter...")
            return
        
        print(f"\n📋 RASCUNHOS ({idioma.upper()}):")
        print("-" * 60)
        for i, a in enumerate(pendentes, 1):
            print(f"  {i}. {a.get('artigo', 'Sem nome')}")
        print("-" * 60)
        
        escolha = self.ler_numero("\nEscolha o número: ", 1, len(pendentes))
        if escolha is None:
            return
        
        a = pendentes[escolha - 1]
        
        print("\n" + "=" * 60)
        print("📝 PREVIEW:")
        print("=" * 60)
        print(f"  Título: {a.get('artigo')}")
        print(f"  Categoria: {a.get('categoria', 'geral')}")
        print(f"  Tipo: {a.get('tipo', 'review')}")
        print("=" * 60)
        
        if not self.ler_sim_nao("\nPublicar? (s/n): "):
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
            print(f"✅ Nenhum artigo pendente")
            input("\nPressione Enter...")
            return
        
        categorias = {}
        for a in pendentes:
            cat = a.get('categoria', 'geral')
            if cat not in categorias:
                categorias[cat] = []
            categorias[cat].append(a)
        
        print(f"\n📊 {len(pendentes)} artigos disponíveis")
        print("\n📂 CATEGORIAS:")
        cats = list(categorias.keys())
        for i, cat in enumerate(cats, 1):
            titulo = self.get_nome_categoria_traduzido(cat, idioma)
            print(f"  {i}. {titulo} ({len(categorias[cat])} artigos)")
        
        print("\n  [0] Todas as categorias")
        
        opcao = input("\n➡️  ").strip()
        
        if opcao == '0':
            artigos_selecionados = pendentes
        elif opcao.isdigit() and 1 <= int(opcao) <= len(cats):
            cat_selecionada = cats[int(opcao) - 1]
            artigos_selecionados = categorias[cat_selecionada]
        else:
            print("❌ Opção inválida")
            input("\nPressione Enter...")
            return
        
        if not artigos_selecionados:
            print("❌ Nenhum artigo selecionado")
            input("\nPressione Enter...")
            return
        
        print(f"\n🎯 Quantos publicar? (máx {len(artigos_selecionados)})")
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
            print(f"\n[{i}/{len(publicar_agora)}] {a.get('artigo')}")
            data_pub = (datetime.now() + timedelta(days=i-1)).strftime("%Y-%m-%d")
            a['data_publicacao'] = data_pub
            self.criar_artigo(a, revisar=True, idioma=idioma, forcar_head=False)
            if i < len(publicar_agora):
                time.sleep(random.randint(2, 5))
        
        self.criar_index(idioma=idioma)
        self.criar_todas_categorias(idioma=idioma)
        self.criar_sitemap()
        self.criar_index_raiz()
        
        print("\n" + "=" * 40)
        print(f"✅ {len(publicar_agora)} artigos publicados!")
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
        
        categorias = {}
        for a in artigos:
            cat = a.get('categoria', 'geral')
            if cat not in categorias:
                categorias[cat] = []
            categorias[cat].append(a)
        
        for cat, arts in categorias.items():
            titulo_cat = self.get_nome_categoria_traduzido(cat, idioma)
            publicados = sum(1 for a in arts if a.get('status') == 'publicado')
            print(f"  📂 {titulo_cat}: {publicados}/{len(arts)}")
        
        input("\nPressione Enter...")
    
    # ==================== SELECIONAR IDIOMA ====================
    
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
    
    # ==================== MOSTRAR PAINEL ====================
    
    def mostrar_painel(self):
        if self.idioma_selecionado is None:
            return
        
        idioma = self.idioma_selecionado
        artigos = self.ler_csv(idioma)
        total = len(artigos)
        
        publicados = 0
        rascunhos = 0
        categorias = self.get_categorias_do_idioma(idioma)
        
        for a in artigos:
            status = a.get('status', 'rascunho').lower()
            if status == 'publicado':
                publicados += 1
            else:
                rascunhos += 1
        
        print("\n" + "=" * 70)
        print(f"  {self.config.get('icone', '✈️')} {self.get_nome_site_simples(idioma)} - {idioma.upper()}")
        print("=" * 70)
        print(f"  📊 {total} artigos | ✅ {publicados} publicados | ⏳ {rascunhos} rascunhos")
        print(f"  🏷️  {len(categorias)} categorias: {', '.join([self.get_nome_categoria_traduzido(c, idioma) for c in list(categorias)[:5]])}")
        print("=" * 70)
    
    # ==================== CALENDÁRIO ====================
    
    def gerenciar_calendario(self):
        """
        📅 GERENCIAR CALENDÁRIO DE PUBLICAÇÕES
        Mostra todos os artigos com data em ordem cronológica.
        Permite editar data, título, categoria e status.
        """
        if self.idioma_selecionado is None:
            print("⚠️ Selecione um idioma primeiro!")
            return

        idioma = self.idioma_selecionado
        artigos = self.ler_csv(idioma)

        if not artigos:
            print("📭 Nenhum artigo encontrado.")
            input("\nPressione Enter...")
            return

        # Filtra artigos com data
        artigos_com_data = [a for a in artigos if a.get('data_publicacao')]

        if not artigos_com_data:
            print("⚠️ Nenhum artigo com data definida.")
            print("   Use a opção 'Publicar UM' para definir a data de um artigo.")
            input("\nPressione Enter...")
            return

        # Ordena por data
        artigos_com_data.sort(key=lambda x: x['data_publicacao'])

        hoje = datetime.now().strftime("%Y-%m-%d")

        while True:
            print("\n" + "=" * 80)
            print(f"📅 CALENDÁRIO DE PUBLICAÇÃO ({idioma.upper()})")
            print("=" * 80)
            print(f"{'Nº':<4} {'Data':<12} {'Status':<10} {'Artigo':<45} {'Categoria':<12}")
            print("-" * 80)

            for i, a in enumerate(artigos_com_data, 1):
                data = a.get('data_publicacao', '')
                titulo = a.get('artigo', '')[:42]
                if len(a.get('artigo', '')) > 42:
                    titulo += '...'
                categoria = a.get('categoria', '')[:11]
                status = "✅ Publicado" if data <= hoje else "⏳ Agendado"
                print(f"{i:<4} {data:<12} {status:<10} {titulo:<45} {categoria:<12}")

            print("=" * 80)
            print("  [0] Voltar")
            print("  [Nº] Editar artigo (ex: 5)")
            print("  [D] Definir data para artigos sem data")
            print("-" * 80)

            opcao = input("\n👉 Escolha: ").strip()

            if opcao == "0":
                break
            elif opcao.lower() == "d":
                self._definir_data_artigos_sem_data(artigos, idioma)
            elif opcao.isdigit():
                idx = int(opcao)
                if 1 <= idx <= len(artigos_com_data):
                    self._editar_artigo_calendario(artigos_com_data[idx - 1], idioma, artigos)
                else:
                    print("❌ Número inválido!")
                    input("\nPressione Enter...")
            else:
                print("❌ Opção inválida!")
                input("\nPressione Enter...")

    def _editar_artigo_calendario(self, artigo, idioma, todos_artigos):
        """
        📝 EDITAR ARTIGO NO CALENDÁRIO
        Edita data, título, categoria e status de um artigo específico.
        """
        print("\n" + "=" * 80)
        print(f"📝 EDITANDO ARTIGO")
        print("=" * 80)
        print(f"  Título atual: {artigo.get('artigo', '')}")
        print(f"  Data atual:   {artigo.get('data_publicacao', '')}")
        print(f"  Categoria:    {artigo.get('categoria', '')}")
        print(f"  Status:       {artigo.get('status', 'rascunho')}")
        print("=" * 80)

        print("\nO que você quer editar?")
        print("  [1] Data de publicação")
        print("  [2] Título")
        print("  [3] Categoria")
        print("  [4] Status (rascunho/publicado)")
        print("  [5] Tudo isso")
        print("  [0] Voltar")

        opcao = input("\n👉 Escolha: ").strip()

        if opcao == "0":
            return

        # Edita data
        if opcao in ["1", "5"]:
            nova_data = input("📅 Nova data (YYYY-MM-DD): ").strip()
            if nova_data:
                try:
                    datetime.strptime(nova_data, "%Y-%m-%d")
                    artigo['data_publicacao'] = nova_data
                    print(f"   ✅ Data atualizada para {nova_data}")
                except ValueError:
                    print("   ❌ Data inválida! Use o formato YYYY-MM-DD")

        # Edita título
        if opcao in ["2", "5"]:
            novo_titulo = input("📝 Novo título: ").strip()
            if novo_titulo:
                artigo['artigo'] = novo_titulo
                novo_slug = self.criar_slug(novo_titulo)
                artigo['slug'] = novo_slug
                print(f"   ✅ Título atualizado para: {novo_titulo}")
                print(f"   ✅ Slug atualizado para: {novo_slug}")

        # Edita categoria
        if opcao in ["3", "5"]:
            categorias = self.get_categorias_do_idioma(idioma)
            if categorias:
                print("\n📂 Categorias disponíveis:")
                for i, cat in enumerate(categorias, 1):
                    print(f"  {i}. {cat}")
                escolha_cat = input("👉 Escolha o número da nova categoria: ").strip()
                if escolha_cat.isdigit():
                    idx_cat = int(escolha_cat) - 1
                    if 0 <= idx_cat < len(categorias):
                        artigo['categoria'] = categorias[idx_cat]
                        print(f"   ✅ Categoria atualizada para: {categorias[idx_cat]}")
                    else:
                        print("   ❌ Categoria inválida!")
            else:
                nova_categoria = input("📂 Nova categoria: ").strip()
                if nova_categoria:
                    artigo['categoria'] = nova_categoria
                    print(f"   ✅ Categoria atualizada para: {nova_categoria}")

        # Edita status
        if opcao in ["4", "5"]:
            novo_status = input("📌 Novo status (rascunho/publicado): ").strip().lower()
            if novo_status in ['rascunho', 'publicado']:
                artigo['status'] = novo_status
                print(f"   ✅ Status atualizado para: {novo_status}")
            else:
                print("   ❌ Status inválido! Use 'rascunho' ou 'publicado'")

        self.salvar_csv(todos_artigos, idioma)
        print("\n✅ Alterações salvas com sucesso!")

        if artigo['status'] == 'publicado':
            gerar = input("\n🔄 Gerar o artigo agora? (s/n): ").strip().lower()
            if gerar in ['s', 'sim']:
                self.criar_artigo(artigo, forcar=True, revisar=False, idioma=idioma, forcar_head=True)
                print("   ✅ Artigo gerado!")
                self.criar_index(idioma=idioma)
                self.criar_todas_categorias(idioma=idioma)
                self.criar_sitemap()

        input("\nPressione Enter para continuar...")

    def _definir_data_artigos_sem_data(self, artigos, idioma):
        """
        📅 DEFINIR DATA PARA ARTIGOS SEM DATA
        Permite definir data em lote para artigos que não têm data.
        """
        artigos_sem_data = [a for a in artigos if not a.get('data_publicacao')]

        if not artigos_sem_data:
            print("✅ Todos os artigos já têm data definida!")
            input("\nPressione Enter...")
            return

        print("\n" + "=" * 80)
        print(f"📅 ARTIGOS SEM DATA DEFINIDA ({len(artigos_sem_data)})")
        print("=" * 80)

        for i, a in enumerate(artigos_sem_data, 1):
            print(f"  {i}. {a.get('artigo', '')[:60]}")

        print("=" * 80)

        data_base = input("\n📅 Data base (YYYY-MM-DD): ").strip()

        try:
            datetime.strptime(data_base, "%Y-%m-%d")
        except ValueError:
            print("❌ Data inválida! Use o formato YYYY-MM-DD")
            input("\nPressione Enter...")
            return

        intervalo = input("📆 Intervalo entre artigos (dias, padrão 1): ").strip()
        if not intervalo:
            intervalo = 1
        else:
            try:
                intervalo = int(intervalo)
            except ValueError:
                print("⚠️ Valor inválido, usando intervalo de 1 dia")
                intervalo = 1

        print("\n🔄 Aplicando datas...")

        data_atual = datetime.strptime(data_base, "%Y-%m-%d")

        for i, a in enumerate(artigos_sem_data):
            data_str = data_atual.strftime("%Y-%m-%d")
            a['data_publicacao'] = data_str
            print(f"   {i+1}. {a.get('artigo', '')[:40]} → {data_str}")
            data_atual += timedelta(days=intervalo)

        self.salvar_csv(artigos, idioma)
        print(f"\n✅ {len(artigos_sem_data)} artigos atualizados com datas!")
        input("\nPressione Enter para continuar...")

    # ==================== MENU ====================
    
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
            print("  [6] 🖼️ Gerenciar imagem do artigo")
            
            print(f"\n🔄 FERRAMENTAS ({self.idioma_selecionado.upper()})")
            print("  [7] 🔄 SINCRONIZAR TUDO (docs + CSV + páginas + sitemap)")
            print("  [8] Deletar artigo (remove pasta + CSV)")
            print("  [9] 🔍 Diagnosticar problemas")
            print("  [11] 🚀 GERAR TODOS OS IDIOMAS (PT → EN + ES)")
            print("  [12] 📅 Gerenciar calendário de publicações")
            
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
                self.gerenciar_imagem_artigo()
            elif opcao == "7":
                print("\n⚠️ SINCRONIZAÇÃO COMPLETA!")
                print("   📂 docs → LER artigos")
                print("   📄 CSV → ATUALIZAR")
                print("   🌐 Index, Categorias, Sitemap → REGENERAR")
                print("   📄 Páginas estáticas → GERAR")
                print("   🔥 A PASTA DOCS É A FONTE DA VERDADE!")
                print("   📌 Rascunhos no CSV → MANTIDOS")
                print("   🗑️ Publicados sem pasta → REMOVIDOS")
                print("   🗑️ Categorias sem pasta → REMOVIDAS")
                print("   📄 Artigos → REGENERADOS COMPLETAMENTE")
                if self.ler_sim_nao("\nContinuar? (s/n): "):
                    self.sincronizar_agora()
            elif opcao == "8":
                self.deletar_artigo()
            elif opcao == "9":
                self.diagnosticar_problemas()
            elif opcao == "10":
                self.idioma_selecionado = None
                self.t = IDIOMAS.get('pt', IDIOMAS['pt'])
                continue
            elif opcao == "11":
                self.gerar_todos_idiomas()
            elif opcao == "12":
                self.gerenciar_calendario()
            elif opcao == "0":
                print("\n👋 Até logo!")
                break
            else:
                print("❌ Opção inválida")
                input("\nPressione Enter...")

if __name__ == "__main__":
    import sys
    
    if "--auto" in sys.argv:
        gerador = Gerador()
        gerador.idioma_selecionado = 'pt'
        gerador.t = IDIOMAS.get('pt', IDIOMAS['pt'])
        gerador.publicar_lotes()
    else:
        gerador = Gerador()
        gerador.menu()