from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import League, Base
from dbase import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency for getting the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/leagues/")
def get_leagues(sport: str, country: str, db: Session = Depends(get_db)):
    leagues = db.query(League.league).filter(League.sport == sport, League.country == country).all()
    if not leagues:
        raise HTTPException(status_code=404, detail="No leagues found for the given sport and country")
    return [league[0] for league in leagues]
