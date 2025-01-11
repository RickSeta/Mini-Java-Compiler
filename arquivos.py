import os

def read_text_files(directory):
    file_contents = {}
    for filename in os.listdir(directory):
        if not filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                file_contents[filename] = file.read()
    return file_contents

def append_to_file(filename, text, dir=None):
    if dir:
        filename = os.path.join(dir, filename)
    with open(filename, 'a', encoding='utf-8') as file:

        file.write(text + '\n')

def erase_file_content(filename, dir=None):
    if dir:
        filename = os.path.join(dir, filename)
    open(filename, 'w').close()