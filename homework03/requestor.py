import requests

# Chose or adjust a response accordingly
# (make sure to change the port)

response = requests.get(url="http://localhost:5026/animals")
# response = requests.get(url="http://localhost:5026/animals/head/bunny")
# response = requests.get(url="http://localhost:5026/animals/legs/6")


print(f'Response Code: {response.status_code} \n')
print(f'Response: \n {response.json()}')
print(f'\n Headers:{response.headers}')