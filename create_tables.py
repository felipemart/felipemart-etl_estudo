from sqlalchemy import create_engine, MetaData, \
    Column, Integer, Numeric, String, Date, Table, ForeignKey
from dotenv import dotenv_values

config = dotenv_values(".env")  

# Set up connections between sqlalchemy and postgres dbapi
string_conn = f'postgresql+psycopg2://{config["POSTGRES_USER"]}:{config["POSTGRES_PASSWORD"]}@{config["POSTGRES_HOST"]}:{config["POSTGRES_PORT"]}/{config["POSTGRES_DB"]}'
engine = create_engine(string_conn)
metadata = MetaData()

clientes_table = Table(
    "clientes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nome", String(255), nullable=False),
    Column("data", Date, nullable=False)
)
produtos_table = Table(
    "produtos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("descricao", String(150), nullable=False),
    Column("valor", Numeric(10,2), nullable=False),
)
lojas_table = Table(    
    "lojas",    
    metadata,    
    Column("id", Integer, primary_key=True),
    Column("descricao", String(135), nullable=True)
)
vendas_table = Table(    
    "vendas",    
    metadata,    
    Column("id", Integer, primary_key=True),
    Column("data", Date, nullable=False),
    Column("id_cliente", ForeignKey("clientes.id"),
        nullable=False),
    Column("id_loja", ForeignKey("lojas.id"),
        nullable=False)
)
vendas_itens_table = Table(    
    "vendas_itens",    
    metadata,    
    Column("id", Integer, primary_key=True),
    Column("id_produtos", ForeignKey("produtos.id"),
        nullable=False),
    Column("id_vendas", ForeignKey("vendas.id")),
    Column("valor", Numeric(10,2), nullable=False)
)

# Start transaction to commit DDL to postgres database
with engine.begin() as conn:
    metadata.create_all(conn)
    # Log the tables as they are created
    for table in metadata.tables.keys():
        print(f"{table} successfully created")