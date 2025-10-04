from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select, SQLModel, create_engine
from database.model import Cliente
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

@app.get("/clientes/")
def listar_clientes():
    with Session(engine) as session:
        return session.exec(select(Cliente)).all()

@app.post("/clientes/")
def cadastrar_cliente(cliente: Cliente):
    with Session(engine) as session:
        session.add(cliente)
        session.commit()
        session.refresh(cliente)
        return cliente