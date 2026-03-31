import sqlite3
import requests
import time


con = sqlite3.connect("pokemon_game.db")
cur = con.cursor()

def get_and_save_pokemon_moves(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"ID {pokemon_id} nicht gefunden.")
        return
    
    data = response.json()
    
    for move_entry in data['moves']:
        move_id = int(move_entry['move']['url'].split('/')[-2])
        

        if move_entry['version_group_details']:
            latest = move_entry['version_group_details'][-1]
            
            move_data = {
                'pokemon_id': pokemon_id,
                'move_id': move_id,
                'level_learned': latest['level_learned_at'],
                'learn_method': latest['move_learn_method']['name']
            }
            save_relation(move_data)

def save_relation(d):

    sql = """INSERT OR IGNORE INTO pokemon_moves 
             (pokemon_id, move_id, level_learned, learn_method)
             VALUES (?, ?, ?, ?)"""
    
    values = (
        d['pokemon_id'], 
        d['move_id'], 
        d['level_learned'], 
        d['learn_method']
    )
    
    try:
        cur.execute(sql, values)
    except sqlite3.OperationalError as e:
        print(f"Fehler: Hast du die Tabelle 'pokemon_moves' erstellt? {e}")

def main():
    print("Starte Download der Verknüpfungen (1 bis 1025)...")
    for i in range(1, 1026):
        try:
            get_and_save_pokemon_moves(i)
            if i % 10 == 0:
                con.commit()
                print(f"Fortschritt: {i}/1025 Pokemon fertig.", flush=True)
            time.sleep(0.1)
        except Exception as e:
            print(f"Kritischer Fehler bei ID {i}: {e}")
            continue

    con.commit()
    print("Fertig! Alle Moves sind den Pokemon zugeordnet.")

if __name__ == "__main__":
    main()