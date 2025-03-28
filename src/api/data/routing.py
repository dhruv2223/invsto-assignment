from fastapi import APIRouter,HTTPException
import psycopg2
from psycopg2 import sql
from ..database import get_connection 
from ..schemas import StockData
router = APIRouter() 
@router.get("/") 
async def get_data(): 
    connection = get_connection() 
    if connection is None:
        raise HTTPException(status_code=500,detail="Database connection failed") 
    else:
        cursor = connection.cursor() 
        cursor.execute("SELECT * FROM stock_prices;") 
        data = cursor.fetchall()  
        cursor.close()
        connection.close() 
        return {"stock_data":data}




@router.post("/")
async def put_data(stock: StockData):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error")

    try:
        cursor = conn.cursor()
        insert_query = sql.SQL("""
            INSERT INTO stock_prices (datetime, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s)
        """)
        cursor.execute(insert_query, (stock.datetime, stock.open, stock.high, stock.low, stock.close, stock.volume))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Stock data added successfully"}
    except psycopg2.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


