from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from configparser import ConfigParser
import uvicorn

# FastAPI app
app = FastAPI()

# Request model
class LeagueInput(BaseModel):
    country: str
    sport: str

# Database connection function
def get_db_connection():
    """
    Establish a database connection using credentials from config.ini.
    """
    config = ConfigParser()
    config.read("config.ini")
    db_host = config["database"]["host"]
    db_name = config["database"]["dbname"]
    db_user = config["database"]["user"]
    db_password = config["database"]["password"]
    db_port = config["database"]["port"]
    cur = None
    conn = None
    try:
        conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user,
                                password=db_password, port=db_port)
        
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

# API endpoint to fetch leagues
@app.post("/get_leagues/")
async def get_leagues(data: LeagueInput):
    """
    Fetch all leagues for a given country and sport.
    """
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = """
        SELECT league
        FROM championship_links
        WHERE country = %s AND sport = %s
        """
        cursor.execute(query, (data.country, data.sport))
        leagues = cursor.fetchall()
        if not leagues:
            raise HTTPException(status_code=404, detail="No leagues found")
        else:
            leagues_list = []
            for row in leagues:
                leagues_list.append(row["league"])

            return {"leagues": leagues_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching leagues: {str(e)}")
    finally:
        cursor.close()
        conn.close()


