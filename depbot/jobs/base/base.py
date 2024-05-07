import boto3
from botocore.exceptions import ClientError
from abc import ABC, abstractmethod
from ...utils import logger
from ..job_format import JobFormat
from dataclasses import dataclass


@dataclass
class BaseJob(ABC):
    """
    Abstract base class for all jobs.
    Provides common functionality and interface for all jobs.
    """

    client = None
    format: JobFormat = None

    @abstractmethod
    def setup(self):
        """
        Initializes the job by setting up necessary resources and configurations.
        This method can be overridden by concrete job classes to perform
        job-specific setup tasks.
        """
        pass

    @abstractmethod
    def run(self):
        """
        Abstract method to be implemented by concrete job classes.
        Defines the main logic and execution flow of the job.
        """
        pass
