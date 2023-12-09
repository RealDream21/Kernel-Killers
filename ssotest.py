import requests
from jose import jwt

# Define your Auth0 data
domain = 'YOUR_AUTH0_DOMAIN'
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
audience = 'YOUR_API_AUDIENCE'
grant_type = 'client_credentials'

# Get a token
data = {'client_id': client_id, 'client_secret': client_secret, 'audience': audience, 'grant_type': grant_type}
response = requests.post(f'https://{domain}/oauth/token', data=data)
token = response.json()['access_token']

# Decode the token
header = jwt.get_unverified_header(token)
claims = jwt.get_unverified_claims(token)

print(header)
print(claims)