from enum import Enum

class BlockType(Enum):

    CODE = "code"
    PARAGRAPH = "paragraph"
    ULIST = "ulist"
    OLIST = "olist"
    HEADING = "heading"
    QUOTE = "quote"

def markdown_to_blocks(markdown):
    new_list = []
    text = markdown.strip()
    split_text = text.split("\n\n")

    for item in split_text:
        item = item.strip()
        
        if item != "":
            new_list.append(item)
    return new_list

def block_to_block_type(block):

    split = block.split(" ")
    result = True

    if len(split[0]) > 6 or len(split[0]) < 1:
        result = False
    for i in split[0]:
        if i != "#":
            result = False
    if len(block) < len(split[0]) + 2:
        result = False
    if len(split) == 1:
        result = False
    if result == True:
        return BlockType.HEADING


    if len(block) >= 6:
        if block[0:3] == "```" and block[len(block) - 3:len(block)] == "```":
            return BlockType.CODE
    
    if "\n" in block:
        list_block = block.split("\n")
        result = True

        for item in list_block:
            if item == "":
                result = False
                break
            if item[0] != ">":
                result = False

        if result == True:
            return BlockType.QUOTE

        result = True

        for item in list_block:
            if item == "":
                result = False
                break
            if item[0:2] != "- ":
                result = False
        if result == True:
            return BlockType.ULIST
        
        result = True
        count = 1

        for item in list_block:
            string = str(count)
            if item == "":
                result = False
                break
            if not item.startswith(f"{string}. "):
                result = False
            count += 1

        if result == True:
            return BlockType.OLIST
    return BlockType.PARAGRAPH
