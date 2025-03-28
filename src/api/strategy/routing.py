from fastapi import APIRouter, HTTPException
import pandas as pd
import numpy as np
from ..database import get_connection

router = APIRouter()

def calculate_ma_crossover_signals(df, short_window=20, long_window=50):
    df['short_ma'] = df['close'].rolling(window=short_window).mean()
    df['long_ma'] = df['close'].rolling(window=long_window).mean()
    
    df['signal'] = 0
    df.loc[df['short_ma'] > df['long_ma'], 'signal'] = 1  # Buy signal
    df.loc[df['short_ma'] < df['long_ma'], 'signal'] = -1  # Sell signal
    
    df['position'] = df['signal'].diff()
    
    return df

def calculate_performance(df):
    df['daily_return'] = df['close'].pct_change()
    
    df['strategy_return'] = df['position'] * df['daily_return']
    
    df['cumulative_return'] = (1 + df['strategy_return']).cumprod()
    
    total_return = df['cumulative_return'].iloc[-1] - 1
    annual_return = (1 + total_return) ** (252 / len(df)) - 1
    sharpe_ratio = np.sqrt(252) * df['strategy_return'].mean() / df['strategy_return'].std()
    
    return {
        "total_return": float(total_return),
        "annual_return": float(annual_return),
        "sharpe_ratio": float(sharpe_ratio),
        "total_trades": int(len(df[df['position'] != 0])),
        "win_rate": float(len(df[df['strategy_return'] > 0]) / len(df[df['strategy_return'] != 0]))
    }

@router.get("/performance")
async def get_strategy_performance():
    connection = get_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT datetime, close FROM stock_prices ORDER BY datetime;")
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        
        df = pd.DataFrame(data, columns=['datetime', 'close'])
        df['close'] = df['close'].astype(float)  # Convert Decimal to float
        
        df = calculate_ma_crossover_signals(df)
        performance = calculate_performance(df)
        
        return {
            "strategy": "Moving Average Crossover",
            "parameters": {
                "short_window": 20,
                "long_window": 50
            },
            "performance": performance
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating strategy performance: {str(e)}") 
