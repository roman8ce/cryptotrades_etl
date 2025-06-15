CREATE TABLE  raw_trades (
    symbol VARCHAR(10),
    price NUMERIC(18, 8),
    quantity NUMERIC(18, 8),
    trade_time TIMESTAMP
    );
                        
CREATE TABLE ohlc_10min (
    timestamp TIMESTAMP,
    symbol VARCHAR(10),
    open NUMERIC(18, 8),
    high NUMERIC(18, 8),
    low NUMERIC(18, 8),
    close NUMERIC(18, 8),
    volume NUMERIC(18, 8)
    );