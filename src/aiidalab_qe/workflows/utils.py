from aiida import orm
from aiida.engine import ProcessBuilderNamespace

from aiidalab_qe.common.types import StructureType

from .qe import QeAppWorkChain


def create_builder(
    input_structure: StructureType,
    parameters: dict,
) -> ProcessBuilderNamespace:
    codes = parameters["codes"]["global"]["codes"]
    builder = QeAppWorkChain.get_builder_from_protocol(input_structure, parameters)
    if "relax" in builder:
        builder.relax.base.pw.metadata.options.resources = {
            "num_machines": codes.get("quantumespresso__pw")["nodes"],
            "num_mpiprocs_per_machine": codes.get("quantumespresso__pw")[
                "ntasks_per_node"
            ],
            "num_cores_per_mpiproc": codes.get("quantumespresso__pw")["cpus_per_task"],
        }
        mws = codes.get("quantumespresso__pw")["max_wallclock_seconds"]
        builder.relax.base.pw.metadata.options["max_wallclock_seconds"] = mws
        parallelization = codes["quantumespresso__pw"]["parallelization"]
        builder.relax.base.pw.parallelization = orm.Dict(dict=parallelization)
    return builder
