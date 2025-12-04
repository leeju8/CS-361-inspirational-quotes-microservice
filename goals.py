from pathlib import Path
from typing import List, Optional
from flask import Flask, jsonify, request
import json

app = Flask(__name__)

DATA_FILE = Path(__file__).with_name("goals.json")


class GoalRepository:
    """Repository for managing goals."""

    def __init__(self, data_file: Path):
        self.data_file = data_file

    def _read_all(self) -> List[dict]:
        if not self.data_file.exists():
            return []
        with self.data_file.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _write_all(self, goals: List[dict]) -> None:
        with self.data_file.open("w", encoding="utf-8") as handle:
            json.dump(goals, handle, indent=4)

    def get_all(self) -> List[dict]:
        return self._read_all()

    def get_by_id(self, goal_id: int) -> Optional[dict]:
        goals = self._read_all()
        for goal in goals:
            if goal["id"] == goal_id:
                return goal
        return None

    def create(self, goal_text: str) -> dict:
        goals = self._read_all()
        new_goal = {
            "id": len(goals) + 1,
            "goal": goal_text,
            "completed": False,
        }
        goals.append(new_goal)
        self._write_all(goals)
        return new_goal

    def mark_completed(self, goal_id: int) -> Optional[dict]:
        goals = self._read_all()
        for goal in goals:
            if goal["id"] == goal_id:
                goal["completed"] = True
                self._write_all(goals)
                return goal
        return None


repository = GoalRepository(DATA_FILE)


def parse_goal_payload() -> str:
    """Validate incoming payloads."""
    data = request.get_json(silent=True) or {}
    goal_text = data.get("goal", "").strip()
    if not goal_text:
        raise ValueError("Request JSON must include a non-empty 'goal' field.")
    return goal_text


# Root route for health check
@app.route("/", methods=["GET"])
def root():
    return jsonify({"service": "Goal Tracker", "status": "running", "endpoints": ["/goals"]}), 200

# GET all goals
@app.route("/goals", methods=["GET"])
def get_goals():
    goals = repository.get_all()
    return jsonify({"goals": goals, "count": len(goals)}), 200


# POST new goal
@app.route("/goals", methods=["POST"])
def add_goal():
    try:
        goal_text = parse_goal_payload()
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    new_goal = repository.create(goal_text)
    return (
        jsonify({"message": "Goal created successfully!", "goal": new_goal}),
        201,
    )


# PUT mark goal as completed
@app.route("/goals/<int:goal_id>", methods=["PUT"])
def complete_goal(goal_id):
    updated_goal = repository.mark_completed(goal_id)
    if not updated_goal:
        return jsonify({"error": "Goal not found"}), 404

    return (
        jsonify({"message": "Goal marked as completed!", "goal": updated_goal}),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5004)

