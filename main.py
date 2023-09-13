import pdfkit

pdfkit.from_file('template.html', 'output.pdf', options={"enable-local-file-access": ""})

print(f"PDF generated")
