import os
import requests
import time

# Dein Zielordner für das Python-Game
assets_path = "assets/sprites"
if not os.path.exists(assets_path):
    os.makedirs(assets_path)

def download_pokemon_sprites(p_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{p_id}/"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return
        
        sprites = res.json()['sprites']
        
        # Deine gewünschte Benennung für das Python-Game:
        # f = front, b = back, sf = shiny front, sb = shiny back
        download_tasks = [
            (sprites.get('front_default'), f"{p_id}_f.png"),
            (sprites.get('back_default'), f"{p_id}_b.png"),
            (sprites.get('front_shiny'), f"{p_id}_sf.png"),
            (sprites.get('back_shiny'), f"{p_id}_sb.png")
        ]
        
        for img_url, filename in download_tasks:
            if img_url:
                img_data = requests.get(img_url).content
                with open(os.path.join(assets_path, filename), 'wb') as f:
                    f.write(img_data)
                    
    except Exception as e:
        print(f"Fehler bei ID {p_id}: {e}")

def main():
    print(f"--- Starte Sprite-Download für dein Python-Game (ID 1 bis 1025) ---")
    
    for i in range(340, 1026):
        download_pokemon_sprites(i)
        
        if i % 10 == 0:
            print(f"Fortschritt: {i}/1025 Pokemon fertig geladen...", flush=True)
        
        # 0.05s Pause, damit die API dich nicht blockiert
        time.sleep(0.05)

    print("\nFERTIG! Alle Sprites sind im Ordner 'assets/sprites'.")
    print("Viel Erfolg beim Programmieren des Kampfsystems!")

if __name__ == "__main__":
    main()