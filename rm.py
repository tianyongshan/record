import os

for filename in os.listdir('.'):
    if filename.endswith('.epub'):
        new_filename = filename.replace(' ', '')
        os.rename(filename, new_filename)
