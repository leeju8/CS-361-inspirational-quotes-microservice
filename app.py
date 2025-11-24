from pathlib import Path
from typing import List, Optional
from flask import Flask, jsonify, request
import json, random

app = Flask(__name__)

DATA_FILE = Path(__file__).with_name("quotes.json")


class QuoteRepository:
    """Simple repository that hides the storage mechanism and avoids shotgun edits."""

    def __init__(self, data_file: Path):
        self.data_file = data_file

    def _read_all(self) -> List[dict]:
        if not self.data_file.exists():
            return []
        with self.data_file.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _write_all(self, quotes: List[dict]) -> None:
        with self.data_file.open("w", encoding="utf-8") as handle:
            json.dump(quotes, handle, indent=4)

    def get_all(self) -> List[dict]:
        return self._read_all()

    def get_random(self) -> Optional[dict]:
        quotes = self._read_all()
        if not quotes:
            return None
        return random.choice(quotes)

    def create(self, quote_text: str) -> dict:
        quotes = self._read_all()
        new_quote = {"id": len(quotes) + 1, "quote": quote_text}
        quotes.append(new_quote)
        self._write_all(quotes)
        return new_quote

    def update(self, quote_id: int, quote_text: str) -> Optional[dict]:
        quotes = self._read_all()
        for quote in quotes:
            if quote["id"] == quote_id:
                quote["quote"] = quote_text
                self._write_all(quotes)
                return quote
        return None


repository = QuoteRepository(DATA_FILE)


def parse_quote_payload() -> str:
    """Validate incoming payloads so every route enforces the same contract."""
    data = request.get_json(silent=True) or {}
    quote_text = data.get("quote", "").strip()
    if not quote_text:
        raise ValueError("Request JSON must include a non-empty 'quote' field.")
    return quote_text

# GET random quote
@app.route("/api/quote", methods=["GET"])
def get_quote():
    quote = repository.get_random()
    if not quote:
        return jsonify({"id": 0, "quote": "No quotes available."}), 404
    return jsonify(quote), 200

# POST new quote
@app.route("/api/quote", methods=["POST"])
def add_quote():
    try:
        quote_text = parse_quote_payload()
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    new_quote = repository.create(quote_text)
    return (
        jsonify({"message": "Quote added successfully!", "quote": new_quote}),
        201,
    )

# PUT edit existing quote
@app.route("/api/quote/<int:quote_id>", methods=["PUT"])
def update_quote(quote_id):
    try:
        quote_text = parse_quote_payload()
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    updated_quote = repository.update(quote_id, quote_text)
    if not updated_quote:
        return jsonify({"error": "Quote not found"}), 404

    return jsonify({"message": "Quote updated!", "quote": updated_quote}), 200

if __name__ == "__main__":
    app.run(debug=True)
