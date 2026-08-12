@echo off
chcp 65001 >nul
title Atualizando Site...

echo ========================================
echo  ATUALIZANDO SITE
echo ========================================
echo.

echo [1/3] Lendo pastas e atualizando INDEX...
python -c "import gerador; g=gerador.Gerador(); g.idioma_selecionado='pt'; g.criar_index()"
python -c "import gerador; g=gerador.Gerador(); g.idioma_selecionado='en'; g.criar_index()"
python -c "import gerador; g=gerador.Gerador(); g.idioma_selecionado='es'; g.criar_index()"

echo.
echo [2/3] Atualizando CATEGORIAS...
python -c "import gerador; g=gerador.Gerador(); g.idioma_selecionado='pt'; g.criar_todas_categorias()"
python -c "import gerador; g=gerador.Gerador(); g.idioma_selecionado='en'; g.criar_todas_categorias()"
python -c "import gerador; g=gerador.Gerador(); g.idioma_selecionado='es'; g.criar_todas_categorias()"

echo.
echo [3/3] Atualizando SITEMAP e RAIZ...
python -c "import gerador; g=gerador.Gerador(); g.criar_sitemap()"
python -c "import gerador; g=gerador.Gerador(); g.criar_index_raiz()"

echo.
echo ========================================
echo  ✅ SITE ATUALIZADO
echo ========================================
echo  📂 docs/ → LIDO (não sobrescrito)
echo  📄 CSVs → LIDOS (não sobrescritos)
echo  🖼️ Imagens → MANTIDAS
echo  🌐 Traduções → MANTIDAS
echo ========================================
pause