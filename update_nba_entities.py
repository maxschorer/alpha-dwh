from bs4 import BeautifulSoup
import json
import requests
import string

import backend

GOAT_RANK = 'b1e25932-6a54-4dff-a3ff-9a960f41d89b'

def add_players(players, letter):
  SOURCE_URL = 'https://www.basketball-reference.com/players/'
  url = SOURCE_URL + letter
  html = requests.get(url).text
  soup = BeautifulSoup(html)
  links = soup.findAll('a')

  for link in links:
    href = link.get('href')
    if not href: continue
    if len(href.split('/')) < 3: continue
    if href.split('/')[2] != letter: continue
    pid = href.split('/')[-1].split('.')[0]
    name = link.get_text()
    players.append({'source_id': pid, 'name': name})


def main():
  # db_players = backend.get_rank_entities(GOAT_RANK)
  db_players = get_rank_entities(GOAT_RANK)
  source_ids = [p['sourceId'] for p in db_players]
  ref_players = []
  for letter in string.ascii_lowercase:
    add_players(ref_players, letter)

  for i, entity in enumerate(ref_players):
    if entity.get('source_id') in source_ids: continue
    backend.create_rank_entity(GOAT_RANK, entity)
    if (i % 10) == 0: print('Completed {}'.format(i))
