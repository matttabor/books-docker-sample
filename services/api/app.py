from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

client = MongoClient("mongodb://db:27017")
db = client.books

@app.route('/')
def home():
    return "Hello"

@app.route('/books/')
def get_books():
    # response_object = {
    #     'container_id': os.uname()[1],
    #     'books': []
    # };

    _books = db.books.find()
    books = []
    for book in _books:
        books.append({
            'name': book['name'],
            'author': book['author']
        })
    #response_object.books = books
    return jsonify(books), 200

@app.route('/books/', methods=["POST"])
def create_book():
    request_data = request.get_json()
    if db.books.find({'name': request_data['name']}).count() > 0:
        return jsonify({'message': 'book already exists'}), 400

    new_book = {
        'name': request_data['name'],
        'author': request_data['author']
    }

    db.books.insert_one(new_book)

    return jsonify({'message': 'new book created'}), 201

@app.route('/books/<string:name>', methods=["DELETE"])
def delete_book(name):
    result = db.books.delete_one({'name': name})
    if result.deleted_count > 0:
        return jsonify({'message': '{} removed successfully'.format(name)}), 204
    else:
        return jsonify({'message': 'Cannot find a book by the name {}'.format(name)}), 400

@app.route('/books/<string:name>')
def get_book(name):
    book = db.books.find_one({'name': name})
    if book:
        return jsonify({'name': book['name'], 'author': book['author']}), 200
    else:
        return jsonify({'message': 'Cannot find a book by the name {}'.format(name)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)