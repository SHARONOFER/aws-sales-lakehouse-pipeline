import csv
import random
from datetime import date, timedelta
from pathlib import Path


# תיקיית היעד שבה יישמר קובץ הנתונים
DATA_DIR = Path("data")

# שם קובץ ה-CSV שניצור
OUTPUT_FILE = DATA_DIR / "sample_sales.csv"

# כדי שכל הרצה תייצר אותם נתונים בדיוק
# זה חשוב לפרויקט, בדיקות ו-Git
random.seed(42)


countries = [
    "Israel",
    "USA",
    "Germany",
    "France",
    "United Kingdom",
    "Netherlands",
    "Spain",
    "Italy",
]

sales_channels = [
    "Online",
    "Store",
    "Partner",
    "Marketplace",
]

payment_methods = [
    "Credit Card",
    "PayPal",
    "Bank Transfer",
    "Cash",
]

customer_segments = [
    "Private",
    "Small Business",
    "Enterprise",
]

products = [
    {"product_id": 501, "product_name": "Laptop", "category": "Electronics", "unit_price": 1200},
    {"product_id": 502, "product_name": "Monitor", "category": "Electronics", "unit_price": 300},
    {"product_id": 503, "product_name": "Keyboard", "category": "Accessories", "unit_price": 80},
    {"product_id": 504, "product_name": "Mouse", "category": "Accessories", "unit_price": 40},
    {"product_id": 505, "product_name": "Office Chair", "category": "Furniture", "unit_price": 250},
    {"product_id": 506, "product_name": "Desk", "category": "Furniture", "unit_price": 450},
    {"product_id": 507, "product_name": "Headphones", "category": "Audio", "unit_price": 150},
    {"product_id": 508, "product_name": "Webcam", "category": "Accessories", "unit_price": 110},
]


def random_order_date(start_date: date, days_range: int) -> str:
    """
    מחזיר תאריך אקראי בטווח נתון.
    """
    random_days = random.randint(0, days_range)
    return (start_date + timedelta(days=random_days)).isoformat()


def generate_sales_data(number_of_rows: int = 1000) -> list[dict]:
    """
    מייצר רשימת עסקאות מכירה לדוגמה.
    כל שורה מייצגת הזמנה אחת.
    """
    sales_data = []

    start_date = date(2026, 1, 1)

    for order_id in range(1, number_of_rows + 1):
        product = random.choice(products)
        quantity = random.randint(1, 10)

        # לפעמים נותנים הנחה קטנה כדי שהדאטה יהיה יותר ריאלי
        discount_percent = random.choice([0, 0, 0, 5, 10, 15])

        unit_price = product["unit_price"]
        gross_amount = quantity * unit_price
        discount_amount = gross_amount * discount_percent / 100
        total_amount = gross_amount - discount_amount

        row = {
            "order_id": order_id,
            "customer_id": random.randint(1000, 1999),
            "customer_segment": random.choice(customer_segments),
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "category": product["category"],
            "order_date": random_order_date(start_date, 364),
            "quantity": quantity,
            "unit_price": unit_price,
            "discount_percent": discount_percent,
            "total_amount": round(total_amount, 2),
            "country": random.choice(countries),
            "sales_channel": random.choice(sales_channels),
            "payment_method": random.choice(payment_methods),
        }

        sales_data.append(row)

    return sales_data


def write_csv(rows: list[dict]) -> None:
    """
    כותב את הנתונים לקובץ CSV.
    """
    DATA_DIR.mkdir(exist_ok=True)

    with OUTPUT_FILE.open(mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    rows = generate_sales_data(number_of_rows=1000)
    write_csv(rows)

    print(f"Sample sales data created successfully: {OUTPUT_FILE}")
    print(f"Rows created: {len(rows)}")