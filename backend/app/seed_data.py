from datetime import datetime, timedelta
from decimal import Decimal
import random

from app.core.database import SessionLocal
from app.models.enterprise import (
    Customer,
    Product,
    Order,
    SupportTicket,
    Employee,
    Expense,
)


def seed_database():
    db = SessionLocal()

    try:
        # Prevent duplicate seed data
        if db.query(Customer).first():
            print("Database already contains data. Skipping seed.")
            return

        random.seed(42)

        # -------------------------
        # CUSTOMERS
        # -------------------------

        customers = [
            Customer(
                name="Acme Corporation",
                email="contact@acme.example",
                industry="Manufacturing",
                country="USA",
            ),
            Customer(
                name="Nova Healthcare",
                email="admin@novahealth.example",
                industry="Healthcare",
                country="UK",
            ),
            Customer(
                name="BluePeak Finance",
                email="operations@bluepeak.example",
                industry="Finance",
                country="Singapore",
            ),
            Customer(
                name="Vertex Retail",
                email="business@vertex.example",
                industry="Retail",
                country="India",
            ),
            Customer(
                name="Orbit Logistics",
                email="support@orbitlogistics.example",
                industry="Logistics",
                country="Germany",
            ),
            Customer(
                name="GreenGrid Energy",
                email="contact@greengrid.example",
                industry="Energy",
                country="Canada",
            ),
            Customer(
                name="Summit Education",
                email="admin@summitedu.example",
                industry="Education",
                country="Australia",
            ),
            Customer(
                name="Titan Telecom",
                email="enterprise@titan.example",
                industry="Telecommunications",
                country="USA",
            ),
        ]

        db.add_all(customers)
        db.flush()

        # -------------------------
        # PRODUCTS
        # -------------------------

        products = [
            Product(
                name="Enterprise Analytics",
                category="Analytics",
                price=Decimal("25000.00"),
            ),
            Product(
                name="AI Intelligence Platform",
                category="Artificial Intelligence",
                price=Decimal("50000.00"),
            ),
            Product(
                name="Customer Intelligence",
                category="Analytics",
                price=Decimal("30000.00"),
            ),
            Product(
                name="Security Monitor",
                category="Security",
                price=Decimal("18000.00"),
            ),
            Product(
                name="Cloud Optimization",
                category="Cloud",
                price=Decimal("22000.00"),
            ),
        ]

        db.add_all(products)
        db.flush()

        # -------------------------
        # ORDERS
        # -------------------------

        base_date = datetime.utcnow() - timedelta(days=365)

        for month in range(12):
            order_date = base_date + timedelta(days=month * 30)

            for _ in range(random.randint(8, 15)):
                customer = random.choice(customers)
                product = random.choice(products)

                quantity = random.randint(1, 4)

                # Introduce a deliberate revenue decline
                # in the final quarter.
                if month >= 9:
                    quantity = max(1, quantity - 1)

                total = product.price * quantity

                order = Order(
                    customer_id=customer.id,
                    product_id=product.id,
                    quantity=quantity,
                    total_amount=total,
                    created_at=order_date,
                )

                db.add(order)

        db.flush()

        # -------------------------
        # SUPPORT TICKETS
        # -------------------------

        subjects = [
            "Login failure",
            "API timeout",
            "Dashboard loading slowly",
            "Incorrect report data",
            "Integration failure",
            "Billing issue",
            "Data synchronization problem",
            "Security alert",
        ]

        descriptions = [
            "Customer reports intermittent failures.",
            "API requests are timing out during peak usage.",
            "Dashboard performance has degraded.",
            "Customer reports unexpected values in the report.",
            "Third-party integration stopped working.",
            "Customer reports an incorrect invoice.",
            "Data synchronization is delayed.",
            "Customer reported suspicious activity.",
        ]

        statuses = ["open", "in_progress", "resolved"]

        for _ in range(100):
            customer = random.choice(customers)
            subject_index = random.randrange(len(subjects))

            ticket = SupportTicket(
                customer_id=customer.id,
                subject=subjects[subject_index],
                description=descriptions[subject_index],
                status=random.choice(statuses),
                priority=random.choice(["low", "medium", "high", "critical"]),
                created_at=base_date + timedelta(
                    days=random.randint(0, 364)
                ),
            )

            db.add(ticket)

        # -------------------------
        # EMPLOYEES
        # -------------------------

        employees = [
            ("Arun Thomas", "Engineering", "Software Engineer", 85000),
            ("Maya Joseph", "Engineering", "Senior Software Engineer", 125000),
            ("Rahul Menon", "Engineering", "ML Engineer", 135000),
            ("Anjali Nair", "Engineering", "Data Engineer", 110000),
            ("David Wilson", "Sales", "Sales Manager", 95000),
            ("Sarah Miller", "Sales", "Account Executive", 75000),
            ("Kevin Brown", "Support", "Support Engineer", 65000),
            ("Priya Kumar", "Support", "Support Manager", 90000),
            ("James Anderson", "Finance", "Financial Analyst", 80000),
            ("Emma Davis", "HR", "HR Manager", 85000),
        ]

        for name, department, role, salary in employees:
            db.add(
                Employee(
                    name=name,
                    department=department,
                    role=role,
                    salary=Decimal(str(salary)),
                    joined_at=base_date
                    + timedelta(days=random.randint(0, 300)),
                )
            )

        # -------------------------
        # EXPENSES
        # -------------------------

        expense_categories = [
            "Cloud Infrastructure",
            "Marketing",
            "Travel",
            "Software",
            "Office",
            "Security",
        ]

        for month in range(12):
            expense_date = base_date + timedelta(days=month * 30)

            for category in expense_categories:
                amount = random.randint(5000, 25000)

                # Deliberately increase cloud expenses
                # during the final quarter.
                if category == "Cloud Infrastructure" and month >= 9:
                    amount *= 2

                db.add(
                    Expense(
                        category=category,
                        description=f"{category} expense for month {month + 1}",
                        amount=Decimal(str(amount)),
                        created_at=expense_date,
                    )
                )

        db.commit()

        print("Enterprise seed data inserted successfully.")

        print(f"Customers: {len(customers)}")
        print(f"Products: {len(products)}")
        print("Orders: generated")
        print("Support tickets: 100")
        print(f"Employees: {len(employees)}")
        print("Expenses: generated")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()