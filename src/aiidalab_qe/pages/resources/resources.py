import solara
from solara.alias import rv


@solara.component
def ResourceSetup():
    with rv.Container(class_="mx-5 mt-2"):
        rv.Html(tag="h1", children=["Resource setup"])
