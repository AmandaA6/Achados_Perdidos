from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base  # importa Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    senha: Mapped[str] = mapped_column(String(100))
