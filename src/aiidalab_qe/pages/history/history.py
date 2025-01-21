import solara
from solara.alias import rv


@solara.component
def CalculationHistory():
    with rv.Container(class_="mt-2"):
        rv.Html(tag="h1", children=["Calculation history"])
