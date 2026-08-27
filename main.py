# We import from the 'database' folder now
# I                         mport the necessary models to ensure they are registered with SQLAlchemy's metadata
# Import the Company model to use it in the add_company function
# Import models to register them with Base.metadata
# "noqa: F401" tells Ruff to ignore the "imported but unused" warning

from select import select  # noqa: I001

from sqlalchemy import select  # noqa: F811

import database.models  # noqa: F401
from database.connection import Base, SessionLocal, engine
from database.models import Company, Service, User, Field, service_field_association  # noqa: F401


# Function to add a new company to the database
def add_company(company_name: str):
    # 1. Use a context manager to handle the session lifecycle
    with SessionLocal() as session:
        # 2. Use SQLAlchemy's select statement to check if the company already exists

        # We use the select statement to query the Company table for a company with the given name.
        stmt = select(Company).where(Company.name == company_name)
        existing_company = session.scalars(stmt).first()
        # 3. If the company does not exist, we create a new Company instance and add it to the session, then commit the transaction.
        if not existing_company:
            new_company = Company(name=company_name)
            session.add(new_company)
            session.commit()
            print(f"Company '{company_name}' added successfully!")
        else:
            # 4. If the company already exists, we print a warning message and skip the addition.
            print(
                f"Warning: Company '{company_name}' already exists. Addition skipped."
            )


def add_service(service_name: str, price: int, company_name: str):
    # open a new session to interact with the database
    with SessionLocal() as session:
        # Check if the company exist
        stmt = select(Company).where(Company.name == company_name)
        existing_company = session.scalars(stmt).first()
        if not existing_company:
            print(
                f"Error: Company '{company_name}' does not exist. Cannot add service."
            )
        else:
            # check if the service alrady exists for the company (not ready yet...)
            stmt = select(Service).where(Service.name == service_name)

            # if the company exists, create a new Service instance and add it to the session, then commit the transaction.
            new_service = Service(
                name=service_name, company_id=existing_company.id, price=price
            )  # we can also use existing_company.id to get the id of the company
            session.add(new_service)
            session.commit()
            print(
                f"The service '{service_name}' was successfully added to the company '{company_name}'!"
            )


def init_db():
    # Instruct SQLAlchemy to create all tables based on the metadata
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    # Execute the initialization function when running this script
    init_db()

add_company("MTN")  # Example usage: Add a company named "MTN"
