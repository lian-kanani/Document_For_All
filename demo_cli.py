# demo_cli.py
from database.connection import Base, engine, get_db
from database.models import Company, Field, Service
from sqlalchemy.orm import Session


def run_demo():
    print("Starting Document For All - Backend PoC...")

    # 1. Database Initialization
    print("-> Creating database schema...")
    Base.metadata.create_all(bind=engine)

    db: Session = next(get_db())

    try:
        # 2. Data Seeding (adding initial data to the database)
        print("-> Seeding data (Company, Service, Fields)...")

        # create a new company
        telecom_company = Company(name="Syriatel", is_active=True)
        db.add(telecom_company)
        db.commit()
        db.refresh(telecom_company)

        # create a new service associated with the company
        recharge_service = Service(
            name="Recharge Credit", price=0.0, company_id=telecom_company.id
        )
        db.add(recharge_service)

        # create dynamic fields
        phone_field = Field(label="Phone number", field_type="string", is_required=True)
        amount_field = Field(label="Amount", field_type="integer", is_required=True)
        db.add_all([phone_field, amount_field])
        db.commit()

        # associate fields with the service
        recharge_service.fields.append(phone_field)
        recharge_service.fields.append(amount_field)
        db.commit()

        # Verification (fetching and displaying the added data)
        print("\n--- Verification Output ---")
        fetched_service = db.query(Service).filter_by(name="Recharge Credit").first()

        print(f"Company: {fetched_service.company.name}")
        print(f"Service: {fetched_service.name}")
        print("Required Fields:")
        for field in fetched_service.fields:
            print(f"   - [ {field.label} ] (Type: {field.field_type})")

        print("-----------------------------\n")
        print("Architecture is fully operational!")

    except Exception as e:  # noqa: BLE001
        print(f"Error occurred: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    run_demo()
