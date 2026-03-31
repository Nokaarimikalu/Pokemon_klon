import sqlite3
import requests
import time

con = sqlite3.connect("pokemon_game.db")
cur = con.cursor()

def get_and_save_abilities(pokemon_id):
    # Abilities findet man im normalen /pokemon/ Endpunkt
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
    res = requests.get(url)
    if res.status_code != 200: return
    
    data = res.json()
    
    for ability_entry in data['abilities']:
        ability_name = ability_entry['ability']['name']
        # Umwandlung von Boolean (True/False) zu Integer (1/0) für SQL
        is_hidden = 1 if ability_entry['is_hidden'] else 0
        
        sql = "INSERT OR IGNORE INTO pokemon_abilities (pokemon_id, ability_name, is_hidden) VALUES (?, ?, ?)"
        cur.execute(sql, (pokemon_id, ability_name, is_hidden))

def main():
    print("Lade Abilities...")
    for i in range(1, 1026):
        try:
            get_and_save_abilities(i)
            if i % 50 == 0:
                con.commit()
                print(f"Fortschritt: {i}/1025...")
            time.sleep(0.05)
        except:
            continue
    con.commit()
    print("Abilities fertig!")

if __name__ == "__main__":
    main()