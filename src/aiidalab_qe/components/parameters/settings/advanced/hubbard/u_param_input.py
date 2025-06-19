import typing as t

import solara


@solara.component
def HubbardUParameterInput(
    label: str,
    u_parameter: float,
    on_change: t.Callable[[float], None],
    disabled: bool = False,
):
    return solara.InputFloat(
        label=label,
        value=u_parameter,
        on_value=on_change,
        disabled=disabled,
    )
