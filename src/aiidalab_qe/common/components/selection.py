import typing as t

import solara


@solara.component
def ToggleButtons(
    value: solara.Reactive,
    options: dict[str, dict[str, str]],
    on_value: t.Optional[t.Callable] = None,
    label: t.Optional[str] = None,
    class_: str = "",
):
    with solara.Row(classes=["control"]):
        if label is not None:
            solara.Text(label, classes=["control-label"])
        with solara.ToggleButtonsSingle(
            value=value,
            on_value=on_value,
            dense=True,
            classes=["toggle-buttons", *class_.split()],
        ):
            for option, data in options.items():
                solara.Button(
                    label=data.get("label", option),
                    tooltip=data.get("description", ""),
                    value=option,
                    style="width: 100px;",
                )
