from flask import Flask, jsonify, render_template
from app.db import users_collection, addresses_collection, credit_cards_collection

app = Flask(__name__)


@app.route("/")
def index() -> None:
    return render_template("index.html")


@app.route("/users")
def get_users() -> None:
    users = list(users_collection.find({}, {"_id": 0}))
    return jsonify(users)


@app.route("/addresses")
def get_addresses() -> None:
    addresses = list(addresses_collection.find({}, {"_id": 0}))
    return jsonify(addresses)


@app.route("/credit-cards")
def get_credit_cards() -> None:
    credit_cards = list(credit_cards_collection.find({}, {"_id": 0}))
    return jsonify(credit_cards)


@app.route("/fetch-all")
def fetch_all() -> None:
    from app.tasks import fetch_users, fetch_addresses, fetch_credit_cards

    fetch_users.delay()
    fetch_addresses.delay()
    fetch_credit_cards.delay()
    return jsonify({"status": "Fetching started"})


if __name__ == "__main__":
    app.run(debug=True)
