"""Server for creating Flask app and handling routes"""

from flask import Flask, render_template
from model import connect_to_db, db

app = Flask(__name__)


@app.route('/')
def display_homepage():
    """Show homepage"""
    return render_template('index.html')


if __name__ == "__main__":

    connect_to_db(app)
    app.run(debug=True)
