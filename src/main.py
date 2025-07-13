from functions import text_to_textnodes, copy_static_public
import os
import shutil

def main():
    source = "./static"
    destination = "./public"

    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)

    copy_static_public(source, destination)

    

if __name__ == "__main__":
    main()