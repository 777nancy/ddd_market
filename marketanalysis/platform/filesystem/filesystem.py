import glob
import logging
import os
import shutil

import boto3
import pandas as pd
import s3fs

from marketanalysis.platform.filesystem.interface import AbstractFileSystem

logger = logging.getLogger(__name__)


class LocalFileSystem(AbstractFileSystem):
    def write(self, df: pd.DataFrame, file_dir: str, file_name_base: str, forced_removal=True):
        if forced_removal and os.path.exists(file_dir):
            self.remove(file_dir)

        file_name = f"{file_name_base}.pkl"
        os.makedirs(file_dir)
        file_path = os.path.join(file_dir, file_name)
        logger.info(f"file_path: {file_path}")
        df.to_pickle(file_path)

    def read(self, file_dir: str):
        files = glob.glob(os.path.join(file_dir, "*.pkl"))
        df_list = [pd.read_pickle(file) for file in files]

        return pd.concat(df_list, axis=0, ignore_index=True)

    def remove(self, file_dir):
        shutil.rmtree(file_dir)


class S3FileSystem(AbstractFileSystem):
    def __init__(self) -> None:
        self.s3 = boto3.resource("s3")
        s3fs.S3FileSystem(anon=False)

    def write(self, df: pd.DataFrame, file_dir: str, file_name_base: str, forced_removal=True):
        if forced_removal:
            self.remove(file_dir)
        file_name = f"{file_name_base}.pkl"

        file_path = "/".join([r"s3:", file_dir, file_name])
        logger.info(f"file_path: {file_path}")
        df.to_pickle(file_path)

    def read(self, file_dir: str):
        file_path_list = file_dir.split(os.path.sep)
        bucket_name = file_path_list[1]

        logger.info(f"bucket_name: {bucket_name}")
        bucket = self.s3.Bucket(bucket_name)  # type: ignore
        prefix_objs = bucket.objects.filter(Prefix="/".join(file_path_list[2:]))
        df_list = [pd.read_pickle(obj.get()["Body"]) for obj in prefix_objs]

        return pd.concat(df_list, axis=0, ignore_index=True)

    def remove(self, file_dir):
        file_path_list = file_dir.split(os.path.sep)
        bucket_name = file_path_list[1]
        bucket = self.s3.Bucket(bucket_name)  # type: ignore
        bucket.objects.filter(Prefix="/".join(file_path_list[2:])).delete()


def create_filesystem() -> AbstractFileSystem:
    environment = os.environ.get("ENVIRONMENT", "local")
    if environment == "local":
        return LocalFileSystem()

    else:
        return S3FileSystem()
