from __future__ import annotations

import solara


@solara.component
def Tester():
    print("\nrendering resources page")
    with solara.Sidebar():
        solara.Text("I am in the sidebar of the wrapping layout component")
    with solara.v.Container(class_="mx-5 mt-2"):
        solara.v.Html(tag="h1", children=["Tester"])
