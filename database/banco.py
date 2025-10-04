from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select, SQLModel, create_engine
from database.model import Cliente, Fornecedor, Produto, Projeto, ProjetoProduto
from contextlib import asynccontextmanager
from datetime import date

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
    
@app.get("/projetosprodutos/")
def listar_projetosprodutos():
    with Session(engine) as session:
        return session.exec(select(ProjetoProduto)).all()

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
def cadastrar_projeto(projeto: Projeto):    
    if isinstance(projeto.prazo_proj, str):
        try:
            projeto.prazo_proj = date.fromisoformat(projeto.prazo_proj)
        except ValueError:
            raise HTTPException(status_code=400, detail="Data inválida, use formato YYYY-MM-DD")
    with Session(engine) as session:
        session.add(projeto)
        session.commit()
        session.refresh(projeto)
        return projeto

@app.post("/projetosprodutos/")
def cadastrar_projetoproduto(projetoproduto: ProjetoProduto):
    with Session(engine) as session:
        session.add(projetoproduto)
        session.commit()
        session.refresh(projetoproduto)
        return projetoproduto