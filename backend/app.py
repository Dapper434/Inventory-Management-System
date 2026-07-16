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
    # loop through inventory to find specific item
    for item in inventory:
        if item.get("id") == item_id:
            return jsonify(item), 200
    
    return jsonify({"error": "Not found"}), 404


@app.route('/inventory', methods=['POST'])
def add_item():
    # get the body data from the request
    data = request.json
    
    new_item = {
        "id": len(inventory) + 1,
        "name": data.get("name"),
        "price": data.get("price"),
        "stock": data.get("stock")
    }    

     # check if we can autofill details depending on product name
    product_data = fetch_openfoodfacts_data(data.get("name", ""))
    if product_data:
        new_item["brands"] = product_data.get("brands", "")
        new_item["ingredients_text"] = product_data.get("ingredients_text", "")

    # save item
    inventory.append(new_item)
    return jsonify(new_item), 201

   
@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    data = request.json
    
    # find the item and update only the fields provided
    for item in inventory:
        if item.get("id") == item_id:
            if "name" in data:
                item["name"] = data["name"]
            if "price" in data:
                item["price"] = data["price"]
            if "stock" in data:
                item["stock"] = data["stock"]
            return jsonify(item), 200
            
    return jsonify({"error": "Not found"}), 404

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory
    
    for item in inventory:
        if item.get("id") == item_id:
            inventory.remove(item)
            return jsonify({"message": "Deleted"}), 200
            
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
 
