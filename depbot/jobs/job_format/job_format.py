from enum import Enum


class JobFormat(Enum):
    """
    The JobFormat Enum class defines the different formats that the jobs can output to.
    """

    STORAGE = "s3"
    ORCHESTRAION_BRIDGE = "eventbridge"
    STEPS = "stepfunction"
    # check all other client name for others
