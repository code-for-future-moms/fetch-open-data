import os

directory = "./text"
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    print("python extract2.py {}".format(f))