from sqlalchemy import text
from app.core.database import engine


def verify_database():
    with engine.connect() as connection:
        tables = connection.execute(
            text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
        ).fetchall()

        print("Tables:")
        for table in tables:
            print("-", table[0])

        print("\nCounts:")

        table_names = [
            "customers",
            "products",
            "orders",
            "support_tickets",
            "employees",
            "expenses",
        ]

        for table_name in table_names:
            count = connection.execute(
                text(f"SELECT COUNT(*) FROM {table_name}")
            ).scalar()

            print(f"{table_name}: {count}")


if __name__ == "__main__":
    verify_database()