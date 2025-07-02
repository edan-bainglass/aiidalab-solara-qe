import solara
import solara.server
import solara.server.fastapi
from aiida import engine, load_profile, orm
from aiida.calculations.arithmetic.add import ArithmeticAddCalculation
from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel

from aiidalab_qe.workflows.qe import QeAppWorkChain

_ = load_profile()

app = FastAPI()

router = APIRouter(prefix="/api/v1")


class WorkflowInput(BaseModel):
    label: str
    description: str
    structure_pk: int
    parameters: dict


@app.get("/")
def index():
    return {
        "message": "Usage: /app to run Solara app; /api/v1/<endpoint> for API calls"
    }


@router.get("/submit-calculation/test")
async def submit_calculation():
    try:
        code = orm.load_code("add@localhost")
        process_node = engine.submit(ArithmeticAddCalculation, x=1, y=2, code=code)
        return {"process_uuid": str(process_node.uuid)}
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err)) from err


@router.post("/submit-workflow")
async def submit_workflow(inputs: WorkflowInput):
    try:
        codes = inputs.parameters["codes"]["global"]["codes"]
        parameters = inputs.parameters
        input_structure = orm.load_node(inputs.structure_pk)
        builder = QeAppWorkChain.get_builder_from_protocol(input_structure, parameters)
        if "relax" in builder:
            builder.relax.base.pw.metadata.options.resources = {
                "num_machines": codes.get("quantumespresso__pw")["nodes"],
                "num_mpiprocs_per_machine": codes.get("quantumespresso__pw")[
                    "ntasks_per_node"
                ],
                "num_cores_per_mpiproc": codes.get("quantumespresso__pw")[
                    "cpus_per_task"
                ],
            }
            mws = codes.get("quantumespresso__pw")["max_wallclock_seconds"]
            builder.relax.base.pw.metadata.options["max_wallclock_seconds"] = mws
            parallelization = codes["quantumespresso__pw"]["parallelization"]
            builder.relax.base.pw.parallelization = orm.Dict(dict=parallelization)
        node = engine.submit(builder)
        return {"process_uuid": str(node.uuid)}
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err)) from err


app.include_router(router)

app.mount("/", app=solara.server.fastapi.app)
