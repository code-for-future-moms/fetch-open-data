import os
import subprocess

in_dir = "./mydir" # pdf files are located here
out_dir = "./text"
for pdf_name in os.listdir(in_dir):
    f = os.path.join(in_dir, pdf_name)
    txt_name = pdf_name.replace('.pdf', '.txt')
    output_path = os.path.join(out_dir, txt_name)
    subprocess.run(["pdftotext", "-raw", "-layout", "-nopgbrk", f, output_path])