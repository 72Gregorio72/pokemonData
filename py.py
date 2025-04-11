import requests
import csv
import time

API_BASE = "https://pokeapi.co/api/v2/pokemon"
POKEMON_COUNT = 1010  # Numero totale di Pokémon ufficiali

def get_stats(pokemon_id, session):
    url = f"{API_BASE}/{pokemon_id}"
    res = session.get(url)
    if res.status_code != 200:
        return None
    data = res.json()
    stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
    return [
        pokemon_id,
        stats.get('hp', 0),
        stats.get('attack', 0),
        stats.get('defense', 0),
        stats.get('special-attack', 0),
        stats.get('special-defense', 0),
        stats.get('speed', 0),
    ]

# CSV output
with open('pokemon_stats.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id_pokemon', 'hp', 'attack', 'defense', 'sp.atk', 'sp.def', 'speed'])

    with requests.Session() as session:
        for pid in range(1, POKEMON_COUNT + 1):
            try:
                row = get_stats(pid, session)
                if row:
                    writer.writerow(row)
                else:
                    writer.writerow([pid] + [''] * 6)
            except Exception as e:
                print(f"Errore con Pokémon ID {pid}: {e}")
                writer.writerow([pid] + [''] * 6)

            # Progresso visibile ogni 50
            if pid % 50 == 0 or pid == POKEMON_COUNT:
                print(f"Processati {pid}/{POKEMON_COUNT} Pokémon...")
            
            time.sleep(0.05)  # Piccolo delay per sicurezza contro rate limiting
