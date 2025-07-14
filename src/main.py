from functions import copy_static_public, generate_page, find_md
import os
import shutil
import sys 

def main():

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    source = "static"
    destination = "docs"
    content = "content"
    page_list = find_md(content)
    
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)

    copy_static_public(source, destination)
    generate_page("content/index.md","template.html", "docs/index.html", basepath)
    
    for page in page_list:
        page_destination = "docs" + page.lstrip("content").rstrip(".md") + ".html"
        directory_destination = page_destination.rstrip(".index.html")
        
        if os.path.exists(directory_destination) == False:
            os.makedirs(directory_destination)
        
        generate_page(page, "template.html", page_destination, basepath)

if __name__ == "__main__":
    main()