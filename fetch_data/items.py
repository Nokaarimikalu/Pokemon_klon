import os
import requests

# Konfiguration
BASE_URL = "https://pokeapi.co/api/v2/item"
SAVE_PATH = "assets/items_sprites"
TOTAL_ITEMS = 2045  # Deine Datenbank-Referenz

def download_item_sprites():
    # Ordner erstellen, falls er nicht existiert
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)
        print(f"Ordner {SAVE_PATH} wurde erstellt.")

    print(f"Starte Download von {TOTAL_ITEMS} Item-Sprites...")

    # Wir nutzen ein Limit, um alle Items in einer Liste zu bekommen
    # Oder wir loopen durch die IDs 1 bis 2045
    for item_id in range(1, TOTAL_ITEMS + 1):
        try:
            # 1. Daten vom Item abrufen
            response = requests.get(f"{BASE_URL}/{item_id}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                item_name = data['name']
                sprite_url = data['sprites']['default']

                if sprite_url:
                    # 2. Bild herunterladen
                    img_data = requests.get(sprite_url).content
                    filename = f"{item_id}.png" # Speichert als ID (z.B. 1.png)
                    
                    with open(os.path.join(SAVE_PATH, filename), 'wb') as handler:
                        handler.write(img_data)
                    
                    if item_id % 50 == 0:
                        print(f"Fortschritt: {item_id}/{TOTAL_ITEMS} heruntergeladen...")
                else:
                    print(f"Item {item_id} ({item_name}) hat kein Sprite.")
            else:
                if response.status_code == 404:
                    continue # Manche IDs könnten in der API fehlen
                print(f"Fehler bei ID {item_id}: Status {response.status_code}")

        except Exception as e:
            print(f"Fehler bei ID {item_id}: {e}")

    print("Download abgeschlossen!")

if __name__ == "__main__":
    download_item_sprites()