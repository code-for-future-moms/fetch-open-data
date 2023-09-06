import os
import subprocess

in_dir = "./mydir" # pdf files are located here
out_dir = "./text"
for filename in os.listdir(in_dir):
    f = os.path.join(in_dir, filename)
    pdf_name = filename.replace('.pdf', '.txt')
    output_path = os.path.join(out_dir, pdf_name)
    subprocess.run(["pdftotext", "-raw", "-layout", "-nopgbrk", f, output_path])