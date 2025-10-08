#!/bin/bash

# Start SQL Server in background
/opt/mssql/bin/sqlservr &

# Wait for SQL Server to be ready
echo "⏳ Waiting for SQL Server to start..."
sleep 20

# Run the init SQL file (nếu có)
if [ -f /sql/cgv.sql ]; then
    echo "🚀 Running /sql/cgv.sql ..."
    /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P 'YourStrong!Passw0rd' -i /sql/cgv.sql
    echo "✅ Database initialized."
else
    echo "⚠️ No /sql/cgv.sql file found, skipping initialization."
fi

# Keep container alive
wait
