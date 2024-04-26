from sqlalchemy import create_engine, MetaData, select, func
from sqlalchemy.orm import Session
from faker import Faker
import sys
import random
import datetime
from dotenv import dotenv_values

config = dotenv_values(".env")  

# Set up connections between sqlalchemy and postgres dbapi
string_conn = f'postgresql+psycopg2://{config["POSTGRES_USER"]}:{config["POSTGRES_PASSWORD"]}@{config["POSTGRES_HOST"]}:{config["POSTGRES_PORT"]}/{config["POSTGRES_DB"]}'
engine = create_engine(string_conn)

session = Session(engine)


# Instantiate metadata class
metadata = MetaData()
# Instantiate faker class
faker = Faker()
# Reflect metadata/schema from existing postgres database
with engine.connect() as conn:
    metadata.reflect(conn)
# create table objects

clientes = metadata.tables["clientes"]
produtos = metadata.tables["produtos"]
lojas = metadata.tables["lojas"]
vendas = metadata.tables["vendas"]
vendas_itens = metadata.tables["vendas_itens"]



# list of fake products to insert into the products table
product_list = ["chapéu", "boné", "camisa", "suéter", "moletom", 
                "shorts", "jeans", "tênis", "botas", "casaco", "acessórios"]
class GenerateData:
    print("generate a specific number of records to a target table in the \
    postgres database.")
    
    def __init__(self):
        print("define command line arguments.")
        self.table = sys.argv[1]
        self.num_records = int(sys.argv[2])
    def create_data(self):
        print("using the faker library, generate data and execute DML.")
        
        if self.table not in metadata.tables.keys():
            return print(f"{self.table} does not exist")
    
     
        if self.table == "clientes":
            print("clientes, inserting data...")
            with session as conn:
                for i in range(self.num_records):
                    print(f"clientes {self.num_records} de {i+1}")
                    insert_stmt = clientes.insert().values(
                        nome = faker.name(),
                        data = faker.date_of_birth(minimum_age=16, maximum_age=60)
                    )
                    conn.execute(insert_stmt)
                conn.commit()
                
        if self.table == "produtos":
            print("products, inserting data...")
            with session as conn:
                for i in range(self.num_records):
                    print(f"products {self.num_records} de {i+1}")
                    insert_stmt = produtos.insert().values(
                        descricao = random.choice(product_list),
                        valor = faker.random_int(1, 100000) / 100.0
                    )
                    conn.execute(insert_stmt)
                conn.commit()

        if self.table == "lojas":
            print("lojas, inserting data...")
            with session as conn:
                for i in range(self.num_records):
                    print(f"lojas {self.num_records} de {i+1}")
                    insert_stmt = lojas.insert().values(
                        descricao = faker.name()
                    )
                    conn.execute(insert_stmt)
                conn.commit()
                    
        if self.table == "vendas":
            
            print("vendas, inserting data...")
            cust = session.scalars(select(clientes)).fetchall()
            prod = session.scalars(select(produtos)).fetchall()
            store = session.scalars(select(lojas)).fetchall()

            with session as conn:
                for i in range(self.num_records):
                    print(f"vendas {self.num_records} de {i+1}")
                    date_obj = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 365))

                    insert_stmt = vendas.insert().values(
                        data = date_obj.strftime("%Y/%m/%d"),
                        id_cliente=random.choice(cust),
                        id_loja=random.choice(store)
                    ).returning(vendas.c.id)
                    r = conn.execute(insert_stmt)
                    id_vendas_inserted = r.fetchone()[0]

                    for j in range(random.randint(1, 5)):
                        insert_stmt = vendas_itens.insert().values(
                            id_produtos=random.choice(prod),
                            id_vendas=id_vendas_inserted,
                            valor = faker.random_int(1, 100000) / 100.0
                        )
                        conn.execute(insert_stmt)

                conn.commit()

if __name__ == "__main__": 
    print("generating data...")   
    generate_data = GenerateData()   
    generate_data.create_data()
