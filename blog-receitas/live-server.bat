@echo off
echo ✅ Servidor rodando em http://localhost:8000
cd docs
python -m http.server 8000
pause