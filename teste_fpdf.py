from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Teste de PDF com fpdf2", ln=True)
pdf.output("teste.pdf")
print("PDF gerado com sucesso.")