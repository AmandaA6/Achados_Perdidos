from sqlalchemy import String, Date, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base  

class Item(Base):
    __tablename__ = "itens"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=True)
    local: Mapped[str] = mapped_column(String(120), nullable=False)
    data: Mapped[Date] = mapped_column(Date, nullable=False) 
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    foto: Mapped[str] = mapped_column(String(200), nullable=True)
