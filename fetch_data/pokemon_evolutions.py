import sqlite3
import requests
import time

con = sqlite3.connect("pokemon_game.db")
cur = con.cursor()

def get_evolutions(species_id):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{species_id}/"
    res = requests.get(url)
    if res.status_code != 200: return
    
    data = res.json()
    chain_url = data['evolution_chain']['url']
    
    # Die Kette abrufen (enthält alle Stufen: z.B. Bisasam -> Bisaknosp -> Bisaflor)
    chain_res = requests.get(chain_url).json()
    chain_data = chain_res['chain']
    
    parse_chain(chain_data)

def parse_chain(current_step):
    
    from_name = current_step['species']['name']
    from_id = int(current_step['species']['url'].split('/')[-2])
    
    for evolution in current_step['evolves_to']:
        to_id = int(evolution['species']['url'].split('/')[-2])
        
        
        details = evolution['evolution_details'][0] if evolution['evolution_details'] else {}
        
        level = details.get('min_level')
        trigger = details.get('trigger', {}).get('name')
        
        item_id = None
        if details.get('item'):
            item_id = int(details['item']['url'].split('/')[-2])
            
        save_evolution(from_id, to_id, level, item_id, trigger)
        
        
        parse_chain(evolution)

def save_evolution(f_id, t_id, lvl, i_id, trigger):
    sql = """INSERT OR IGNORE INTO pokemon_evolutions 
             (from_id, to_id, evolution_level, item_id, trigger_name)
             VALUES (?, ?, ?, ?, ?)"""
    cur.execute(sql, (f_id, t_id, lvl, i_id, trigger))

def main():
    print("Starte Evolution-Download...")
    
    for i in range(1, 1026):
        try:
            get_evolutions(i)
            if i % 20 == 0:
                con.commit()
                print(f"Spezies {i} verarbeitet...")
            time.sleep(0.05) # Kleiner Delay
        except Exception as e:
            continue
            
    con.commit()
    print("Evolutions-Datenbank ist fertig!")

if __name__ == "__main__":
    main()