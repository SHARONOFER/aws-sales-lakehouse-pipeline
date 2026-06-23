# AWS Sales Lakehouse Pipeline

A learning project that demonstrates a simple sales data lakehouse pipeline using Python, Docker, GitHub, and AWS services.

## Planned Architecture

Local Development:
- Python
- Docker
- VS Code
- Git and GitHub via SSH

AWS Pipeline:
- Amazon S3 for data storage
- AWS Glue for catalog and ETL
- Amazon Athena for querying data
- Amazon Redshift for future analytics layer

## Project Structure

```text
aws-sales-lakehouse-pipeline/
├── data/
├── scripts/
├── sql/
├── docs/
├── docker/
├── README.md
├── requirements.txt
├── .gitignore
└── docker-compose.yml
## Docker Basics

```text
Dockerfile
   ↓ docker build
Image
   ↓ docker run
Container
```

Meaning:

```text
Dockerfile = the recipe that defines how to build the environment
Image      = the ready package created from the Dockerfile
Container  = a live running instance of the Image
```

In this project:

```text
docker/Dockerfile
   ↓ docker build
aws-sales-lakehouse-pipeline:local
   ↓ docker run
Running container that executes the Python sales pipeline script
```

Dockerfile        = מתכון לבניית הסביבה
Image             = הסביבה המוכנה
docker-compose.yml = הוראות איך להריץ את הסביבה
Container         = ההרצה בפועל

Dockerfile
= איך לבנות Image

docker-compose.yml
= איך להריץ Container מה־Image

docker compose up
=
תבנה אם צריך
תיצור קונטיינר
תריץ את התוכנית
תציג לי את הפלט

sales-pipeline              = שם השירות ב-compose
aws-sales-lakehouse-pipeline:local = שם ה-Image
aws-sales-lakehouse-pipeline       = שם ה-Container