from functions import text_to_textnodes


def main():
    result = text_to_textnodes("Hello, this is **bold** and _italic_ and `code` and ![a bear](https://bear-images.org/bear.jpg) and a [link](https://boot.dev)")
    for i in result:
        print(i)

if __name__ == "__main__":
    main()