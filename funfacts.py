from pathlib import Path
from typing import List, Optional
from flask import Flask, jsonify, request
import json
import random

app = Flask(__name__)

DATA_FILE = Path(__file__).with_name("funfacts.json")


class FunFactRepository:
    """Repository for managing fun facts."""

    def __init__(self, data_file: Path):
        self.data_file = data_file

    def _read_all(self) -> List[dict]:
        if not self.data_file.exists():
            return []
        with self.data_file.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _write_all(self, facts: List[dict]) -> None:
        with self.data_file.open("w", encoding="utf-8") as handle:
            json.dump(facts, handle, indent=4)

    def get_all(self) -> List[dict]:
        return self._read_all()

    def get_random(self) -> Optional[dict]:
        facts = self._read_all()
        if not facts:
            return None
        return random.choice(facts)

    def create(self, fact_text: str) -> dict:
        facts = self._read_all()
        new_fact = {"id": len(facts) + 1, "fact": fact_text}
        facts.append(new_fact)
        self._write_all(facts)
        return new_fact


repository = FunFactRepository(DATA_FILE)


def parse_fact_payload() -> str:
    """Validate incoming payloads."""
    data = request.get_json(silent=True) or {}
    fact_text = data.get("fact", "").strip()
    if not fact_text:
        raise ValueError("Request JSON must include a non-empty 'fact' field.")
    return fact_text


# Root route for health check
@app.route("/", methods=["GET"])
def root():
    return jsonify({"service": "Fun Facts", "status": "running", "endpoints": ["/funfact"]}), 200

# GET random fun fact
@app.route("/funfact", methods=["GET"])
def get_funfact():
    fact = repository.get_random()
    if not fact:
        return jsonify({"id": 0, "fact": "No fun facts available."}), 404
    return jsonify(fact), 200


# POST new fun fact
@app.route("/funfact", methods=["POST"])
def add_funfact():
    try:
        fact_text = parse_fact_payload()
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    new_fact = repository.create(fact_text)
    return (
        jsonify({"message": "Fun fact added successfully!", "fact": new_fact}),
        201,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5002)

