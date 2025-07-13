from htmlnode import LeafNode , HTMLNode, ParentNode
from textnode import TextType, TextNode
from markdown_blocks import block_to_block_type, BlockType, markdown_to_blocks
import re 

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": f'{text_node.url}'})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": f'{text_node.url}', "alt": f'{text_node.text}'})
    raise Exception("not from acceptable types")




def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            result.append(node)
        else:
            split_list = node.text.split(delimiter)
            if len(split_list) % 2 == 0:
                raise Exception("Invalid markdown syntax")

            for i, part in enumerate(split_list):
                if split_list[i] == "":
                    continue
                if i % 2 == 0:  # Even index = regular text
                    result.append(TextNode(part, TextType.TEXT))
                else:  # Odd index = delimited text
                    result.append(TextNode(part, text_type))
    return result

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches



def split_nodes_image(old_nodes):
    node_result_list = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)

        if not images:
            node_result_list.append(node)
            continue
        
        whole_text = node.text
        
        for image in images:
            cut = whole_text.split(f"![{image[0]}]({image[1]})")
            if cut[0]:
                node_result_list.append(TextNode(cut[0], TextType.TEXT))
            node_result_list.append(TextNode(image[0] ,TextType.IMAGE, image[1]))
            whole_text = whole_text.split(f"{cut[0]}![{image[0]}]({image[1]})")[1]
        
        if whole_text != "":
            node_result_list.append(TextNode(whole_text, TextType.TEXT))
    
    return node_result_list
    



def split_nodes_link(old_nodes):
    node_result_list = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)

        if not links:
            node_result_list.append(node)
            continue
        
        whole_text = node.text
        
        for link in links:
            cut = whole_text.split(f"[{link[0]}]({link[1]})")
            if cut[0]:
                node_result_list.append(TextNode(cut[0], TextType.TEXT))
            node_result_list.append(TextNode(link[0] ,TextType.LINK, link[1]))
            whole_text = whole_text.split(f"{cut[0]}[{link[0]}]({link[1]})")[1]
        
        if whole_text != "":
            node_result_list.append(TextNode(whole_text, TextType.TEXT))
        
    return node_result_list

def text_to_textnodes(text):
    text_node = [TextNode(text, TextType.TEXT)]
    first = split_nodes_image(text_node)
    second = split_nodes_link(first)
    third = split_nodes_delimiter(second, "**", TextType.BOLD)
    fourth = split_nodes_delimiter(third, "_", TextType.ITALIC)
    fifth = split_nodes_delimiter(fourth, "`", TextType.CODE)
    return fifth


def text_to_children(text):
    text_node_list = text_to_textnodes(text)
    html_node_list = []
    for text_node in text_node_list:
        html_node_list.append(text_node_to_html_node(text_node))
    return html_node_list

def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    html_blocks = []
    
    for block in block_list:
        block_type = block_to_block_type(block)
        
        if block_type != BlockType.CODE:
            if block_type == BlockType.PARAGRAPH:
                block_tag = "p"
                list_children = text_to_children(block) 
                block_html = HTMLNode(block_tag, None, list_children)

            if block_type == BlockType.HEADING:
                block_tag = "h" + str(len(block) - len(block.lstrip("#"))) 
                block_text = block.lstrip("#").lstrip()
                list_children = text_to_children(block_text)
                block_html = HTMLNode(block_tag, None, list_children)

            if block_type == BlockType.QUOTE:
                block_tag = "blockquote"
                complete = []
                split_quote = block.split("\n")
                
                for item in split_quote:
                    complete.append(item.lstrip("> "))
                block_text = "\n".join(complete)

                list_children = text_to_children(block_text)
                block_html = HTMLNode(block_tag, None, list_children)


            if block_type == BlockType.ULIST:
                block_tag = "ul"
                split_block = block.split("\n")
                list_nodes = []
                html_element_list = []

                for item in split_block:
                    if item.startswith("*"):
                        list_nodes.append(item.lstrip("* "))
                    if item.startswith("-"):
                        list_nodes.append(item.lstrip("- "))
                    if item.startswith("+"):
                        list_nodes.append(item.lstrip("+ "))

                for item in list_nodes:
                    list_children = text_to_children(item)
                    html_element_list.append(HTMLNode("li", None, list_children))

                block_html = HTMLNode("ul", None, html_element_list)
                
            if block_type == BlockType.OLIST:
                block_tag = "ol"
                split_block = block.split("\n")
                list_nodes = []
                html_element_list = []
                counter = 1
                for item in split_block:
                    if item.startswith(str(counter) + "."):
                        list_nodes.append(item.lstrip(str(counter) + ". "))
                for item in list_nodes:
                    list_children = text_to_children(item)
                    html_element_list.append(HTMLNode("li", None, list_children)) 
                
                block_html = HTMLNode("ol", None, html_element_list)
        else:
            block_tag = "pre"
            code_tag = "code"
            block_text = block.strip("```")
            text_node = TextNode(block_text, TextType.CODE)
            code_html = text_node_to_html_node(text_node)
            block_html = HTMLNode(block_tag, None, [code_html])

        html_blocks.append(block_html)
    
    return HTMLNode("div", None, html_blocks)