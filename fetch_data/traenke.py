import sqlite3
import requests
import time

con = sqlite3.connect("pokemon_game.db")
cur = con.cursor()

def get_item(item_id):
    url = f"https://pokeapi.co/api/v2/item/{item_id}"
    res = requests.get(url)
    if res.status_code != 200:
        return None
    
    data = res.json()
    
    # Beschreibung filtern (wir nehmen die erste englische)
    description = ""
    for entry in data['flavor_text_entries']:
        if entry['language']['name'] == 'en':
            description = entry['text']
            break
            
    # Move ID extrahieren, falls vorhanden (für TMs)
    m_id = None
    if 'baby-trigger-for' in data: # Manche Items triggern Moves
        pass # Spezielle Logik falls nötig
    
    # Die PokéAPI speichert TMs oft in einem separaten Feld
    # Wir schauen, ob 'machines' Daten enthält
    if data.get('machines'):
        # Wir brauchen eine zweite API-Abfrage für die Machine-URL
        m_url = data['machines'][0]['machine']['url']
        m_data = requests.get(m_url).json()
        m_id = int(m_data['move']['url'].split('/')[-2])

    item_data = {
        'id': data['id'],
        'name': data['name'],
        'description': description,
        'category': data['category']['name'],
        'price': data['cost'],
        'fling_power': data.get('fling_power'),
        'effect_value': None # Meistens in 'effect_entries' versteckt, falls du es brauchst
    }
    
    # Effect Value ist komplexer, wir nehmen hier oft die 'fling_effect' ID oder lassen es NULL
    return item_data, m_id

def save_item(d, m_id):
    sql = """INSERT OR IGNORE INTO items 
             (id, name, description, category, price, fling_power, effect_value, move_id)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    
    values = (
        d['id'], d['name'], d['description'], d['category'], 
        d['price'], d['fling_power'], d['effect_value'], m_id
    )
    cur.execute(sql, values)

def main():
    print("Starte Item-Download (IDs 1 bis ca. 2100)...")
    # Es gibt über 2000 Items inklusive aller TMs und Beeren
    for i in range(1, 2101):
        try:
            result = get_item(i)
            if result:
                item_data, m_id = result
                save_item(item_data, m_id)
                if i % 50 == 0:
                    con.commit()
                    print(f"Item {i} verarbeitet...", flush=True)
            time.sleep(0.05)
        except Exception as e:
            continue

    con.commit()
    print("Item-Datenbank ist vollständig!")

if __name__ == "__main__":
    main()