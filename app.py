from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from numpy import extract
from sklearn.linear_model import LinearRegression
import pandas as pd
import pickle
from datetime import datetime
from sqlalchemy import func, extract


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense_tracker.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

another_expenses = []
expenses = []

# Define Goal model
class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Goal('{self.description}', '{self.amount}', '{self.target_date}')"

# Route for setting up goals
@app.route('/set_goal', methods=['POST'])
def set_goal():
    user_id = 1  # Placeholder for user identification, replace with actual user id retrieval
    description = request.form['description']
    amount = float(request.form['amount'])
    target_date = datetime.strptime(request.form['target_date'], '%Y-%m-%d').date()

    new_goal = Goal(user_id=user_id, description=description, amount=amount, target_date=target_date)
    db.session.add(new_goal)
    db.session.commit()

    return jsonify({'message': 'Goal set successfully!'})

# Route for getting all goals
@app.route('/get_goals')
def get_goals():
    user_id = 1  # Placeholder for user identification, replace with actual user id retrieval
    goals = Goal.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': goal.id, 'description': goal.description, 'amount': goal.amount, 'target_date': goal.target_date.strftime('%Y-%m-%d')} for goal in goals])


# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Routes
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your username and password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        date_str = request.form['date']

        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        
        category = request.form['category']
        expense = Expense(description=description, amount=amount, date=date, category=category, user_id=current_user.id)
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!')
        return redirect(url_for('view_expenses'))
    return render_template('add_expense.html')

@app.route('/view_expenses')
@login_required
def view_expenses():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    
    return render_template('view_expenses.html', expenses=expenses)




def get_monthly_expenses(user_id, year):
    monthly_expenses = db.session.query(
        extract('month', Expense.date).label('month'),
        func.sum(Expense.amount).label('total')
    ).filter_by(user_id=user_id)\
     .filter(extract('year', Expense.date) == year)\
     .group_by(extract('month', Expense.date))\
     .order_by(extract('month', Expense.date))\
     .all()
    
    return monthly_expenses

def prepare_data(monthly_expenses):
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    labels = []
    values = []

    for month, total in monthly_expenses:
        labels.append(month_names[month - 1])  # Convert month number to month name
        values.append(total)
    
    data = {
        'labels': labels,
        'values': values
    }
    
    return data
@app.route('/report')
@login_required
def report():
    current_year = datetime.now().year
    monthly_expenses = get_monthly_expenses(current_user.id, current_year)
    data = prepare_data(monthly_expenses)
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    total_expense = sum(expense.amount for expense in expenses)
    return render_template('report.html', total_expense=total_expense,data=data)

@app.route('/expenses-data')
def expenses():
    # Sample data (replace with your actual data)
    current_year = datetime.now().year
    monthly_expenses = get_monthly_expenses(current_user.id, current_year)
    data = prepare_data(monthly_expenses)
    
    return data

@app.route('/packet', methods=['GET', 'POST'])
@login_required
def packet():

    
    if 'category' in request.form:
            
            # Handling the expense form
            category = request.form['category']
            amount = request.form['amount']
            date = request.form['date']
            # Assuming you have a function to add expenses to the database
            new_expense = Expense(user_id=current_user.id, category=category, amount=amount, date=date)
            db.session.add(new_expense)
            db.session.commit()
    elif 'sourceofincome' in request.form:
            
            # Handling the income form
            sourceofincome = request.form['sourceofincome']
            amount = request.form['amount']
            date = datetime.today();
            # Add new entry to another_expenses list
            another_expenses.append({'sourceofincome': sourceofincome, 'amount': amount, 'date': date})
        

            return redirect(url_for('packet'))
     # Get the current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_year_month = datetime.now().strftime('%Y-%m')

    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    expenses_filter = [expense for expense in expenses if expense.date.strftime('%Y-%m') == current_year_month]
    
    




    # current_date = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
       
        # Get form data
        sourceofincome = request.form['sourceofincome']
        amount = request.form['amount']
    
        
        
        
        # Add new entry to another_expenses list
        another_expenses.append({'sourceofincome': sourceofincome, 'amount': amount})
        
        # Redirect to the same page to display the updated table
        return redirect(url_for('packet'))
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('packet.html', expenses=expenses_filter, another_expenses=another_expenses, current_date=current_date)

    
    
    

@app.route('/predict_expense', methods=['GET', 'POST'])
@login_required
def predict_expense():
    if request.method == 'POST':
        month = int(request.form['month'])
        year = int(request.form['year'])
        category = request.form['category']

        # Load the model
        with open('expense_predictor.pkl', 'rb') as f:
            model = pickle.load(f)

        # Prepare the input data
        user_id = current_user.id
        input_data = pd.DataFrame({'month': [month], 'year': [year], 'user_id': [user_id]})

        # Make a prediction
        predicted_amount = model.predict(input_data)[0]

        # Retrieve past expenses
        query = Expense.query.filter_by(user_id=current_user.id)
        if category:
            query = query.filter_by(category=category)
        past_expenses = query.all()

        # Prepare data for chart
        past_expenses_data = [{'date': exp.date, 'amount': exp.amount, 'category': exp.category} for exp in past_expenses]
        past_expenses_df = pd.DataFrame(past_expenses_data)
        past_expenses_df['date'] = pd.to_datetime(past_expenses_df['date'])
        past_expenses_df = past_expenses_df.sort_values(by='date')
        
        labels = past_expenses_df['date'].dt.strftime('%Y-%m').tolist()
        data = past_expenses_df['amount'].tolist()

        return render_template('predict_expense.html', predicted_amount=predicted_amount, past_expenses=past_expenses, labels=labels, data=data)

    return render_template('predict_expense.html')

def train_model():
    expenses = Expense.query.all()
    data = []
    for expense in expenses:
        data.append({
            'description': expense.description,
            'amount': expense.amount,
            'category': expense.category,
            'date': expense.date,
            'user_id': expense.user_id
        })

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year

    # Prepare the data for training
    X = df[['month', 'year', 'user_id']]
    y = df['amount']

    # Train the model
    model = LinearRegression()
    model.fit(X, y)

    # Save the model to a file
    with open('expense_predictor.pkl', 'wb') as f:
        pickle.dump(model, f)

# Initialize the database and create tables
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
        train_model()  # Train the model
    app.run(debug=True)
