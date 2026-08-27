from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base

# 1. الجدول الوسيط (Association Table) لعلاقة Many-to-Many
# نستخدم Table مباشرة من SQLAlchemy لأنه جدول ربط بحت لا نحتاج لعمل Class له
service_field_association = Table(
    "service_field_association",
    Base.metadata,
    Column(
        "service_id",
        Integer,
        ForeignKey("services.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "field_id",
        Integer,
        ForeignKey("fields.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class User(Base):
    """User model representing application users/employees."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"


class Company(Base):
    """Company model representing service providers (e.g., Telecom A, Telecom B)."""

    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # إعداد العلاقة (Relationship) مع الخدمات: One-to-Many
    # back_populates تجعل SQLAlchemy يفهم العلاقة من الطرفين تلقائياً
    services = relationship(
        "Service", back_populates="company", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Company(name='{self.name}')>"


class Service(Base):
    """Service model representing specific services offered by companies."""

    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    company_id = Column(
        Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False
    )
    price = Column(Integer, default=0)  # تكلفة الخدمة أو الرسوم
    is_active = Column(Boolean, default=True)

    # الربط العكسي مع جدول الشركات
    company = relationship("Company", back_populates="services")

    # إعداد علاقة Many-to-Many مع الحقول باستخدام الجدول الوسيط
    fields = relationship(
        "Field", secondary=service_field_association, back_populates="services"
    )

    def __repr__(self):
        return f"<Service(name='{self.name}', company_id={self.company_id})>"


class Field(Base):
    """Field model representing dynamic form fields (e.g., Phone Number, Amount)."""

    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(
        String(50), nullable=False
    )  # الاسم الذي يظهر للمستخدم في الواجهة (مثل: رقم الهاتف)
    field_type = Column(
        String(20), nullable=False
    )  # نوع الحقل (text, number, date) للتحقق منه في الواجهة
    is_required = Column(Boolean, default=True)

    # الربط العكسي مع الخدمات
    services = relationship(
        "Service", secondary=service_field_association, back_populates="fields"
    )

    def __repr__(self):
        return f"<Field(label='{self.label}', type='{self.field_type}')>"
