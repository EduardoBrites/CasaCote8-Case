from fastapi import Depends, FastAPI, HTTPException
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
    
# Métodos Delete

def get_session():
    with Session(engine) as session:
        yield session

@app.delete("/clientes/{id_cli}")
def deletar_cliente(id_cli: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, id_cli)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    session.delete(cliente)
    session.commit()
    return {"message": "Cliente deletado com sucesso"}

@app.delete("/fornecedores/{id_fornec}")
def deletar_fornecedor(id_fornec: int, session: Session = Depends(get_session)):
    fornecedor = session.get(Fornecedor, id_fornec)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    session.delete(fornecedor)
    session.commit()
    return {"message": "Fornecedor deletado com sucesso"}

@app.delete("/produtos/{id_prod}")
def deletar_produto(id_prod: int, session: Session = Depends(get_session)):
    produto = session.get(Produto, id_prod)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    session.delete(produto)
    session.commit()
    return {"message": "Produto deletado com sucesso"}

@app.delete("/projetos/{id_proj}")
def deletar_projeto(id_proj: int, session: Session = Depends(get_session)):
    projeto = session.get(Projeto, id_proj)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    session.delete(projeto)
    session.commit()
    return {"message": "Projeto deletado com sucesso"}

@app.delete("/projetosprodutos/{projeto_id_proj}/{produto_id_prod}/{produto_fornecedor_id_fornec}")
def deletar_projetoproduto(
    projeto_id_proj: int,
    produto_id_prod: int,
    produto_fornecedor_id_fornec: int,
    session: Session = Depends(get_session)
):
    projeto_produto = session.get(
        ProjetoProduto,
        (projeto_id_proj, produto_id_prod, produto_fornecedor_id_fornec)
    )
    if not projeto_produto:
        raise HTTPException(status_code=404, detail="Relação Projeto-Produto não encontrada")

    session.delete(projeto_produto)
    session.commit()
    return {"message": "Item do projeto deletado com sucesso"}