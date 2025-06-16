import requests
import json
import time

class SupersetAPI:
    def __init__(self):
        self.base_url = 'http://superset:8088/api/v1'
        self.headers = None

    def login(self):
        response = requests.post(
            f'{self.base_url}/security/login',
            json={'username': 'admin', 'password': 'admin', 'provider': 'db'}
        )
        self.headers = {
            'Authorization': f'Bearer {response.json()["access_token"]}',
            'Content-Type': 'application/json'
        }

    def create_database(self):
        response = requests.post(
            f'{self.base_url}/database/',
            headers=self.headers,
            json={
                'database_name': 'PostgreSQL',
                'sqlalchemy_uri': 'postgresql+psycopg2://airflow:airflow@postgres:5432/airflow',
                'expose_in_sqllab': True
            }
        )
        return response.json()['id']

    def create_dataset(self, database_id, table_name):
        response = requests.post(
            f'{self.base_url}/dataset/',
            headers=self.headers,
            json={
                'database': database_id,
                'schema': 'public',
                'table_name': table_name
            }
        )
        return response.json()['id']

    def create_chart(self, dataset_id, chart_type, metric, name, time_grain):
        params = {
            'granularity_sqla': 'trade_time',
            'time_grain_sqla': time_grain,
            'time_range': 'No filter',
            'metrics': [{
                'expressionType': 'SIMPLE',
                'column': {'column_name': metric['column']},
                'aggregate': metric['type'],
                'label': metric['label'],
                'optionName': f'metric_{metric["column"]}'
            }],
            'viz_type': chart_type,
            'y_axis_format': '~g',
            'groupby': ['symbol'],
        }

        response = requests.post(
            f'{self.base_url}/chart/',
            headers=self.headers,
            json={
                'datasource_id': dataset_id,
                'datasource_type': 'table',
                'slice_name': name,
                'viz_type': chart_type,
                'params': json.dumps(params)
            }
        )
        
        if response.status_code not in [200, 201]:
            print(f'Error creating chart: {response.status_code}')
            print(f'Response: {response.text}')
            raise Exception('Failed to create chart')
            
        return response.json()['id']

    def create_table_chart(self, dataset_id, name):
        params = {
            'granularity_sqla': 'timestamp',
            'time_grain_sqla': None,
            'time_range': 'No filter',
            'query_mode': 'raw',
            'all_columns': [
                'symbol',
                'timestamp',
                'open',
                'high',
                'low',
                'close',
                'volume'
            ],
            'order_by_cols': ['timestamp DESC'],
            'row_limit': 1000,
            'viz_type': 'table'
        }

        response = requests.post(
            f'{self.base_url}/chart/',
            headers=self.headers,
            json={
                'datasource_id': dataset_id,
                'datasource_type': 'table',
                'slice_name': name,
                'viz_type': 'table',
                'params': json.dumps(params)
            }
        )
        
        if response.status_code not in [200, 201]:
            print(f'Error creating chart: {response.status_code}')
            print(f'Response: {response.text}')
            raise Exception('Failed to create chart')
            
        return response.json()['id']

def main():
    api = SupersetAPI()
    api.login()

    database_id = api.create_database()
    time.sleep(5)
    
    raw_trades_dataset_id = api.create_dataset(database_id, 'raw_trades')

    price_chart_id = api.create_chart(
        dataset_id=raw_trades_dataset_id,
        chart_type='line',
        metric={'type': 'AVG', 'column': 'price', 'label': 'Average Price'},
        name='Price Over Time',
        time_grain='PT1S'
    )

    volume_chart_id = api.create_chart(
        dataset_id=raw_trades_dataset_id,
        chart_type='bar',
        metric={'type': 'SUM', 'column': 'quantity', 'label': 'Volume'},
        name='Volume Over Time',
        time_grain='PT1M'
    )

    ohlc_dataset_id = api.create_dataset(database_id, 'ohlc_10min')
    
    table_chart_id = api.create_table_chart(
        dataset_id=ohlc_dataset_id,
        name='OHLCV'
    )

    print('All charts created successfully')

if __name__ == '__main__':
    main()