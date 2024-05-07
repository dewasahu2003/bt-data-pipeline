from io import StringIO
import boto3

from depbot.utils import logger
from ..job_format import JobFormat
from ..base import BaseJob
from dataclasses import dataclass
import pandas as pd
from boto3.exceptions import ClientError
from .format import FileFormat
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class StoreJob(BaseJob):
    """
    Concrete implementation of the BaseJob class for storing data in s3
    """

    client = None
    format: JobFormat = JobFormat.STORAGE

    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.client = boto3.client(
            self.format.value,
        )

    def run(self):
        return super().run()

    @classmethod
    def save(
        self,
        file_type: FileFormat,
        df: pd.DataFrame,
        object_name: str,
    ):
        if file_type == FileFormat.CSV:
            self.save_csv(df, object_name)
            del df
        elif file_type == FileFormat.JSONL:
            self.save_jsonl(df, object_name)
            del df
        else:
            logger.error(f"Unsupported file type: {file_type}")

    def save_jsonl(self, df: pd.DataFrame, object_name: str):
        key = f"data/{object_name}.jsonl"
        bucket_name = "bot-data-wp"
        # process file
        json_buffer = StringIO()
        df.to_json(
            json_buffer,
            orient="records",
            lines=True,
            force_ascii=False,
        )
        # Upload the file
        try:
            response = self.client.put_object(
                ACL="private", Bucket=bucket_name, Key=key, Body=json_buffer.getvalue()
            )
            logger.info(f"Upload Successful : {response}")
        except ClientError as e:
            logger.error(f"Error occured :{e}")
            return False
        return True

    def save_csv(self, df: pd.DataFrame, object_name: str):
        key = f"data/{object_name}.csv"
        bucket_name = "bot-data-wp"

        # process file
        csv_buffer = StringIO()
        df.to_csv(csv_buffer)

        # Upload the file
        try:
            response = self.client.put_object(
                ACL="private", Bucket=bucket_name, Key=key, Body=csv_buffer.getvalue()
            )
            logger.info(f"Upload Successful : {response}")
        except ClientError as e:
            logger.error(f"Error occured :{e}")
            return False
        return True
