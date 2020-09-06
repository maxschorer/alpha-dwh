import json
import requests

HEADERS = {
  'authority': 'xmyygv64cjantodrggj3uu5xrq.appsync-api.us-west-2.amazonaws.com',
  'accept': 'application/json, text/plain, */*',
  'x-amz-user-agent': 'aws-amplify/3.4.2 js',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
  'x-api-key': 'da2-wsknunntiffb3hyxefmrxez4ma',
  'content-type': 'application/json; charset=UTF-8',
  'sec-fetch-site': 'cross-site',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'accept-language': 'en-US,en;q=0.9',
}
URL = 'https://xmyygv64cjantodrggj3uu5xrq.appsync-api.us-west-2.amazonaws.com/graphql'


def api(query, variables=None):
  def get_operation(query):
    return query.strip().split('{')[0].split()[1]
  payload = {
    'operationName': get_operation(query),
    'query': query,
    'variables': variables
  }
  req = requests.post(URL, headers=HEADERS, data=json.dumps(payload))
  return json.loads(req.text)


def get_rank_entities(rank_id):
  QUERY = '''
    query GetRankWithEntities {
      getRank(id: "%s") {
        id
        name
        entities(nextToken: %s, limit: 4450) {
          items {
            id
            name
            sourceId
          }
          nextToken
        }
      }
    }
  '''
  response = api(QUERY % (rank_id, 'null'))
  items = []
  while True:
    items += response['data']['getRank']['entities']['items']
    next_token = response['data']['getRank']['entities']['nextToken']
    if not next_token: break
    response = api(QUERY % (rank_id, '"{}"'.format(next_token)))
  return items
  # return response['data']['getRank']['entities']['items']


def create_rank_entity(rank_id, entity):
  QUERY = '''
    mutation CreateEntityWithRank {
      createEntity(input: {
        sourceId: "%s", name: "%s", rankId: "%s"}) {
        id
        name
      }
    }
  '''

  response = api(QUERY % (entity.get('source_id'), entity.get('name'), entity_id))

