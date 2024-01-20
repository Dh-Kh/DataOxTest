import psycopg2
import pandas as pd


def insert_into_database():
    conn = psycopg2.connect(
        database="postgres",
        host="pgdb",
        user="postgres",
        password="12345",
        port="5432"
        )
    df = pd.read_csv("car_data.csv")
    table_name = "car_storage"
    table_schema = '''
    CREATE TABLE IF NOT EXISTS {} (
        url VARCHAR,
        title VARCHAR,
        price_usd INTEGER,
        odometer INTEGER,
        username VARCHAR,
        phone_number VARCHAR,
        image_url VARCHAR,
        images_count INTEGER,
        car_number VARCHAR,
        car_vin VARCHAR,
        datetime_found TIMESTAMP
    );
    '''.format(table_name)
    insert_query = f"INSERT INTO {table_name} VALUES %s"

    with conn.cursor() as cursor:
        cursor.execute(table_schema)
        conn.commit()
        records = [tuple(row) for row in df.itertuples(index=False, name=None)]
        psycopg2.extras.execute_values(cursor, insert_query, records)
        conn.commit()
    conn.close()
        
        