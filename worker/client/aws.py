
import boto3
import botocore

from worker.config import config

session = boto3.session.Session()

s3_client = session.client(
    service_name='s3',
    endpoint_url=config.aws.endpoint,
    aws_access_key_id=config.aws.key_id,
    aws_secret_access_key=config.aws.key,
)


class AWSClient():

    def download_image_by_name(self, filename: str, bucket: str, file_storage: str):
        try:
            s3_client.download_file(
                Bucket=bucket,
                Key=filename,
                Filename=f'{file_storage}/{filename}'
            )
        except botocore.exceptions.ClientError:
            pass


aws_client = AWSClient()
