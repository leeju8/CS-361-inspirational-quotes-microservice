#!/usr/bin/env python3
"""
Main integration program that communicates with all four microservices.
Run each microservice in a separate terminal before running this program.
"""

import requests
import json
from typing import Optional

# Microservice URLs
QUOTES_URL = "http://localhost:5001"
FUNFACTS_URL = "http://localhost:5002"
REFLECTIONS_URL = "http://localhost:5003"
GOALS_URL = "http://localhost:5004"


def print_separator():
    """Prints a visual separator line."""
    print("\n" + "=" * 60 + "\n")


def get_quote() -> None:
    """Fetches and displays a random inspirational quote from the quotes service."""
    try:
        response = requests.get(f"{QUOTES_URL}/api/quote")
        if response.status_code == 200:
            quote_data = response.json()
            print(f"\nInspirational Quote:")
            print(f"   \"{quote_data.get('quote', 'N/A')}\"")
            print(f"   (ID: {quote_data.get('id', 'N/A')})")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Quotes microservice.")
        print("   Make sure it's running on port 5001.")
    except Exception as e:
        print(f"Error: {e}")


def get_funfact() -> None:
    """Fetches and displays a random fun fact from the fun facts service."""
    try:
        response = requests.get(f"{FUNFACTS_URL}/funfact")
        if response.status_code == 200:
            fact_data = response.json()
            print(f"\nFun Fact:")
            print(f"   {fact_data.get('fact', 'N/A')}")
            print(f"   (ID: {fact_data.get('id', 'N/A')})")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Fun Facts microservice.")
        print("   Make sure it's running on port 5002.")
    except Exception as e:
        print(f"Error: {e}")


def add_funfact() -> None:
    """Prompts user for a fun fact and adds it to the fun facts service."""
    fact_text = input("\nEnter a fun fact to add: ").strip()
    if not fact_text:
        print("Error: Fun fact cannot be empty.")
        return

    try:
        response = requests.post(
            f"{FUNFACTS_URL}/funfact",
            json={"fact": fact_text},
            headers={"Content-Type": "application/json"},
        )
        if response.status_code == 201:
            result = response.json()
            print(f"\n{result.get('message', 'Fun fact added!')}")
            print(f"   Fact: {result.get('fact', {}).get('fact', 'N/A')}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Fun Facts microservice.")
        print("   Make sure it's running on port 5002.")
    except Exception as e:
        print(f"Error: {e}")


def add_reflection() -> None:
    """Prompts user for a daily reflection and saves it to the reflections service."""
    reflection_text = input("\nEnter your reflection for today: ").strip()
    if not reflection_text:
        print("Error: Reflection cannot be empty.")
        return

    try:
        response = requests.post(
            f"{REFLECTIONS_URL}/reflection",
            json={"reflection": reflection_text},
            headers={"Content-Type": "application/json"},
        )
        if response.status_code == 201:
            result = response.json()
            print(f"\n{result.get('message', 'Reflection saved!')}")
            reflection = result.get("reflection", {})
            print(f"   Date: {reflection.get('date', 'N/A')}")
            print(f"   Reflection: {reflection.get('reflection', 'N/A')}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Reflections microservice.")
        print("   Make sure it's running on port 5003.")
    except Exception as e:
        print(f"Error: {e}")


def view_today_reflection() -> None:
    """Fetches and displays today's reflection from the reflections service."""
    try:
        response = requests.get(f"{REFLECTIONS_URL}/reflection/today")
        if response.status_code == 200:
            reflection_data = response.json()
            print(f"\nToday's Reflection:")
            print(f"   Date: {reflection_data.get('date', 'N/A')}")
            print(f"   Reflection: {reflection_data.get('reflection', 'N/A')}")
        elif response.status_code == 404:
            print("\nNo reflection found for today.")
            print("   Use option 4 to add a reflection.")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Reflections microservice.")
        print("   Make sure it's running on port 5003.")
    except Exception as e:
        print(f"Error: {e}")


def view_goals() -> None:
    """Fetches and displays all goals from the goals service."""
    try:
        response = requests.get(f"{GOALS_URL}/goals")
        if response.status_code == 200:
            data = response.json()
            goals = data.get("goals", [])
            count = data.get("count", 0)

            print(f"\nYour Goals ({count} total):")
            if not goals:
                print("   No goals yet. Use option 7 to create one!")
            else:
                for goal in goals:
                    status = "[DONE]" if goal.get("completed", False) else "[IN PROGRESS]"
                    print(f"   {status} [{goal.get('id', 'N/A')}] {goal.get('goal', 'N/A')}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Goals microservice.")
        print("   Make sure it's running on port 5004.")
    except Exception as e:
        print(f"Error: {e}")


def add_goal() -> None:
    """Prompts user for a new goal and adds it to the goals service."""
    goal_text = input("\nEnter a new goal: ").strip()
    if not goal_text:
        print("Error: Goal cannot be empty.")
        return

    try:
        response = requests.post(
            f"{GOALS_URL}/goals",
            json={"goal": goal_text},
            headers={"Content-Type": "application/json"},
        )
        if response.status_code == 201:
            result = response.json()
            print(f"\n{result.get('message', 'Goal created!')}")
            goal = result.get("goal", {})
            print(f"   Goal: {goal.get('goal', 'N/A')}")
            print(f"   ID: {goal.get('id', 'N/A')}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Goals microservice.")
        print("   Make sure it's running on port 5004.")
    except Exception as e:
        print(f"Error: {e}")


def complete_goal() -> None:
    """Marks a goal as completed in the goals service."""
    view_goals()
    try:
        goal_id = int(input("\nEnter the ID of the goal to mark as completed: "))
    except ValueError:
        print("Error: Please enter a valid number.")
        return

    try:
        response = requests.put(f"{GOALS_URL}/goals/{goal_id}")
        if response.status_code == 200:
            result = response.json()
            print(f"\n{result.get('message', 'Goal completed!')}")
            goal = result.get("goal", {})
            print(f"   Goal: {goal.get('goal', 'N/A')}")
        elif response.status_code == 404:
            print("Error: Goal not found.")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Goals microservice.")
        print("   Make sure it's running on port 5004.")
    except Exception as e:
        print(f"Error: {e}")


def print_menu():
    """Displays the main menu with all available options."""
    print_separator()
    print("Microservices Integration Menu")
    print_separator()
    print("1. Get Inspirational Quote")
    print("2. Get Fun Fact")
    print("3. Add Fun Fact")
    print("4. Add Daily Reflection")
    print("5. View Today's Reflection")
    print("6. View All Goals")
    print("7. Add New Goal")
    print("8. Mark Goal as Completed")
    print("9. Exit")
    print_separator()


def main():
    """Main program loop that handles user input and routes to appropriate functions."""
    print("\nWelcome to the Microservices Integration Program!")
    print("\nNote: Make sure all microservices are running:")
    print("   - Quotes: port 5001")
    print("   - Fun Facts: port 5002")
    print("   - Reflections: port 5003")
    print("   - Goals: port 5004")

    while True:
        print_menu()
        choice = input("Select an option (1-9): ").strip()

        if choice == "1":
            get_quote()
        elif choice == "2":
            get_funfact()
        elif choice == "3":
            add_funfact()
        elif choice == "4":
            add_reflection()
        elif choice == "5":
            view_today_reflection()
        elif choice == "6":
            view_goals()
        elif choice == "7":
            add_goal()
        elif choice == "8":
            complete_goal()
        elif choice == "9":
            print("\nGoodbye! Thanks for using the microservices integration.")
            break
        else:
            print("\nInvalid option. Please select 1-9.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()

