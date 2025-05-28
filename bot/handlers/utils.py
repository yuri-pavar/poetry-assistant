import re

def convert_poetry_blocks(text: str) -> str:
    lines = text.splitlines()
    in_poetry = False
    result = []
    block = []

    for line in lines:
        if line.startswith(">"):
            in_poetry = True
            block.append(line[1:].strip())
        else:
            if in_poetry:
                result.append("<pre>" + "\n".join(block) + "</pre>")
                block = []
                in_poetry = False
            result.append(line)
    if block:
        result.append("<pre>" + "\n".join(block) + "</pre>")

    return "\n".join(result)


def convert_inline_formatting(text: str) -> str:
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'_(.+?)_', r'<i>\1</i>', text)

    return text


def convert_code_blocks_to_pre(text: str) -> str:
    return re.sub(r'```(?:\w*\n)?(.*?)```', r'<pre>\1</pre>', text, flags=re.DOTALL)

def prepare_for_html(text: str) -> str:
    text = convert_poetry_blocks(text)
    text = convert_inline_formatting(text)
    text = convert_code_blocks_to_pre(text)

    return text
