import typing as t

import solara


@solara.component
def HubbardUParameterInput(
    label: str,
    u_parameter: float,
    on_change: t.Callable[[float], None],
):
    return solara.InputFloat(
        label=label,
        value=u_parameter,
        on_value=on_change,
    )
