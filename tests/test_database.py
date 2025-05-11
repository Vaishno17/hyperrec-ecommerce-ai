import sqlite3

def test_db_connection():
    conn = sqlite3.connect("database/ecommerce_recommendations.db")
    c = conn.cursor()
    c.execute("SELECT * FROM customers LIMIT 1")
    assert c.fetchone() is not None
    conn.close()
