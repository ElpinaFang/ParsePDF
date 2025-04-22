import tabula

tables = tabula.read_pdf("PETAIR APPLICATION FORM.pdf", pages="all")
df = tables[0]
print(df)