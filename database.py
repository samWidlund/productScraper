import sqlite3

def add_product(product_id, title, price, url):
    con = sqlite3.connect('found_items.db')
    cur = con.cursor()
    
    # verify if product exist
    cur.execute("SELECT itemId FROM products WHERE itemId = ?", (product_id,))
    if cur.fetchone():
        print(f"Produkt {product_id} finns redan")
        con.close()
        return False
    
    # add product
    cur.execute("INSERT INTO products (itemId, title, price, url) VALUES (?, ?, ?, ?)", 
                (product_id, title, price, url))
    con.commit()
    con.close()
    print(f"Lade till: {title}")
    return True

def is_new_product(product_id):
    
    # verify if product already is found
    con = sqlite3.connect('found_items.db')
    cur = con.cursor()
    cur.execute("SELECT itemId FROM products WHERE itemId = ?", (product_id,))
    result = cur.fetchone() is None
    con.close()
    return result