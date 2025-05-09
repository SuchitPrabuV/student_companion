from flask import Flask, render_template, request, redirect, url_for,send_file
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///goals.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    collaborator = db.Column(db.String(100))
    status = db.Column(db.String(50))
    done = db.Column(db.Boolean, default=False)

@app.route('/goals.html')
def goals():
    goals = Goal.query.all()
    return render_template('/groupgoals.html', goals=goals)

@app.route('/timetable.html')
def timetable():
    goals = Goal.query.all()
    #return render_template('/timetable.html')
    return render_template('/timetablealt.html')

@app.route('/todo.html')
def todo():
    goals = Goal.query.all()
    return render_template('/todolist.html')
    

@app.route('/ttscript.js')
def ttscript():
    return send_file('static/ttscript.js')

@app.route('/ttstyles.css')
def ttstyles():
    return send_file('static/ttstyles.css')


@app.route('/')
def index():
    return render_template('student_companion.html')

@app.route('/add', methods=['POST'])
def add():
    description = request.form['description']
    collaborator = request.form['collaborator']
    status = request.form['status']
    new_goal = Goal(description=description, collaborator=collaborator, status=status)
    db.session.add(new_goal)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle/<int:goal_id>')
def toggle(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    goal.done = not goal.done
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:goal_id>')
def delete(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    db.session.delete(goal)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
