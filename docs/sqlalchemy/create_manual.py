# -*- coding: utf-8 -*-
import codecs

content = """# SQLAlchemy 2.0 완벽 가이드 매뉴얼

이 문서는 SQLAlchemy 2.0의 주요 기능과 실무 사용법을 정리한 매뉴얼입니다.

## 목차

1. [Import 항목별 상세 설명](#1-import-항목별-상세-설명)
2. [실무 샘플 코드](#2-실무-샘플-코드)
3. [쇼핑몰 시나리오 기반 완전한 예제](#3-쇼핑몰-시나리오-기반-완전한-예제)

---

## 1. Import 항목별 상세 설명

### 1.1 BaseUser (Starlette)

**목적**: 인증 시스템에서 사용자 모델의 기본 인터페이스를 제공합니다.

**사용 방법**:
```python
from starlette.authentication import BaseUser

class User(Base, BaseUser):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255))

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.username

    @property
    def identity(self) -> str:
        return str(self.id)
```

**필수 구현 속성**:
- `is_authenticated`: 사용자 인증 여부
- `display_name`: 표시용 이름
- `identity`: 고유 식별자

---

### 1.2 JSONB (PostgreSQL)

**목적**: PostgreSQL의 JSONB 타입을 사용하여 JSON 데이터를 효율적으로 저장하고 인덱싱합니다.

**사용 방법**:
```python
from sqlalchemy.dialects.postgresql import JSONB

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    specifications = Column(JSONB)
    metadata = Column(JSONB, default={})
```

**주요 특징**:
- JSON과 달리 바이너리 형태로 저장되어 인덱싱 가능
- GIN 인덱스 사용 가능
- SQLite에서는 지원하지 않음

---

### 1.3 Column

**목적**: 테이블의 컬럼을 정의하는 전통적인 SQLAlchemy 방식입니다.

**사용 방법**:
```python
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    age = Column(Integer, default=0)
```

**주요 매개변수**:
- `primary_key`: 기본 키 지정
- `nullable`: NULL 허용 여부 (기본값: True)
- `unique`: 고유 제약 조건
- `default`: 기본값
- `server_default`: 서버 측 기본값
- `index`: 인덱스 생성 여부
- `autoincrement`: 자동 증가

---

### 1.4 Integer

**목적**: 정수형 데이터 타입을 정의합니다.

**사용 방법**:
```python
from sqlalchemy import Integer

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_quantity = Column(Integer, default=0, nullable=False)
    price = Column(Integer)  # 센트 단위로 저장
```

---

### 1.5 String

**목적**: 가변 길이 문자열을 저장합니다 (VARCHAR 타입).

**사용 방법**:
```python
from sqlalchemy import String

class User(Base):
    __tablename__ = "users"
    username = Column(String(255), nullable=False)
    email = Column(String(320), unique=True)
    description = Column(String(1000))
```

---

### 1.6 Boolean

**목적**: 참/거짓 값을 저장합니다.

**사용 방법**:
```python
from sqlalchemy import Boolean

class User(Base):
    __tablename__ = "users"
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False)
    email_verified = Column(Boolean, server_default='0')
```

---

### 1.7 DateTime

**목적**: 날짜와 시간 정보를 저장합니다.

**사용 방법**:
```python
from sqlalchemy import DateTime, func

class Post(Base):
    __tablename__ = "posts"
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    published_at = Column(DateTime, nullable=True)
```

**주요 옵션**:
- `timezone=True`: 시간대 정보 포함
- `server_default=func.now()`: 서버 측 현재 시간
- `onupdate=func.now()`: 업데이트 시 자동 갱신

---

### 1.8 ForeignKey

**목적**: 외래 키 제약 조건을 정의하여 테이블 간 관계를 설정합니다.

**사용 방법**:
```python
from sqlalchemy import ForeignKey

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
```

**주요 매개변수**:
- `ondelete`: 참조 레코드 삭제 시 동작
  - `CASCADE`: 함께 삭제
  - `SET NULL`: NULL로 설정
  - `RESTRICT`: 삭제 방지
  - `NO ACTION`: 동작 없음

---

### 1.9 Numeric

**목적**: 고정 소수점 숫자를 저장합니다. 금융 데이터 등 정확한 소수점 계산이 필요한 경우 사용합니다.

**사용 방법**:
```python
from sqlalchemy import Numeric

class Product(Base):
    __tablename__ = "products"
    price = Column(Numeric(10, 2))  # 전체 10자리, 소수점 2자리
    tax_rate = Column(Numeric(5, 4), default=0.1)
    weight = Column(Numeric(8, 3))
```

---

### 1.10 Index

**목적**: 데이터베이스 인덱스를 생성하여 쿼리 성능을 향상시킵니다.

**사용 방법**:
```python
from sqlalchemy import Index

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    username = Column(String(255))

    __table_args__ = (
        Index('idx_user_email', 'email'),
        Index('idx_user_name_email', 'username', 'email'),  # 복합 인덱스
    )
```

---

### 1.11 UniqueConstraint

**목적**: 하나 이상의 컬럼에 대해 고유 제약 조건을 설정합니다.

**사용 방법**:
```python
from sqlalchemy import UniqueConstraint

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    tenant_id = Column(Integer)
    username = Column(String(255))

    __table_args__ = (
        UniqueConstraint('email', name='uq_user_email'),
        UniqueConstraint('tenant_id', 'username', name='uq_tenant_username'),
    )
```

---

### 1.12 CheckConstraint

**목적**: 컬럼 값에 대한 조건 검증을 데이터베이스 레벨에서 수행합니다.

**사용 방법**:
```python
from sqlalchemy import CheckConstraint

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    price = Column(Numeric(10, 2))
    stock = Column(Integer)

    __table_args__ = (
        CheckConstraint('price > 0', name='check_price_positive'),
        CheckConstraint('stock >= 0', name='check_stock_non_negative'),
    )
```

---

### 1.13 Enum

**목적**: 열거형 데이터 타입을 정의합니다.

**사용 방법**:
```python
from sqlalchemy import Enum
import enum

class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
```

---

### 1.14 func

**목적**: SQL 함수를 호출할 수 있는 네임스페이스를 제공합니다.

**사용 방법**:
```python
from sqlalchemy import func

class User(Base):
    __tablename__ = "users"
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
```

---

### 1.15 PrimaryKeyConstraint

**목적**: 복합 기본 키를 정의합니다.

**사용 방법**:
```python
from sqlalchemy import PrimaryKeyConstraint

class OrderItem(Base):
    __tablename__ = "order_items"
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))

    __table_args__ = (
        PrimaryKeyConstraint('order_id', 'product_id'),
    )
```

---

### 1.16 Mapped (SQLAlchemy 2.0)

**목적**: SQLAlchemy 2.0의 새로운 타입 힌트 방식입니다.

**사용 방법**:
```python
from sqlalchemy.orm import Mapped

class User(Base):
    __tablename__ = "users"

    id: Mapped[int]  # 자동으로 NOT NULL
    username: Mapped[str]
    email: Mapped[Optional[str]]  # NULL 허용
```

---

### 1.17 mapped_column (SQLAlchemy 2.0)

**목적**: SQLAlchemy 2.0에서 컬럼을 정의하는 새로운 방식입니다.

**사용 방법**:
```python
from sqlalchemy.orm import mapped_column

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
```

---

### 1.18 relationship

**목적**: ORM 레벨에서 테이블 간 관계를 정의합니다.

**사용 방법**:
```python
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    posts = relationship("Post", back_populates="user")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="posts")
```

**주요 매개변수**:
- `back_populates`: 양방향 관계 설정
- `lazy`: 로딩 전략 (select, joined, selectin, dynamic)
- `cascade`: 연쇄 작업 설정

---

### 1.19 MutableDict

**목적**: JSON/JSONB 컬럼의 변경 사항을 추적합니다.

**사용 방법**:
```python
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.postgresql import JSONB

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    preferences = Column(MutableDict.as_mutable(JSONB), default={})
```

---

## 2. 실무 샘플 코드

### 2.1 기본 사용자 테이블

```python
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(60))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
```

### 2.2 1:N 관계 (사용자-게시글)

```python
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    posts: Mapped[list["Post"]] = relationship(back_populates="user")

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
```

### 2.3 N:M 관계 (학생-강의)

```python
class StudentCourse(Base):
    __tablename__ = "student_course"

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), primary_key=True)

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    courses: Mapped[list["Course"]] = relationship(
        secondary="student_course",
        back_populates="students"
    )

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    students: Mapped[list["Student"]] = relationship(
        secondary="student_course",
        back_populates="courses"
    )
```

---

## 3. 쇼핑몰 시나리오 기반 완전한 예제

### 3.1 Enum 정의

```python
import enum

class OrderStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class PaymentMethod(enum.Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
```

### 3.2 고객 테이블 (복합 기본 키)

```python
from typing import Optional
from datetime import datetime
from sqlalchemy import (
    Boolean, Column, DateTime, Integer, String, Numeric,
    PrimaryKeyConstraint, UniqueConstraint, CheckConstraint, Index, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Customer(Base):
    \"\"\"고객 테이블 - 복합 기본 키 사용\"\"\"
    __tablename__ = "customers"

    # 복합 기본 키
    tenant_id: Mapped[int] = mapped_column(Integer, nullable=False)
    customer_number: Mapped[str] = mapped_column(String(20), nullable=False)

    # 기본 정보
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # 선택적 정보
    address: Mapped[Optional[str]] = mapped_column(String(500))
    city: Mapped[Optional[str]] = mapped_column(String(100))
    country: Mapped[str] = mapped_column(String(2), default='KR')

    # 상태
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    loyalty_points: Mapped[int] = mapped_column(Integer, default=0)

    # 타임스탬프
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # 관계
    orders: Mapped[list["Order"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        # 복합 기본 키
        PrimaryKeyConstraint('tenant_id', 'customer_number'),

        # 고유 제약
        UniqueConstraint('tenant_id', 'email', name='uq_customer_email'),

        # 체크 제약
        CheckConstraint('loyalty_points >= 0'),

        # 인덱스
        Index('idx_customer_tenant_email', 'tenant_id', 'email'),
    )
```

### 3.3 상품 테이블

```python
from decimal import Decimal

class Product(Base):
    \"\"\"상품 테이블\"\"\"
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    # 가격
    base_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    sale_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))

    # 재고
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0)

    # 타임스탬프
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # 관계
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="product")

    __table_args__ = (
        CheckConstraint('base_price > 0'),
        CheckConstraint('stock_quantity >= 0'),
        Index('idx_product_category', 'category'),
    )
```

### 3.4 주문 테이블

```python
class Order(Base):
    \"\"\"주문 테이블\"\"\"
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    # 고객 정보 (복합 외래 키)
    customer_tenant_id: Mapped[int] = mapped_column(Integer, nullable=False)
    customer_number: Mapped[str] = mapped_column(String(20), nullable=False)

    # 주문 상태
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus),
        default=OrderStatus.PENDING
    )

    # 금액
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    # 타임스탬프
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # 관계
    customer: Mapped["Customer"] = relationship(
        back_populates="orders",
        foreign_keys="[Order.customer_tenant_id, Order.customer_number]"
    )
    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index('idx_order_customer', 'customer_tenant_id', 'customer_number'),
        Index('idx_order_status', 'status'),
    )
```

### 3.5 주문 항목 테이블 (N:M 중간 테이블)

```python
class OrderItem(Base):
    \"\"\"주문 항목 - Order와 Product의 N:M 관계\"\"\"
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),
        index=True
    )
    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("products.id", ondelete="RESTRICT"),
        index=True
    )

    # 주문 정보
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    # 상품 정보 스냅샷
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    product_sku: Mapped[str] = mapped_column(String(50), nullable=False)

    # 관계
    order: Mapped["Order"] = relationship(back_populates="order_items")
    product: Mapped["Product"] = relationship(back_populates="order_items")

    __table_args__ = (
        UniqueConstraint('order_id', 'product_id', name='uq_order_product'),
        CheckConstraint('quantity > 0'),
        CheckConstraint('unit_price > 0'),
    )
```

### 3.6 사용 예제

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 엔진 생성
engine = create_engine('sqlite:///shopping_mall.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# 고객 생성
customer = Customer(
    tenant_id=1,
    customer_number="CUST-0001",
    email="customer@example.com",
    full_name="홍길동",
    phone="010-1234-5678",
    hashed_password="hashed_pw"
)
session.add(customer)

# 상품 생성
product = Product(
    sku="PROD-001",
    name="노트북",
    category="전자제품",
    base_price=Decimal("1500000.00"),
    stock_quantity=50
)
session.add(product)
session.commit()

# 주문 생성
order = Order(
    order_number="ORD-20250120-0001",
    customer_tenant_id=1,
    customer_number="CUST-0001",
    subtotal=Decimal("1500000.00"),
    total_amount=Decimal("1500000.00")
)
session.add(order)
session.commit()

# 주문 항목 생성
order_item = OrderItem(
    order_id=order.id,
    product_id=product.id,
    quantity=1,
    unit_price=product.base_price,
    subtotal=product.base_price,
    product_name=product.name,
    product_sku=product.sku
)
session.add(order_item)
session.commit()

# 조회
customer = session.query(Customer).filter_by(
    tenant_id=1,
    customer_number="CUST-0001"
).first()
print(f"고객: {customer.full_name}")
for order in customer.orders:
    print(f"  주문: {order.order_number}")
    for item in order.order_items:
        print(f"    상품: {item.product_name}, 수량: {item.quantity}")

session.close()
```

---

## 4. 주요 패턴 및 베스트 프랙티스

### 4.1 인덱스 전략

```python
# 단일 컬럼 인덱스
Index('idx_user_email', 'email')

# 복합 인덱스 (순서 중요!)
Index('idx_user_name_email', 'username', 'email')

# 부분 인덱스 (PostgreSQL)
Index('idx_active_users', 'email', postgresql_where=text('is_active = true'))

# GIN 인덱스 (JSONB)
Index('idx_metadata', 'metadata', postgresql_using='gin')
```

### 4.2 제약 조건

```python
# 체크 제약
CheckConstraint('age >= 18', name='check_adult')
CheckConstraint('price > 0', name='check_positive_price')

# 고유 제약
UniqueConstraint('email', name='uq_email')
UniqueConstraint('tenant_id', 'username', name='uq_tenant_user')

# 복합 기본 키
PrimaryKeyConstraint('table1_id', 'table2_id')
```

### 4.3 관계 로딩 전략

```python
# Lazy Loading (기본값) - N+1 문제 주의
posts = relationship("Post", lazy="select")

# Eager Loading - JOIN 사용
posts = relationship("Post", lazy="joined")

# Subquery Loading - IN 절 사용
posts = relationship("Post", lazy="selectin")

# Dynamic - 쿼리 객체 반환
posts = relationship("Post", lazy="dynamic")
```

---

## 5. 참고 사항

- SQLAlchemy 2.0에서는 `Mapped`와 `mapped_column`을 사용하는 것이 권장됩니다
- 복합 기본 키나 외래 키는 `__table_args__`에서 정의합니다
- N+1 문제를 피하기 위해 적절한 로딩 전략을 선택하세요
- 인덱스는 조회 성능을 향상시키지만 쓰기 성능은 저하시킬 수 있습니다
- 제약 조건은 데이터 무결성을 보장하는 가장 확실한 방법입니다

"""

# UTF-8-SIG 인코딩으로 저장 (BOM 포함)
with codecs.open('table.md', 'w', 'utf-8-sig') as f:
    f.write(content)

print("File created successfully")
print(f"Size: {len(content)} bytes")
