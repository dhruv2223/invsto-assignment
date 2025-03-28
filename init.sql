CREATE TABLE IF NOT EXISTS stock_prices (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP NOT NULL,
    open DECIMAL(10, 2) NOT NULL,
    high DECIMAL(10, 2) NOT NULL,
    low DECIMAL(10, 2) NOT NULL,
    close DECIMAL(10, 2) NOT NULL,
    volume INTEGER NOT NULL
);

-- Import CSV data into the table
\copy stock_prices(datetime, open, high, low, close, volume) FROM PROGRAM 'cut -d"," -f1-6 /docker-entrypoint-initdb.d/stock_data.csv' DELIMITER ',' CSV HEADER;
