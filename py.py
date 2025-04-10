import requests
import csv
import time
from tqdm import tqdm

POKEMON_COUNT = 1010  # numero totale di Pokémon ufficiali (aggiornabile)
API_BASE = "https://pokeapi.co/api/v2"

def get_pokemon_moves(pokemon_id):
    url = f"{API_BASE}/pokemon/{pokemon_id}"
    res = requests.get(url)
    if res.status_code != 200:
        return []
    data = res.json()
    level_up_moves = []

    for move_entry in data['moves']:
        for version in move_entry['version_group_details']:
            if version['move_learn_method']['name'] == 'level-up':
                move_url = move_entry['move']['url']
                level_up_moves.append(move_url)
                break  # una sola volta per mossa
    return list(set(level_up_moves))

def get_move_priority(move_url):
    res = requests.get(move_url)
    if res.status_code != 200:
        return (0, 0, 0)
    move = res.json()
    power = move['power'] or 0
    accuracy = move['accuracy'] or 0
    pp = move['pp'] or 0
    return (power, accuracy, -pp)  # PP in negativo per ordinare da meno a più

def get_move_id_from_url(move_url):
    return int(move_url.rstrip('/').split('/')[-1])

def get_top_4_moves(move_urls):
    scored = []
    for url in move_urls:
        try:
            priority = get_move_priority(url)
            scored.append((priority, url))
            time.sleep(0.1)  # evita overload dell'API
        except:
            continue
    top_moves = sorted(scored, key=lambda x: x[0], reverse=True)[:4]
    return [get_move_id_from_url(url) for _, url in top_moves]

# CSV file output
with open('pokemon_top_moves.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['pokemon_id', 'move1_id', 'move2_id', 'move3_id', 'move4_id'])

    for pid in tqdm(range(1, POKEMON_COUNT + 1)):
        try:
            move_urls = get_pokemon_moves(pid)
            if not move_urls:
                writer.writerow([pid, '', '', '', ''])
                continue
            move_ids = get_top_4_moves(move_urls)
            while len(move_ids) < 4:
                move_ids.append('')
            writer.writerow([pid] + move_ids)
        except Exception as e:
            print(f"Errore con il Pokémon {pid}: {e}")
            writer.writerow([pid, '', '', '', ''])
