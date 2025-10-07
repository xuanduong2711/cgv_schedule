import csv
from datetime import datetime, timedelta
import random

# Một số format ngày hay dùng
formats = [
    "%Y-%m-%d",      # 2025-09-21
    "%d-%m-%Y",      # 21-09-2025
    "%d/%m/%Y",      # 21/09/2025
    "%d.%m.%Y",      # 21.09.2025
    "%d-%m-%Y",      # 21-09-25
    "%Y/%m/%d"       # 2025/09/21
]

rows = []
base = datetime(2020, 1, 1, 0, 0, 0)

for i in range(20):
    random_date = base + timedelta(
        days=random.randint(0, 2000)
    )
    # Chọn format ngẫu nhiên
    fmt = random.choice(formats)
    rows.append([random_date.strftime(fmt)])

# Xuất CSV
with open("data/date_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["date"])  # header
    writer.writerows(rows)

print("✅ Done! File saved: data/fake_datetime.csv")