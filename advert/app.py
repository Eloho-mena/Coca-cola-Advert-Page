from flask import Flask, request,jsonify, render_template
from models import db, Comment, Advert


app = Flask(__name__, static_folder='static', template_folder='templates')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


import routes

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

