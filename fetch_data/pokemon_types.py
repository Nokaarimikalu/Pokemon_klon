import sqlite3
import requests
import time

con = sqlite3.connect("pokemon_game.db")
cur = con.cursor()

def get_pokemon_types(p_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{p_id}"
    response = requests.get(url)
    data = response.json()
    
    for t_entry in data['types']:
        type_data = {
            'pokemon_id': p_id,
            'type_id': int(t_entry['type']['url'].split('/')[-2]),
            'slot': t_entry['slot']
        }
        save_pokemon_types(type_data)

def save_pokemon_types(type_dict):
   
    sql = """INSERT OR IGNORE INTO pokemon_types (pokemon_id, type_id, slot)
             VALUES (?, ?, ?)"""
    
    values = (type_dict['pokemon_id'], type_dict['type_id'], type_dict['slot'])
    
    cur.execute(sql, values)
    

def main():
    for i in range(1, 152):
        get_pokemon_types(i)
        print(f"Typen für ID {i} gespeichert.")
        time.sleep(0.2) 
    
    con.commit() 
    print("Fertig! Alle Typen-Verknüpfungen sind in der DB.")

if __name__ == "__main__":
    main()