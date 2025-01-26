import solara
from solara.alias import rv


@solara.component
def ResourceSetup():
    print("rendering resources page")
    with rv.Container(class_="mx-5 mt-2"):
        rv.Html(tag="h1", children=["Resource setup"])
