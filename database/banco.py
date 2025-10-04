from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select, SQLModel, create_engine
from database.model import Cliente, Fornecedor, Produto, Projeto, ProjetoProduto
from contextlib import asynccontextmanager

#Utiliar toda vez que algo for alterado nesse doc:
#uvicorn database.banco:app --reload

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="CasaCote8 API", version="1.0", lifespan=lifespan)

# Métodos Get
@app.get("/clientes/")
def listar_clientes():
    with Session(engine) as session:
        return session.exec(select(Cliente)).all()
    
@app.get("/fornecedores/")
def listar_fornecedores():
    with Session(engine) as session:
        return session.exec(select(Fornecedor)).all()

@app.get("/produtos/")
def listar_produtos():
    with Session(engine) as session:
        return session.exec(select(Produto)).all()
    
@app.get("/projetos/")
def listar_projetos():
    with Session(engine) as session:
        return session.exec(select(Projeto)).all()

# Métodos Post

@app.post("/clientes/")
def cadastrar_cliente(cliente: Cliente):
    with Session(engine) as session:
        session.add(cliente)
        session.commit()
        session.refresh(cliente)
        return cliente

@app.post("/fornecedores/")
def cadastrar_fornecedor(fornecedor: Fornecedor):
    with Session(engine) as session:
        session.add(fornecedor)
        session.commit()
        session.refresh(fornecedor)
        return fornecedor
    
@app.post("/produtos/")
def cadastrar_produto(produto: Produto):
    with Session(engine) as session:
        session.add(produto)
        session.commit()
        session.refresh(produto)
        return produto
    
@app.post("/projetos/")
def cadastrar_produto(projeto: Projeto):
    with Session(engine) as session:
        session.add(projeto)
        session.commit()
        session.refresh(projeto)
        return projeto

