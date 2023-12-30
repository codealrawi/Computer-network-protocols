import requests

def get_random_numbers(n):
    response = requests.post('http://localhost:5000/random_numbers', json={'n': n})
    if response.ok:
        return response.json().get('numbers')
    else:
        return None
