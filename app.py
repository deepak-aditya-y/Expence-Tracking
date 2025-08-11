from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

# Flask app setup
app = Flask(__name__)

# Database file path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "expense_tracker.db")

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Database Models
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    reason = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.relationship('Category', backref=db.backref('expenses', lazy=True))

class BorrowRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    reason = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(10))  # 'lent' or 'borrowed'

# Create tables and default categories
with app.app_context():
    db.create_all()
    if Category.query.count() == 0:
        default_categories = ['Food', 'Transport', 'Groceries', 'Entertainment', 'Bills', 'Other']
        for name in default_categories:
            db.session.add(Category(name=name))
        db.session.commit()

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add")
def add():
    categories = Category.query.all()
    return render_template("add.html", categories=categories)

@app.route("/monthly")
def monthly():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    return render_template("monthly.html", expenses=expenses)

@app.route("/loans")
def loans():
    loans = BorrowRecord.query.order_by(BorrowRecord.date.desc()).all()
    return render_template("loans.html", loans=loans)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
