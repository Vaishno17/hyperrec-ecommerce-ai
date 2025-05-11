import sqlite3
import pandas as pd

def initialize_database():
    # Connect to the SQLite database
    conn = sqlite3.connect("database/ecommerce_recommendations.db")
    c = conn.cursor()

    # Create customers table
    c.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id TEXT PRIMARY KEY,
        age INTEGER,
        gender TEXT,
        location TEXT,
        browsing_history TEXT,
        purchase_history TEXT,
        customer_segment TEXT,
        avg_order_value REAL,
        holiday TEXT,
        season TEXT
    )
    ''')

    # Create products table
    c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        category TEXT,
        subcategory TEXT,
        price REAL,
        brand TEXT,
        average_rating_of_similar_products REAL,
        product_rating REAL,
        customer_review_sentiment_score REAL,
        holiday TEXT,
        season TEXT,
        geographical_location TEXT,
        similar_product_list TEXT,
        probability_of_recommendation REAL
    )
    ''')

    # Load CSVs
    customer_df = pd.read_csv("data/customer_data_collection.csv")
    product_df = pd.read_csv("data/product_recommendation_data.csv")

    # Insert data into the customers table
    customer_df.to_sql("customers", conn, if_exists="replace", index=False)

    # Insert data into the products table
    product_df.to_sql("products", conn, if_exists="replace", index=False)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
