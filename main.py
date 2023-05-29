from fastapi import FastAPI
from database import SessionLocal, engine, Base
from models import NetFlow
import pandas as pd
from sqlalchemy.orm import sessionmaker
import asyncio
from predict import *
app = FastAPI()
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
data={}
# Create an empty DataFrame
@app.get("/netflow")
async def get_netflow_data():
    session = Session()
    netflow_row = session.query(NetFlow).first()

    if netflow_row:
            row_dict = netflow_row.__dict__
            row_dict.pop('_sa_instance_state', None)
    session.close()
    return    {"message":str(prediction(row_dict))}





@app.post("/upload/")
async def upload_csv():
    file_path = r"C:\Users\hp\Desktop\ppp\env\files\data (2).csv" 
    df = pd.read_csv(file_path)
    data = df.to_dict(orient="records")  
    netflows = [NetFlow(**item) for item in data]

    with SessionLocal() as db:
        db.bulk_save_objects(netflows)
        db.commit()

    return {"message": "Data uploaded successfully"}


   



