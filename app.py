from flask import Flask, make_response, jsonify, request
import sqlite3
import json

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/api/orders/<order_number>', methods=['GET'])
def get_order(order_number):
    if request.method == 'GET':
        _conn = sqlite3.connect('orders.db')
        _cur = _conn.cursor()
        order_number = int(order_number)
        _cur.execute("SELECT * FROM orders WHERE order_number= ?", (order_number,))
        _order = _cur.fetchall()
        _conn.close()
        if _order:
            column = [x[0] for x in _cur.description]
            order = [{column[0]: row[0], column[1]: row[1], column[2]: row[2]} for row in _order]
            response = make_response(json.dumps(order), 200)
            response.mimetype = 'application/json'
            return response
        else:
            response = make_response(json.dumps([]), 404)
            return response


@app.route('/api/orders', methods=['GET'])
def get_orders():
    if request.method == 'GET':
        _conn = sqlite3.connect('orders.db')
        _cur = _conn.cursor()
        _cur.execute(f"SELECT * FROM orders")
        _orders = _cur.fetchall()
        _conn.close()
        if _orders:
            column = [x[0] for x in _cur.description]
            del _orders[0]
            orders = [{column[0]: row[0], column[1]: row[1], column[2]: row[2]} for row in _orders]
            response = make_response(json.dumps(orders), 200)
            response.mimetype = 'application/json'
            return response
        else:
            response = make_response([], 404)
            return response


@app.route('/api', methods=['PUT'])
def pay_orders():
    return jsonify({'metoda': 'PUT'})


if __name__ == '__main__':
    app.run()
