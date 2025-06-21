from __future__ import annotations

from dataclasses import dataclass, field

from aiida.plugins import DataFactory

UpfData = DataFactory("pseudo.upf")


@dataclass
class PseudoFamily:
    """The dataclass to deal with pseudo family strings.

    Attributes:
    library: the library name of the pseudo family, e.g. SSSP or PseudoDojo.
    cmd_library_name: the sub command name used in aiida-pseudo command line.
    version: the version of the pseudo family, e.g. 1.2
    functional: the functional of the pseudo family, e.g. PBE, PBEsol.
    accuracy: the accuracy of the pseudo family, which is protocol in aiida-pseudo, e.g. efficiency, precision, standard, stringent.
    relativistic: the relativistic treatment of the pseudo family, e.g. SR, FR.
    file_type: the file type of the pseudo family, e.g. upf, psml, currently only used for PseudoDojo.
    """

    library: str
    version: str
    functional: str
    accuracy: str
    cmd_library_name: str = field(init=False)
    relativistic: str | None = None
    file_type: str | None = None

    def __post_init__(self):
        """Post init operations and checks."""
        if self.library == "SSSP":
            self.cmd_library_name = "sssp"
        elif self.library == "PseudoDojo":
            self.cmd_library_name = "pseudo-dojo"
        else:
            raise ValueError(f"Unknown pseudo library {self.library}")

    @classmethod
    def from_string(cls, pseudo_family_string: str) -> PseudoFamily:
        """Initialize from a pseudo family string."""
        # We support two pseudo families: SSSP and PseudoDojo
        # They are formatted as follows:
        # SSSP: SSSP/<version>/<functional>/<accuracy>
        # PseudoDojo: PseudoDojo/<version>/<functional>/<relativistic>/<accuracy>/<file_type>
        # where <relativistic> is either 'SR' or 'FR' and <file_type> is either 'upf' or 'psml'
        # Before we unify the format of family strings, the conditions below are necessary
        # to distinguish between the two families
        library = pseudo_family_string.split("/")[0]
        if library == "SSSP":
            version, functional, accuracy = pseudo_family_string.split("/")[1:]
            relativistic = None
            file_type = None
        elif library == "PseudoDojo":
            (
                version,
                functional,
                relativistic,
                accuracy,
                file_type,
            ) = pseudo_family_string.split("/")[1:]
        else:
            raise ValueError(
                f"Not able to parse valid library name from {pseudo_family_string}"
            )

        return cls(
            library=library,
            version=version,
            functional=functional,
            accuracy=accuracy,
            relativistic=relativistic,
            file_type=file_type,
        )
