import argparse  # עיבוד ארגומנטים משורת הפקודה
import os  # פונקציות מערכת (קבצים, משתני סביבה)
import time  # פונקציות זמן (sleep ומדידות זמן)
from pathlib import Path  # עבודה נוחה עם נתיבי קבצים

import boto3  # AWS SDK לעבודה עם שירותי AWS
from botocore.exceptions import ClientError, NoCredentialsError, ProfileNotFound  # חריגות AWS נפוצות


DEFAULT_AWS_CONFIG_DIR = r"D:\aws_config"
DEFAULT_AWS_PROFILE = "sales-lakehouse"
DEFAULT_AWS_REGION = "eu-west-1"
DEFAULT_DATABASE = "sales_lakehouse"
DEFAULT_OUTPUT_LOCATION = "s3://sharon-sales-lakehouse-pipeline/athena-results/"


def configure_aws_environment(aws_config_dir: str, profile: str, region: str) -> None:
    """מגדיר את AWS SDK כך שיכיר את קבצי ה־credentials וה־config ו־profile."""

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
    """יוצר ומחזיר `boto3.Session` עם פרופיל ואזור נתונים."""

    return boto3.Session(
        profile_name=profile,
        region_name=region,
    )



def start_athena_query(
    session: boto3.Session,
    query: str,
    database: str,
    output_location: str,
) -> str:
    athena_client = session.client("athena")

    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            "Database": database,
        },
        ResultConfiguration={
            "OutputLocation": output_location,
        },
    )
    return response["QueryExecutionId"]


def wait_for_query_to_finish(
    session: boto3.Session,
    query_execution_id: str,
) -> dict:
    athena_client = session.client("athena")

    while True:
        response = athena_client.get_query_execution(
            QueryExecutionId=query_execution_id
        )

        status = response["QueryExecution"]["Status"]["State"]

        if status in ["SUCCEEDED", "FAILED", "CANCELLED"]:
            return response

        print(f"Query status: {status}")
        time.sleep(2)


def print_query_summary(response: dict) -> None:
    query_execution = response["QueryExecution"]
    status = query_execution["Status"]["State"]

    print(f"Final query status: {status}")

    if status == "SUCCEEDED":
        output_location = query_execution["ResultConfiguration"]["OutputLocation"]

        statistics = query_execution.get("Statistics", {})
        data_scanned_bytes = statistics.get("DataScannedInBytes", 0)

        print("Athena query completed successfully.")
        print(f"Result location: {output_location}")
        print(f"Data scanned: {data_scanned_bytes} bytes")

    else:
        reason = query_execution["Status"].get("StateChangeReason", "Unknown reason")
        print(f"Athena query did not succeed. Reason: {reason}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run an Athena query using boto3."
    )

    parser.add_argument(
        "--query",
        required=True,
        help="SQL query to run in Athena.",
    )

    parser.add_argument(
        "--database",
        default=DEFAULT_DATABASE,
        help="Athena database name.",
    )

    parser.add_argument(
        "--output-location",
        default=DEFAULT_OUTPUT_LOCATION,
        help="S3 location for Athena query results.",
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
        "--debug",
        action="store_true",
        help="Print detailed debug logs for each execution step.",
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

    query_execution_id = start_athena_query(
        session=session,
        query=args.query,
        database=args.database,
        output_location=args.output_location,
    )

    print(f"Started Athena query.")
    print(f"QueryExecutionId: {query_execution_id}")

    response = wait_for_query_to_finish(
        session=session,
        query_execution_id=query_execution_id,
    )

    print_query_summary(response)


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