from copy import deepcopy

import solara


@solara.component
def EigenvaluesInput(
    kind_index: int,
    kind_name: str,
    num_states: int,
    eigenvalues: solara.Reactive[list[list[list[tuple[int, int, str, float]]]]],
):
    kind_eigenvalues = eigenvalues.value[kind_index]
    with solara.Row():
        with solara.Column():
            solara.Text(f"{kind_name}")
        with solara.Column():
            for spin_index, spin_label in enumerate(("Up", "Down")):
                with solara.Row():
                    solara.Text(spin_label)
                    for state_index in range(num_states):

                        def update_eigenvalue(
                            value: str,
                            state: int = state_index,
                            spin: int = spin_index,
                            kind: int = kind_index,
                        ):
                            eigvals = deepcopy(eigenvalues.value)
                            eigvals[kind][spin][state] = (
                                state,
                                spin,
                                kind_name,
                                float(value),
                            )
                            eigenvalues.set(eigvals)

                        eigenvalue = kind_eigenvalues[spin_index][state_index][-1]
                        solara.Select(
                            label=f"{state_index + 1}",
                            values=["-1", "0", "1"],
                            value=str(int(eigenvalue)),
                            on_value=update_eigenvalue,
                        )
