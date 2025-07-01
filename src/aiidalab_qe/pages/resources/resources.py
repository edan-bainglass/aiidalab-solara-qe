import solara


@solara.component
def ResourceSetup():
    print("rendering resources page")
    with solara.v.Container(class_="mx-5 mt-2"):
        solara.v.Html(tag="h1", children=["Resource setup"])
