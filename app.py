import random
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "kn224s-lr4-rps-secret"

CHOICES = ["rock", "scissors", "paper"]

CHOICE_LABELS = {
    "rock":     "Камінь",
    "scissors": "Ножиці",
    "paper":    "Папір",
}

CHOICE_EMOJI = {
    "rock":     "🪨",
    "scissors": "✂️",
    "paper":    "📄",
}

# Камінь б'є ножиці, ножиці ріжуть папір, папір накриває камінь
BEATS = {
    "rock":     "scissors",
    "scissors": "paper",
    "paper":    "rock",
}


def determine_winner(player: str, computer: str) -> str:
    """Повертає 'win', 'lose' або 'draw'."""
    if player == computer:
        return "draw"
    if BEATS[player] == computer:
        return "win"
    return "lose"


def get_score() -> dict:
    return {
        "wins":   session.get("wins", 0),
        "losses": session.get("losses", 0),
        "draws":  session.get("draws", 0),
    }


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        player_choice = request.form.get("choice")

        if player_choice not in CHOICES:
            return redirect(url_for("index"))

        computer_choice = random.choice(CHOICES)
        outcome = determine_winner(player_choice, computer_choice)

        # Оновлення рахунку в сесії
        if outcome == "win":
            session["wins"] = session.get("wins", 0) + 1
        elif outcome == "lose":
            session["losses"] = session.get("losses", 0) + 1
        else:
            session["draws"] = session.get("draws", 0) + 1

        result = {
            "player":   player_choice,
            "computer": computer_choice,
            "outcome":  outcome,
        }

    return render_template(
        "index.html",
        choices=CHOICES,
        labels=CHOICE_LABELS,
        emojis=CHOICE_EMOJI,
        score=get_score(),
        result=result,
    )


@app.route("/reset", methods=["POST"])
def reset():
    session.pop("wins", None)
    session.pop("losses", None)
    session.pop("draws", None)
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
