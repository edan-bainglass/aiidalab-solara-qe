import solara


def Paragraph(text: str):
    return solara.HTML("p", text, style="margin-bottom: 10px;")
