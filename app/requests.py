import requests
import json

secret_key = None


def configure_request(app):
  '''function that configures the request object needed for running the application'''
  global secret_key
  secret_key = app.config['SECRET_KEY']
  
def get_quotes():
  url = "https://quotes15.p.rapidapi.com/quotes/random/"
  headers = {
    "X-RapidAPI-Host": "quotes15.p.rapidapi.com",
    "X-RapidAPI-Key": "f1ecc09012msh395fade747664ecp14465djsn59429cc15c85"
  }

  response = requests.request("GET", url, headers=headers)
  
  results = json.loads(response.text)
  content = results.get('content')
  data = results.get('originator')
  name = data['name']
  quote = f'{content} {name}'
  print(quote)
  
  return quote
  