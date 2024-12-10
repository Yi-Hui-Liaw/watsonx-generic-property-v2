import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///db/database.db", echo=False)

data = pd.read_excel("data/sql/abc-lumenh-nexus-sample.xlsx", sheet_name=None)

for k, v in data.items():
    v.columns = [x.replace(" ", "_") for x in v.columns]
    table = k.split(" ")[0]
    v.to_sql(table, con=engine, index=False, if_exists="replace")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()