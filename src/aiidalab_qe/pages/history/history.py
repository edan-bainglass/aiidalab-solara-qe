import solara


@solara.component
def CalculationHistory():
    print("\nrendering history page")
    with solara.v.Container(class_="mx-5 mt-2"):
        solara.v.Html(tag="h1", children=["Calculation history"])
