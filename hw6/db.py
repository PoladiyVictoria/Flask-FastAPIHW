import databases
from sqlalchemy import Table, Column, Integer, String, Date, MetaData, DECIMAL, create_engine
from settings import settings


DATABASE_URL = settings.DATABASE_URL
db = databases.Database(DATABASE_URL)
metadata = MetaData()


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(20)),
    Column("surname", String(20)),
    Column("email", String(128)),
    Column("password", String(128)),
)

product = Table(
    "product",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(20)),
    Column("description", String(120)),
    Column("price", DECIMAL),
)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

