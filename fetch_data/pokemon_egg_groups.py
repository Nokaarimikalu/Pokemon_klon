import sqlite3
import requests
import time

con = sqlite3.connect("pokemon_game.db")
cur = con.cursor()

def get_and_save_egg_groups(pokemon_id):
    # Egg Groups findet man im /pokemon-species/ Endpunkt
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}/"
    res = requests.get(url)
    if res.status_code != 200: return
    
    data = res.json()
    
    for group in data['egg_groups']:
        group_name = group['name']
        
        sql = "INSERT OR IGNORE INTO pokemon_egg_groups (pokemon_id, group_name) VALUES (?, ?)"
        cur.execute(sql, (pokemon_id, group_name))

def main():
    print("Lade Egg Groups...")
    for i in range(1, 1026):
        try:
            get_and_save_egg_groups(i)
            if i % 50 == 0:
                con.commit()
                print(f"Fortschritt: {i}/1025...")
            time.sleep(0.05)
        except:
            continue
    con.commit()
    print("Egg Groups fertig!")

if __name__ == "__main__":
    main()