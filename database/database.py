import sqlite3
import os

def add_product(product_id, title, price, url):
    db_path = os.path.join(os.path.dirname(__file__), 'ebay_found_items.db')
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    # verify if product exist
    cur.execute("SELECT itemId FROM products WHERE itemId = ?", (product_id,))
    if cur.fetchone():
        print(f"Product {product_id} already in database")
        con.close()
        return False
    
    # add product
    cur.execute("INSERT INTO products (itemId, title, price, url) VALUES (?, ?, ?, ?)", 
                (product_id, title, price, url))
    con.commit()
    con.close()
    print(f"Added product to database: {title}")
    return True

def is_new_product(product_id):
    
    # verify if product already is found
    db_path = os.path.join(os.path.dirname(__file__), 'ebay_found_items.db')
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT itemId FROM products WHERE itemId = ?", (product_id,))
    result = cur.fetchone() is None
    con.close()
    return result