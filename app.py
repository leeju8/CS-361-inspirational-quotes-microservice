from flask import Flask, jsonify, request
import random, json, os

app = Flask(__name__)

DATA_FILE = "quotes.json"

def load_quotes():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_quotes(quotes):
    with open(DATA_FILE, "w") as f:
        json.dump(quotes, f, indent=4)

# GET random quote
@app.route("/api/quote", methods=["GET"])
def get_quote():
    quotes = load_quotes()
    if not quotes:
        return jsonify({"id": 0, "quote": "No quotes available."}), 404
    return jsonify(random.choice(quotes)), 200

# POST new quote
@app.route("/api/quote", methods=["POST"])
def add_quote():
    data = request.get_json()
    if not data or "quote" not in data:
        return jsonify({"error": "Missing 'quote' field"}), 400

    quotes = load_quotes()
    new_quote = {"id": len(quotes) + 1, "quote": data["quote"]}
    quotes.append(new_quote)
    save_quotes(quotes)

    return jsonify({"message": "Quote added successfully!", "quote": new_quote}), 201

# PUT edit existing quote
@app.route("/api/quote/<int:quote_id>", methods=["PUT"])
def update_quote(quote_id):
    data = request.get_json()

    quotes = load_quotes()
    for q in quotes:
        if q["id"] == quote_id:
            q["quote"] = data["quote"]
            save_quotes(quotes)
            return jsonify({"message": "Quote updated!", "quote": q}), 200

    return jsonify({"error": "Quote not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
