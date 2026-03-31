import sqlite3
import requests
import time


con = sqlite3.connect("pokemon_game.db")
cur = con.cursor()

def get_move(id):
    url = f"https://pokeapi.co/api/v2/move/{id}"
    response = requests.get(url)
    response_json = response.json()
    filtered_moves_eigenschaften = {
        'id': response_json['id'],
        'name': response_json['name'],
        'power': response_json['power'],
        'accuracy': response_json['accuracy'],
        'pp': response_json['pp'],
        'priority': response_json['priority'],
        'type_id': int(response_json['type']['url'].split('/')[-2]),
        'damage_class': response_json['damage_class']['name']
    }
    return filtered_moves_eigenschaften

def save_moves(move_data):
    
    sql = """INSERT OR IGNORE INTO moves (
                id, name, power, accuracy, pp, priority, type_id, damage_class
             )
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    
  
    values = (
        move_data['id'],
        move_data['name'],
        move_data['power'],
        move_data['accuracy'],
        move_data['pp'],
        move_data['priority'],
        move_data['type_id'],
        move_data['damage_class']
    )
    
    cur.execute(sql, values)


def main():
    
    for i in range(1, 1001):
        try:
            move_data = get_move(i)
            save_moves(move_data)
            print(f"Move ID {i}: {move_data['name']} geladen", flush=True)
            time.sleep(0.1)
        except Exception as e:
            # Falls eine ID nicht existiert (404), überspringen wir sie einfach
            print(f"ID {i} übersprungen oder Fehler: {e}")
            continue
    
    con.commit()
    print("Fertig! Die Move-Bibliothek ist auf dem neuesten Stand.")

main()