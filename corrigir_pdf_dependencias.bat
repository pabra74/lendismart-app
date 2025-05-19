@echo off
echo Desinstalando versões antigas de FPDF...
pip uninstall -y fpdf
pip uninstall -y pyfpdf
echo Instalando fpdf2 correta...
pip install --upgrade fpdf2
echo.
echo Tudo concluído. Podes reiniciar a app no Streamlit.
pause