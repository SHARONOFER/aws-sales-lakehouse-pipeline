import csv
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "sample_sales.csv"

sales_data = [
    {"order_id": 1, "customer_id": 101, "product_id": 501, "order_date": "2026-06-01", "quantity": 2, "price": 120, "country": "Israel"},
    {"order_id": 2, "customer_id": 102, "product_id": 502, "order_date": "2026-06-02", "quantity": 1, "price": 300, "country": "USA"},
    {"order_id": 3, "customer_id": 103, "product_id": 503, "order_date": "2026-06-03", "quantity": 5, "price": 40, "country": "Israel"},
    {"order_id": 4, "customer_id": 104, "product_id": 504, "order_date": "2026-06-04", "quantity": 3, "price": 75, "country": "Germany"},
    {"order_id": 5, "customer_id": 105, "product_id": 505, "order_date": "2026-06-05", "quantity": 4, "price": 55, "country": "France"},
]

DATA_DIR.mkdir(exist_ok=True)

with OUTPUT_FILE.open(mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=sales_data[0].keys())
    writer.writeheader()
    writer.writerows(sales_data)

print(f"Sample sales data created: {OUTPUT_FILE}")
