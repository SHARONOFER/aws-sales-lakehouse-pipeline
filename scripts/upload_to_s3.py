import argparse
import os
from pathlib import Path

import boto3
from botocore.exceptions import ClientError, NoCredentialsError, ProfileNotFound


DEFAULT_AWS_CONFIG_DIR = r"D:\aws_config"
DEFAULT_AWS_PROFILE = "sales-lakehouse"
DEFAULT_AWS_REGION = "eu-west-1"
DEFAULT_LOCAL_FILE = "data/sample_sales.csv"
DEFAULT_S3_KEY = "raw/sales/sample_sales.csv"


def configure_aws_environment(aws_config_dir: str, profile: str, region: str) -> None:
    credentials_file = Path(aws_config_dir) / "credentials"
    config_file = Path(aws_config_dir) / "config"

    if not credentials_file.exists():
        raise FileNotFoundError(f"AWS credentials file not found: {credentials_file}")

    if not config_file.exists():
        raise FileNotFoundError(f"AWS config file not found: {config_file}")

    os.environ["AWS_SHARED_CREDENTIALS_FILE"] = str(credentials_file)
    os.environ["AWS_CONFIG_FILE"] = str(config_file)
    os.environ["AWS_PROFILE"] = profile
    os.environ["AWS_REGION"] = region


def create_boto3_session(profile: str, region: str) -> boto3.Session:
    return boto3.Session(
        profile_name=profile,
        region_name=region,
    )


def validate_aws_identity(session: boto3.Session) -> None:
    sts_client = session.client("sts")
    sts_client.get_caller_identity()
    print("AWS identity check passed.")


def upload_file_to_s3(
    session: boto3.Session,
    bucket_name: str,
    local_file: str,
    s3_key: str,
) -> None:
    local_path = Path(local_file)

    if not local_path.exists():
        raise FileNotFoundError(f"Local file not found: {local_path}")

    s3_client = session.client("s3")

    print(f"Uploading local file: {local_path}")
    print(f"Target S3 path: s3://{bucket_name}/{s3_key}")

    s3_client.upload_file(
        Filename=str(local_path),
        Bucket=bucket_name,
        Key=s3_key,
        ExtraArgs={
            "ContentType": "text/csv",
            "ServerSideEncryption": "AES256",
        },
    )

    response = s3_client.head_object(
        Bucket=bucket_name,
        Key=s3_key,
    )

    uploaded_size = response.get("ContentLength")

    print("Upload completed successfully.")
    print(f"S3 path: s3://{bucket_name}/{s3_key}")
    print(f"Uploaded size: {uploaded_size} bytes")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upload the local sales CSV file to Amazon S3."
    )

    parser.add_argument(
        "--bucket",
        required=True,
        help="Target S3 bucket name.",
    )

    parser.add_argument(
        "--aws-config-dir",
        default=DEFAULT_AWS_CONFIG_DIR,
        help="Local directory that contains AWS credentials and config files.",
    )

    parser.add_argument(
        "--profile",
        default=DEFAULT_AWS_PROFILE,
        help="AWS profile name.",
    )

    parser.add_argument(
        "--region",
        default=DEFAULT_AWS_REGION,
        help="AWS region.",
    )

    parser.add_argument(
        "--local-file",
        default=DEFAULT_LOCAL_FILE,
        help="Local file path to upload.",
    )

    parser.add_argument(
        "--s3-key",
        default=DEFAULT_S3_KEY,
        help="Target S3 object key.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    configure_aws_environment(
        aws_config_dir=args.aws_config_dir,
        profile=args.profile,
        region=args.region,
    )

    session = create_boto3_session(
        profile=args.profile,
        region=args.region,
    )

    validate_aws_identity(session)

    upload_file_to_s3(
        session=session,
        bucket_name=args.bucket,
        local_file=args.local_file,
        s3_key=args.s3_key,
    )


if __name__ == "__main__":
    try:
        main()

    except ProfileNotFound as error:
        print("AWS profile was not found.")
        print(error)
        raise

    except NoCredentialsError as error:
        print("AWS credentials were not found.")
        print(error)
        raise

    except ClientError as error:
        print("AWS returned an error.")
        print(error)
        raise