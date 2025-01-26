import solara
from solara.alias import rv


@solara.component
def CalculationHistory():
    print("\nrendering history page")
    with rv.Container(class_="mx-5 mt-2"):
        rv.Html(tag="h1", children=["Calculation history"])
