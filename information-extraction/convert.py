import os

directory = "./mydir"
out_dir = "./text"
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    pdf_name = filename.replace('.pdf', '.txt')
    output_path = os.path.join(out_dir, pdf_name)
    print("pdftotext -raw -layout -nopgbrk {} {}".format(f, output_path))