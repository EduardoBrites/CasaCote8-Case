from typing import Optional, List
from datetime import date
from sqlmodel import SQLModel, Field, Relationship


class Cliente(SQLModel, table=True):
    __tablename__ = "CLIENTE"
    __table_args__ = {"extend_existing": True}

    id_cli: int | None = Field(primary_key=True)
    nome_cli: Optional[str] = Field(default=None, max_length=150)
    tel_cli: Optional[int] = Field(default=None)
    cpfcnpj_cli: Optional[int] = Field(default=None, unique=True)
    email_cli: Optional[str] = Field(default=None, max_length=150)

    projetos: List["Projeto"] = Relationship(back_populates="cliente")


class Fornecedor(SQLModel, table=True):
    __tablename__ = "FORNECEDOR"
    __table_args__ = {"extend_existing": True}

    id_fornec: int | None = Field(primary_key=True)
    cpfcnpj_fornec: Optional[int] = Field(default=None, unique=True)
    tel_fornec: Optional[int] = Field(default=None)
    nome_fornec: Optional[str] = Field(default=None, max_length=70)
    email_fornec: Optional[str] = Field(default=None, max_length=150)

    produtos: List["Produto"] = Relationship(back_populates="fornecedor")


class Produto(SQLModel, table=True):
    __tablename__ = "PRODUTO"
    __table_args__ = {"extend_existing": True}

    id_prod: int | None = Field(primary_key=True)
    fornecedor_id_fornec: int = Field(foreign_key="FORNECEDOR.id_fornec")

    nome_prod: Optional[str] = Field(default=None, max_length=150)
    cor_prod: Optional[str] = Field(default=None, max_length=15)
    colecao_prod: Optional[str] = Field(default=None, max_length=50)
    bordado_prod: Optional[bool] = Field(default=None, max_length=1)
    corlinha_prod: Optional[str] = Field(default=None, max_length=15)
    observacao_prod: Optional[str] = Field(default=None, max_length=300)
    precouni_prod: Optional[float] = Field(default=None)

    fornecedor: Optional[Fornecedor] = Relationship(back_populates="produtos")
    projetos: List["ProjetoProduto"] = Relationship(back_populates="produto")


class Projeto(SQLModel, table=True):
    __tablename__ = "PROJETO"
    __table_args__ = {"extend_existing": True}

    id_proj: int | None = Field(primary_key=True)
    prazo_proj: Optional[date] = None
    cliente_id_cli: int = Field(foreign_key="CLIENTE.id_cli")

    cliente: Optional[Cliente] = Relationship(back_populates="projetos")
    produtos: List["ProjetoProduto"] = Relationship(back_populates="projeto")


class ProjetoProduto(SQLModel, table=True):
    __tablename__ = "PROJETO_PRODUTO"
    __table_args__ = {"extend_existing": True}

    projeto_id_proj: int = Field(foreign_key="PROJETO.id_proj", primary_key=True)
    produto_id_prod: int = Field(foreign_key="PRODUTO.id_prod", primary_key=True)
    produto_fornecedor_id_fornec: int = Field(foreign_key="FORNECEDOR.id_fornec", primary_key=True)

    quantidade_produto: Optional[int] = None

    projeto: Optional[Projeto] = Relationship(back_populates="produtos")
    produto: Optional[Produto] = Relationship(back_populates="projetos")
