import random
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/random_numbers', methods=['POST'])
def generate_random_numbers():
    n = request.json.get('n')
    if n is None or not isinstance(n, int) or n < 1:
        return jsonify({'error': 'Invalid input'}), 400
    numbers = [random.randint(1, n) for _ in range(n)]
    return jsonify({'numbers': numbers})

if __name__ == '__main__':
    app.run()
