#!/bin/bash

# Load variables từ .env nếu có
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "⚠️ .env file not found, using defaults"
fi

# Đảm bảo biến môi trường SA_PASSWORD có giá trị
: "${SA_PASSWORD:?Environment variable SA_PASSWORD is not set}"

# Start SQL Server ở background
/opt/mssql/bin/sqlservr &

# Chờ SQL Server khởi động
echo "⏳ Waiting for SQL Server to start..."
sleep 10

# Kiểm tra và chạy file SQL nếu tồn tại
if [ -f "${SQL_FILE:-/sql/cgv.sql}" ]; then
    echo "🚀 Running ${SQL_FILE:-/sql/cgv.sql} ..."
    /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "$SA_PASSWORD" -i "${SQL_FILE:-/sql/cgv.sql}"
    echo "✅ Database initialized."
else
    echo "⚠️ SQL file not found at ${SQL_FILE:-/sql/cgv.sql}, skipping initialization."
fi

# Giữ container sống
wait
