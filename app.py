from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)

# Models
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    expenses = db.relationship('Expense', backref='category')

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

# Routes
@app.route('/')
def index():
    expenses = Expense.query.all()
    categories = Category.query.all()
    return render_template('index.html', expenses=expenses, categories=categories)

@app.route('/add', methods=['POST'])
def add_expense():
    desc = request.form['description']
    amount = float(request.form['amount'])
    category_id = int(request.form['category_id'])
    new_expense = Expense(description=desc, amount=amount, category_id=category_id)
    db.session.add(new_expense)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if Category.query.count() == 0:
            for name in ['Food', 'Transport', 'Groceries', 'Entertainment', 'Bills', 'Other']:
                db.session.add(Category(name=name))
            db.session.commit()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 4000)), debug=True)
