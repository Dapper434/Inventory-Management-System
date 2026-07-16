from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

# setup flask app
app = Flask(__name__)
CORS(app)

# our fake database for now
inventory = []

def fetch_openfoodfacts_data(product_name):
    # search for the product by name on the external api
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={product_name}&search_simple=1&action=process&json=1"
    try:
        headers = {"User-Agent": "IMS-App-Lab/1.0"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # grab the first product if we found any
            if data.get("products") and len(data["products"]) > 0:
                return data["products"][0]
    except Exception:
        pass
    return None


@app.route('/inventory', methods=['GET'])
def get_all_items():
    # return the whole list
    return jsonify(inventory), 200

app.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    # loop through inventory to find the specific item
    for item in inventory:
        if item.get("id") == item_id:
            return jsonify(item), 200
    
    return jsonify({"error": "Not found"}), 404
