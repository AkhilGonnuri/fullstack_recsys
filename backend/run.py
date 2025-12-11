import json
from datetime import datetime
from flask.json import jsonify
from flask import request
import requests

from flask import render_template

from app import app, db, manager, migrate
from app.model import User, Movie, Interaction

# API server (your api.py runs here)
API_ADDRESS = 'http://127.0.0.1:8000'


@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()

    # Correct URL (no % formatting)
    url = f"{API_ADDRESS}/api/recommend"

    # Call the API
    response = requests.post(url, json=data)
    res = json.loads(response.content)

    # Convert movie IDs returned into DB rows
    recommend_db_items = [
        Movie.query.filter_by(id=ids).first()
        for ids in res["result"]
    ]

    recommend_items = [
        {"id": item.id, "title": item.title, "genre": item.genre}
        for item in recommend_db_items
        if item is not None
    ]

    return {"result": recommend_items}


@app.route('/init', methods=['GET'])
def init():
    all_db_items = Movie.query.all()
    all_items = sorted([
        {
            "id": item.id,
            "title": item.title,
            "genre": item.genre,
            "date": datetime.strftime(item.date, "%Y-%b-%d"),
        }
        for item in all_db_items
    ], key=lambda x: x["id"])
    return {"result": all_items}


@manager.command
def run():
    app.run()


if __name__ == "__main__":
    manager.run()
