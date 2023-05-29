from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import urllib
import os
host_server = os.environ.get('host_server', 'ppp-server.postgres.database.azure.com')
db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '5432')))
database_name = os.environ.get('database_name', 'db_ppp')
db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'pppadminserver')))
db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', 'pilote@koussay12')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode','prefer')))
DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server, db_server_port, database_name, ssl_mode)
engine=create_engine(DATABASE_URL,
    echo=True
)

Base=declarative_base()

SessionLocal=sessionmaker(bind=engine)
