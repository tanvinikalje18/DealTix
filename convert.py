from markdown_pdf import MarkdownPdf, Section

pdf = MarkdownPdf(toc_level=2)
with open("DealTix_Project_Report.md", "r", encoding="utf-8") as f:
    text = f.read()

pdf.add_section(Section(text, toc=False))
pdf.save("DealTix_Project_Report.pdf")
print("PDF conversion successful")
