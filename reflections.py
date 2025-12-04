from pathlib import Path
from typing import List, Optional
from flask import Flask, jsonify, request
import json
from datetime import datetime

app = Flask(__name__)

DATA_FILE = Path(__file__).with_name("reflections.json")


class ReflectionRepository:
    """Repository for managing daily reflections."""

    def __init__(self, data_file: Path):
        self.data_file = data_file

    def _read_all(self) -> List[dict]:
        if not self.data_file.exists():
            return []
        with self.data_file.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _write_all(self, reflections: List[dict]) -> None:
        with self.data_file.open("w", encoding="utf-8") as handle:
            json.dump(reflections, handle, indent=4)

    def get_all(self) -> List[dict]:
        return self._read_all()

    def get_today(self) -> Optional[dict]:
        today = datetime.now().strftime("%Y-%m-%d")
        reflections = self._read_all()
        for reflection in reflections:
            if reflection.get("date") == today:
                return reflection
        return None

    def create(self, reflection_text: str) -> dict:
        reflections = self._read_all()
        today = datetime.now().strftime("%Y-%m-%d")
        new_reflection = {
            "id": len(reflections) + 1,
            "date": today,
            "reflection": reflection_text,
        }
        reflections.append(new_reflection)
        self._write_all(reflections)
        return new_reflection


repository = ReflectionRepository(DATA_FILE)


def parse_reflection_payload() -> str:
    """Validate incoming payloads."""
    data = request.get_json(silent=True) or {}
    reflection_text = data.get("reflection", "").strip()
    if not reflection_text:
        raise ValueError("Request JSON must include a non-empty 'reflection' field.")
    return reflection_text


# Root route for health check
@app.route("/", methods=["GET"])
def root():
    return jsonify({"service": "Daily Reflections", "status": "running", "endpoints": ["/reflection", "/reflection/today"]}), 200

# POST new reflection
@app.route("/reflection", methods=["POST"])
def add_reflection():
    try:
        reflection_text = parse_reflection_payload()
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    new_reflection = repository.create(reflection_text)
    return (
        jsonify(
            {
                "message": "Reflection saved successfully!",
                "reflection": new_reflection,
            }
        ),
        201,
    )


# GET today's reflection
@app.route("/reflection/today", methods=["GET"])
def get_today_reflection():
    reflection = repository.get_today()
    if not reflection:
        return (
            jsonify(
                {
                    "message": "No reflection found for today.",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                }
            ),
            404,
        )
    return jsonify(reflection), 200


if __name__ == "__main__":
    app.run(debug=True, port=5003)

