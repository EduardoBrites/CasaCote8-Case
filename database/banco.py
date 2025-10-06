from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select, SQLModel, create_engine
from database.model import Cliente, Fornecedor, Produto, Projeto, ProjetoProduto
from contextlib import asynccontextmanager
from datetime import date
from typing import List, Dict, Any
from sqlalchemy import extract, func

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
    

@app.get("/lucro/{projeto_id}")
def calcular_lucro_projeto(projeto_id: int):
    with Session(engine) as session:
        stmt = (
            select(ProjetoProduto, Produto)
            .join(Produto, Produto.id_prod == ProjetoProduto.produto_id_prod)
            .where(ProjetoProduto.projeto_id_proj == projeto_id)
        )
        results = session.exec(stmt).all()
        detalhes: List[Dict[str, Any]] = []
        total_lucro = 0.0

        for projprod, produto in results:
            quantidade = projprod.quantidade_prod or 0
            preco = produto.precouni_prod or 0.0
            lucro_item = quantidade * preco
            total_lucro += lucro_item

            detalhes.append({
                "produto_id": produto.id_prod,
                "produto_nome": produto.nome_prod,
                "quantidade": quantidade,
                "preco_unitario": preco,
                "lucro_item": lucro_item
            })

        return {"projeto_id": projeto_id, "total_lucro": total_lucro, "detalhes": detalhes}
    
@app.get("/lucro_mensal/")
def calcular_lucro_mensal():
    with Session(engine) as session:
        stmt = (
            select(
                extract("year", Projeto.prazo_proj).label("ano"),
                extract("month", Projeto.prazo_proj).label("mes"),
                func.sum((ProjetoProduto.quantidade_prod * Produto.precouni_prod)).label("lucro_total")
            )
            .join(ProjetoProduto, Projeto.id_proj == ProjetoProduto.projeto_id_proj)
            .join(Produto, Produto.id_prod == ProjetoProduto.produto_id_prod)
            .group_by("ano", "mes")
            .order_by("ano", "mes")
        )

        results = session.exec(stmt).all()
        retorno = [
            {"ano": int(r.ano), "mes": int(r.mes), "lucro_total": float(r.lucro_total or 0)}
            for r in results
        ]
        return retorno

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
    


#Metodos put

@app.put("/clientes/{id_cli}")
def atualizar_cliente(id_cli: int, cliente_atualizado: Cliente):
    with Session(engine) as session:
        cliente = session.get(Cliente, id_cli)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        for campo, valor in cliente_atualizado.dict(exclude_unset=True).items():
            setattr(cliente, campo, valor)

        session.add(cliente)
        session.commit()
        session.refresh(cliente)
        return cliente


@app.put("/fornecedores/{id_fornec}")
def atualizar_fornecedor(id_fornec: int, fornecedor_atualizado: Fornecedor):
    with Session(engine) as session:
        fornecedor = session.get(Fornecedor, id_fornec)
        if not fornecedor:
            raise HTTPException(status_code=404, detail="Fornecedor não encontrado")

        for campo, valor in fornecedor_atualizado.dict(exclude_unset=True).items():
            setattr(fornecedor, campo, valor)

        session.add(fornecedor)
        session.commit()
        session.refresh(fornecedor)
        return fornecedor


@app.put("/produtos/{id_prod}")
def atualizar_produto(id_prod: int, produto_atualizado: Produto):
    with Session(engine) as session:
        produto = session.get(Produto, id_prod)
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        for campo, valor in produto_atualizado.dict(exclude_unset=True).items():
            setattr(produto, campo, valor)

        session.add(produto)
        session.commit()
        session.refresh(produto)
        return produto


@app.put("/projetos/{id_proj}")
def atualizar_projeto(id_proj: int, projeto_atualizado: Projeto):
    with Session(engine) as session:
        projeto = session.get(Projeto, id_proj)
        if not projeto:
            raise HTTPException(status_code=404, detail="Projeto não encontrado")

        for campo, valor in projeto_atualizado.dict(exclude_unset=True).items():
            setattr(projeto, campo, valor)

        session.add(projeto)
        session.commit()
        session.refresh(projeto)
        return projeto


@app.put("/projetosprodutos/{projeto_id}/{produto_id}")
def atualizar_projeto_produto(projeto_id: int, produto_id: int, dados_atualizados: ProjetoProduto):
    with Session(engine) as session:
        projeto_produto = session.get(ProjetoProduto, (projeto_id, produto_id))
        if not projeto_produto:
            raise HTTPException(status_code=404, detail="Relação Projeto-Produto não encontrada")

        for campo, valor in dados_atualizados.dict(exclude_unset=True).items():
            setattr(projeto_produto, campo, valor)

        session.add(projeto_produto)
        session.commit()
        session.refresh(projeto_produto)
        return projeto_produto
    
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