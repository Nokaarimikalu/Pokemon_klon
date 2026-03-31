import sqlite3
import requests
import time


con = sqlite3.connect("pokemon_game.db")
cur = con.cursor()

# fetchen der typen fuer die typen tabelle
# ========================================================================================================
# ========================================================================================================
# ========================================================================================================
# ========================================================================================================


def filter_types_data(raw_json):
    filtered_types_data = {
        'id': raw_json['id'],
        'name': raw_json['name']
    }

    return filtered_types_data


def save_types_data(filtered_json):
    types_data = """ INSERT OR IGNORE INTO types (id, name)
                     VALUES (?,?)"""

    values = (filtered_json['id'], filtered_json['name'])

    cur.execute(types_data, values)
    con.commit()


def get_type_data_db():
    
    for type_id in range(1, 19):
        url = f"https://pokeapi.co/api/v2/type/{type_id}"
        response = requests.get(url)
        real_types_data = filter_types_data(response.json())
        save_types_data(real_types_data)
        print(f"type_id {type_id} ist erfolgreich runtergeladen")
        time.sleep(0.5)
# ========================================================================================================
# ========================================================================================================
# ========================================================================================================
# ========================================================================================================





# ========================================================================================================
# ========================================================================================================
# ========================================================================================================
# ========================================================================================================

def get_type_effectness_db():

    for type_id in range(1, 19):
        url = f"https://pokeapi.co/api/v2/type/{type_id}"
        response = requests.get(url)
        sort_type_effectness(response, type_id)
        print(f"type_id {type_id} ist erfolgreich runtergeladen")
        time.sleep(0.5)
        
    
def sort_type_effectness(response, type_id):
    damage_relations_json = response.json()['damage_relations']
    damage_type_id = type_id
    double_dmg_to_json = damage_relations_json['double_damage_to']
    half_dmg_to_json = damage_relations_json['half_damage_to']
    no_dmg_to_json = damage_relations_json['no_damage_to']
    double_results = fetch_damage_to_loop(double_dmg_to_json, damage_type_id, 2)
    half_results = fetch_damage_to_loop(half_dmg_to_json, damage_type_id, 0.5)
    no_results = fetch_damage_to_loop(no_dmg_to_json, damage_type_id, 0)    
    save_type_effectness(double_results)
    save_type_effectness(half_results)
    save_type_effectness(no_results)




def fetch_damage_to_loop(target_type, damage_type_id, damage_factor):
    list_of_all_dmg_to = []
    for i in target_type:
        url = i['url']
        target_type_id = int(url.split('/')[-2])

        list_of_all_dmg_to.append(
            {
                'damage_type_id': damage_type_id,
                'target_type_id': target_type_id,
                'damage_factor': damage_factor
        })
    return list_of_all_dmg_to

def save_type_effectness(result_list):
    types_effectivness_data = """ INSERT OR IGNORE INTO type_efficiency (damage_type_id, target_type_id, damage_factor)
                                  VALUES (?,?,?)"""

    for entry in result_list:
        values = (entry['damage_type_id'], entry['target_type_id'], entry['damage_factor'])
        cur.execute(types_effectivness_data, values)


    con.commit()



def main():
    #get_type_data_db()
    get_type_effectness_db()
    con.close()


if __name__ == "__main__":
    main()