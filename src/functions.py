from htmlnode import LeafNode
from textnode import TextType, TextNode
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
