from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

if "database" not in config:
    raise KeyError("The 'database' section is missing in the configuration file.")

db_user = config["database"]["user"]
db_password = config["database"]["password"]
db_host = config["database"]["host"]
db_port = config["database"]["port"]
db_name = config["database"]["dbname"]

# Create the database URL dynamically
database_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
