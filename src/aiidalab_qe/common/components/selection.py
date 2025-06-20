import typing as t

import solara


@solara.component
def ToggleButtons(
    value: solara.Reactive,
    options: t.Union[dict[str, dict[str, str]], tuple[str, ...]],
    on_value: t.Optional[t.Callable] = None,
    disabled: bool = False,
    label: t.Optional[str] = None,
    class_: str = "",
):
    if isinstance(options, tuple):
        options = {option: {"label": option} for option in options}
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
                    disabled=disabled,
                )
