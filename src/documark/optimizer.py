import re


def optimize(md_text: str) -> str:
    text = md_text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"(#{1,6})([^ #\n])", r"\1 \2", text)
    return text.strip() + "\n"
