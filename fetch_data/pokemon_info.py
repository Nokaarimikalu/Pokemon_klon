import sqlite3
import requests
import time


con = sqlite3.connect("pokemon_game.db")
cur = con.cursor()



def get_pokemon(name):
    url =  f"https://pokeapi.co/api/v2/pokemon/{name}"
    url_other =  f"https://pokeapi.co/api/v2/pokemon-species/{name}"
    response = requests.get(url)
    response_other = requests.get(url_other)
    cleanedData = filterData(response.json(),response_other.json())
    save_pokemon_data(cleanedData)

    

def filterData(raw_json,raw_json_other):

    flavor_text = "No description available" # Standardwert, falls nix gefunden wird
    for entry in raw_json_other["flavor_text_entries"]:
        if entry["language"]["name"] == "en":
            flavor_text = entry["flavor_text"].replace('\f', ' ').replace('\n', ' ')
            break

    filtered_data = {
        "id": raw_json["id"],
        "name": raw_json["name"],
        "hp": raw_json["stats"][0]["base_stat"],
        "atk": raw_json["stats"][1]["base_stat"],
        "def": raw_json["stats"][2]["base_stat"],
        "sp_atk": raw_json["stats"][3]["base_stat"],
        "sp_def": raw_json["stats"][4]["base_stat"],
        "speed": raw_json["stats"][5]["base_stat"],
        "height": raw_json["height"],
        "weight": raw_json["weight"],
        "base_experience": raw_json["base_experience"],
        "capture_rate": raw_json_other["capture_rate"],
        "gender_rate": raw_json_other["gender_rate"],
        "hatch_counter": raw_json_other["hatch_counter"],
        "growth_rate": raw_json_other["growth_rate"]["name"],
        "flavor_text": flavor_text

    }
    return filtered_data



def save_pokemon_data(data):
    
    save_data = """ 
        INSERT OR IGNORE INTO pokemon_info (
            id, name, hp, atk, def, sp_atk, sp_def, speed, 
            height, weight, base_experience, capture_rate, 
            gender_rate, hatch_counter, growth_rate, flavor_text
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
    """ 
    
    
    values = (
        data["id"], 
        data["name"], 
        data["hp"], 
        data["atk"], 
        data["def"],  
        data["sp_atk"],
        data["sp_def"], 
        data["speed"], 
        data["height"], 
        data["weight"],
        data["base_experience"],
        data["capture_rate"],
        data["gender_rate"],
        data["hatch_counter"],
        data["growth_rate"],
        data["flavor_text"]
    )
    
    cur.execute(save_data, values)
    con.commit()


def main():
    for i in range(1, 152):
        get_pokemon(i)
        time.sleep(0.3)
        print(f"Pokemon ID:{i} geladen", flush=True)

main()