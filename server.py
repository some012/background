from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Хранилище данных в виде словаря
products = {}

# Создание карточки продукта
@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    price = data.get('price')

    product_id = str(len(products) + 1)
    products[product_id] = {'name': name, 'description': description, 'price': price}

    return jsonify({'id': product_id}), 201

# Чтение карточки продукта
@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    if product_id in products:
        return jsonify(products[product_id]), 200
    else:
        return jsonify({'error': 'Product not found'}), 404

# Скачивание списка продуктов
@app.route('/products_download', methods=['GET'])
def download_products():
    response = app.response_class(
        response=json.dumps(products),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run()
