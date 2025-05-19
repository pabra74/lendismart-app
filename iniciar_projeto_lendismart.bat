@echo off
echo === Criar ambiente virtual ===
python -m venv venv

echo === Ativar ambiente virtual ===
call venv\Scripts\activate.bat

echo === Instalar dependências ===
pip install --upgrade pip
pip install -r requirements.txt

echo === Iniciar Streamlit ===
streamlit run main.py

pause