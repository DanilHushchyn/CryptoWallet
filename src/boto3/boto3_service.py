import base64
from io import BytesIO
import uuid
import logging
import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException
from config.settings import SPACES_ACCESS_KEY_ID, SPACES_SECRET_ACCESS_KEY, BUCKET
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

disable_warnings(InsecureRequestWarning)


class BotoService:
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name='fra1',
                            endpoint_url='https://crypto.fra1.digitaloceanspaces.com',
                            aws_access_key_id=SPACES_ACCESS_KEY_ID,
                            aws_secret_access_key=SPACES_SECRET_ACCESS_KEY,
                            verify=False
                            )

    @staticmethod
    async def upload_image(base64_image):
        try:
            base64_image = base64_image.split(',')[1]
            image_data = base64.b64decode(base64_image)
        except:
            raise HTTPException(status_code=401, detail='Base64 image error')
        unique_filename = str(uuid.uuid4()) + '.png'

        file_path = f'{unique_filename}'
        with BytesIO(image_data) as image_stream:
            try:
                BotoService.client.upload_fileobj(image_stream, BUCKET, file_path)
                BotoService.client.put_object_acl(
                    ACL='public-read',
                    Bucket=BUCKET,
                    Key=file_path,
                )
                url = f"https://{BUCKET}.fra1.digitaloceanspaces.com/{BUCKET}/{file_path}"
                return url
            except ClientError as e:
                logging.error(e)
                return False
