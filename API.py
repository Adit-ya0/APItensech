from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Pantry API base URL
PANTRY_API_BASE_URL = "https://getpantry.cloud/apiv1/pantry/b6057d6b-762a-4a1e-8724-2eab6a74a6e4/"


@app.route('/')
def index():
    return "hello welcome"

@app.route('/add-item', methods=['POST'])
def add_item():
    data = request.get_json()
    pantry_id = data.get('pantry_id')
    basket_key = data.get('basket_key')
    value = data.get('value')

    # Prepare the URL for storing key-value pair in the Pantry
    url = f'{PANTRY_API_BASE_URL}basket/{pantry_id}/{basket_key}'

    # Make a POST request to store the key-value pair
    response = requests.post(url, json={'value': value})

    if response.status_code == 200:
        return jsonify({'message': 'Item added successfully'}), 201
    else:
        return jsonify({'message': 'Failed to add item'}), 500

@app.route('/get-item', methods=['GET'])
def get_item():
    pantry_id = request.args.get('pantry_id')
    basket_key = request.args.get('basket_key')

    # Prepare the URL for retrieving the value from the Pantry
    url = f'{PANTRY_API_BASE_URL}basket/{basket_key}'

    # Make a GET request to retrieve the value
    response = requests.get(url)

    if response.status_code == 200:
        item_data = response.json()
        value = item_data.get('value')
        return jsonify({'value': value}), 200
    else:
        return jsonify({'message': 'Item not found'}), 404

@app.route('/list-baskets', methods=['GET'])
def list_baskets():
    pantry_id = request.args.get('pantry_id')

    # Prepare the URL for listing baskets in the Pantry
    url = f'{PANTRY_API_BASE_URL}basket/{pantry_id}'

    # Make a GET request to list baskets
    response = requests.get(url)

    if response.status_code == 200:
        baskets = response.json()
        return jsonify({'baskets': baskets}), 200
    else:
        return jsonify({'message': 'Pantry not found'}), 404

@app.route('/update-item', methods=['PUT'])
def update_item():
    data = request.get_json()
    pantry_id = data.get('pantry_id')
    basket_key = data.get('basket_key')
    new_value = data.get('new_value')

    # Prepare the URL for updating the value in the Pantry
    url = f'{PANTRY_API_BASE_URL}basket/{pantry_id}/{basket_key}'

    # Make a PUT request to update the value
    response = requests.put(url, json={'value': new_value})

    if response.status_code == 200:
        return jsonify({'message': 'Item updated successfully'}), 200
    else:
        return jsonify({'message': 'Item not found'}), 404

@app.route('/delete-item', methods=['DELETE'])
def delete_item():
    pantry_id = request.args.get('pantry_id')
    basket_key = request.args.get('basket_key')

    # Prepare the URL for deleting the item from the Pantry
    url = f'{PANTRY_API_BASE_URL}basket/{pantry_id}/{basket_key}'

    # Make a DELETE request to delete the item
    response = requests.delete(url)

    if response.status_code == 200:
        return '', 204
    else:
        return jsonify({'message': 'Item not found'}), 404

if _name_ == '__main__':
    app.run(debug=True)
