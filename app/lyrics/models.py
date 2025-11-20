from sqlalchemy import (
    DateTime,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base

# from sqlalchemy import (
#     Column,
#     Integer,
#     String,
#     Boolean,
#     DateTime,
#     ForeignKey,
#     Numeric,
#     Table,
#     Index,
#     UniqueConstraint,
#     CheckConstraint,
#     text,
#     func,
#     PrimaryKeyConstraint,
#     Enum,
# )


class StoreDefaultInfo(Base):
    __tablename__ = "store_default_info"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )

    store_info: Mapped[str] = mapped_column(
        Text,
        unique=False,
        nullable=True,
    )

    store_name: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=False,
    )

    store_category: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=True,
    )

    store_address: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=True,
    )

    store_phone_number: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
    )

    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return f"id={self.id}, store_name={self.store_name}"


class PromptTemplate(Base):
    __tablename__ = "prompt_template"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )

    description: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=True,
    )

    prompt: Mapped[str] = mapped_column(
        Text,
        unique=False,
        nullable=False,
    )

    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return f"id={self.id}, description={self.description}"


class Attribute(Base):
    __tablename__ = "attribute"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )

    attr_category: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=False,
    )

    attr_value: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return f"id={self.id}, attr_category={self.attr_category}"


class SongSample(Base):
    __tablename__ = "song_sample"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )

    ai: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=False,
    )

    ai_model: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=False,
    )

    season: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=True,
    )

    num_of_people: Mapped[int] = mapped_column(
        Integer,
        unique=False,
        nullable=True,
    )

    people_category: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=True,
    )

    genre: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=True,
    )

    sample_song: Mapped[str] = mapped_column(
        String(400),
        unique=True,
        nullable=False,
    )

    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return f"id={self.id}, sample_song={self.sample_song}"


class SongResultsAll(Base):
    __tablename__ = "song_results_all"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )

    store_info: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=True,
    )

    store_name: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=False,
    )

    store_category: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=True,
    )

    store_address: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=True,
    )

    store_phone_number: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
    )

    description: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=True,
    )

    prompt: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    attr_category: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=False,
    )

    attr_value: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    ai: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=False,
    )

    ai_model: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=False,
    )

    season: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=True,
    )

    num_of_people: Mapped[int] = mapped_column(
        Integer,
        unique=False,
        nullable=True,
    )

    people_category: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=True,
    )

    genre: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=True,
    )

    sample_song: Mapped[str] = mapped_column(
        String(400),
        unique=True,
        nullable=False,
    )

    result_song: Mapped[str] = mapped_column(
        String(400),
        unique=True,
        nullable=False,
    )

    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return f"id={self.id}, result_song={self.result_song}"
