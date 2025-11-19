@app/home/models.py 이 코드의 상단에는 import와 관련하여 주석으로 만들어 놓은 코드들이 있다. 이 코드들 중
BaseUser, JSONB, Column,     Integer,    String,    Boolean,    DateTime,    ForeignKey,    Numeric,    Table,    Index,    UniqueConstraint,    CheckConstraint,    text,    func,   PrimaryKeyConstraint,    Enum,  generate_password_hash, check_password_hash, Mapped, mapped_column, relationship, DynamicMapped, backref, MutableDict 에 대해 각각을 항목으로 만들어 메뉴얼과 같이 자세히 정리해줘. 어떤 목적으로 사용되고, 어떤 방법으로 사용할 수 있는지 간단한 코드를 기반으로 설명을 해줘. 이후 실무에서 사용 하는 방식의 샘플 코드를 각 항목별로 3개씩 추가로 만들어줘.

마지막으로 sqlalchemy2.0에서 제안하는 mapped와 관련하여 아래 요구사항에 맞는 시나리오 기반 샘플 테이블을 만들어줘.

쇼핑몰의 상품 테이블, 주문 테이블, 고객 테이블을 만들어줘. 고객은 여러개의 같은 상품을 주문할 수 있기 때문에 주문 테이블은 고객 테이블과 상품 테이블의 N:M 중간 테이블이 되어야 한다. 예상되는 필요한 필드들을 추가해줘. 고객 테이블은 임의로 2개의 컬럼으로 구성된 복합키를 정의해줘. 
실무에서 사용할만한 필드 정의와 테이블 옵션을 최대한 많이 구현해줘.
그리고 각 옵션의 설정에 대해 주석으로 어떤 목적인지, 어떤 옵션들이 있으며 각 옵션은 어떤 역할을 하는지를 설명으로 만들어줘.

내가 요구한 사항들은 @docs/sqlalchemy/table.md 에 만들어줘.
이 문서는 메뉴얼로 사용할 것이기 때문에 최대한 자세히, 다양한 정보를 정리하여 실무에 사용할 수 있도록 만들어줘.