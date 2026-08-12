@echo off
echo ✅ Servidor rodando em http://localhost:8002
cd docs
python -m http.server 8002
pause