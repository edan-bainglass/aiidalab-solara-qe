from .parameters import ParametersConfigurationStep
from .properties import PropertiesSelectionStep
from .resources import ResourcesSelectionStep
from .results import ResultsStep
from .structure import StructureSelectionStep
from .submission import SubmissionStep

QE_WIZARD_STEPS = (
    {
        "title": "Select structure",
        "component": StructureSelectionStep,
    },
    {
        "title": "Select properties",
        "component": PropertiesSelectionStep,
    },
    {
        "title": "Configure workflow parameters",
        "component": ParametersConfigurationStep,
    },
    {
        "title": "Choose computational resources",
        "component": ResourcesSelectionStep,
    },
    {
        "title": "Submit workflow",
        "component": SubmissionStep,
        "is_submission_step": True,
    },
    {
        "title": "Status & results",
        "component": ResultsStep,
    },
)
