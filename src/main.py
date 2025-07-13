from functions import copy_static_public, generate_page, find_md
import os
import shutil

def main():
    source = "static"
    destination = "public"
    content = "content"
    page_list = find_md(content)
    
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)

    copy_static_public(source, destination)
    generate_page("content/index.md","template.html", "public/index.html")
    
    for page in page_list:
        page_destination = "public" + page.lstrip("content").rstrip(".md") + ".html"
        directory_destination = page_destination.rstrip(".index.html")
        
        if os.path.exists(directory_destination) == False:
            os.makedirs(directory_destination)
        
        generate_page(page, "template.html", page_destination)

if __name__ == "__main__":
    main()