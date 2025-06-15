from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

DEFAULT_ARGS = {
    'start_date': datetime.now().replace(second=0, microsecond=0),
    'owner': 'admin'
}

with DAG('ohlc_aggregation',
    schedule_interval='*/10 * * * *',
    default_args=DEFAULT_ARGS,
    max_active_runs=1,
    catchup=False,
    tags=['ohlc', 'admin']
) as dag:
    
    raw_data_aggregator = PostgresOperator(
        task_id="raw_data_aggregator",
        postgres_conn_id='postgres_ohlc',
        sql="""
            INSERT INTO ohlc_10min(timestamp, symbol, open, high, low, close, volume)
            SELECT 
                DATE_TRUNC('minute', trade_time) AS timestamp,
                symbol,
                (ARRAY_AGG(price ORDER BY trade_time ASC))[1] AS open,
                MAX(price) AS high,
                MIN(price) AS low,
                (ARRAY_AGG(price ORDER BY trade_time DESC))[1] AS close,
                SUM(quantity) AS volume
            FROM raw_trades
            WHERE trade_time BETWEEN DATE_TRUNC('minute', NOW()) - interval '1 minute' AND DATE_TRUNC('minute', NOW())
            GROUP BY DATE_TRUNC('minute', trade_time), symbol;
        """
    )