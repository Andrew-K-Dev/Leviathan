from fpdf import FPDF

def generate_info_pdf(data, filename="output_bundle.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Leviathan Market Report", ln=True, align='C')
    pdf.ln(10)
    for item in data:
        pdf.cell(200, 10, txt=f"{item['title']} - {item['price']}", ln=True)
        pdf.cell(200, 10, txt=item['url'], ln=True)
        pdf.ln(5)
    pdf.output(filename)
    return filename