from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("gamehub.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    conn = get_db_connection()
    games = conn.execute("SELECT * FROM games").fetchall()
    conn.close()
    return render_template("index.html", games=games)

@app.route("/games")
def view_games():
    conn = get_db_connection()
    games = conn.execute("SELECT * FROM games").fetchall()
    conn.close()

    return {
        "games": [dict(game) for game in games]
    }

@app.route("/games/search")
def search_games():
    search_query = request.args.get("q", "")

    conn = get_db_connection()

    games = conn.execute(
        "SELECT * FROM games WHERE title LIKE ?",
        ('%' + search_query + '%',)
    ).fetchall()

    conn.close()

    return {
        "games": [dict(game) for game in games]
    }

@app.route("/games/price/<float:max_price>")
def filter_price(max_price):
    conn = get_db_connection()

    games = conn.execute(
    "SELECT * FROM games WHERE price <= ?",
    (max_price,)
).fetchall()

    conn.close()

    return {
        "games": [dict(game) for game in games]
    }

@app.route("/games/genre/<genre>")
def filter_genre(genre):
    conn = get_db_connection()

    games = conn.execute(
        "SELECT * FROM games WHERE genre = ?",
        (genre,)
    ).fetchall()

    conn.close()

    return {
        "games": [dict(game) for game in games]
    }

@app.route("/games/<int:game_id>")
def game_details(game_id):
    conn = get_db_connection()
   
    game = conn.execute(
        "SELECT * FROM games WHERE id = ?",
        (game_id,)
    ).fetchone()

    conn.close()

    if game is None:
        return {"error": "Game not found"}, 404

    return {"game": dict(game)}

@app.route("/games/add", methods=["POST"])
def add_game():
    data = request.get_json()

    conn = get_db_connection()

    conn.execute(
        """
        INSERT INTO games (title, genre, price, description, image)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            data["title"],
            data["genre"],
            data["price"],
            data["description"],
            data["image"]
        )
    )

    conn.commit()
    conn.close()

    return {"message": "Game added successfully"}, 201

if __name__ == "__main__":
    app.run(debug=True)


