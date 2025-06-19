import io
import typing as t

import solara

from .utils import UpfData


@solara.component
def PseudoUploadComponent(
    kind_name: str,
    pseudo_filename: str,
    cutoffs: tuple[float, float],
    update: t.Callable[[str, str], None],
    disabled: bool = False,
):
    def store_and_update(file_info: dict):
        # TODO consider checking if a node with this filename already exists
        # TODO extract cutoffs from uploaded UPF file
        if disabled:
            # TODO remove this once FileDrop supports disabled state
            return
        filename: str = file_info["name"]
        content: bytes = file_info["data"]
        new_pseudo = UpfData(file=io.BytesIO(content), filename=filename)
        new_pseudo.store()
        update(new_pseudo.uuid, filename)

    with solara.Row(classes=["control", "pseudo-uploader"]):
        solara.Text(
            kind_name,
            classes=["pseudo-uploader-label"],
        )
        with solara.Div(class_="pseudo-uploader-filedrop"):
            solara.FileDrop(
                label=pseudo_filename,
                on_file=store_and_update,
                lazy=False,
                # disabled=disabled,  # TODO feature request or extend
            )
        solara.Text(f"ψ: {cutoffs[0]:.2f} Ry | ρ: {cutoffs[1]:.2f} Ry")
