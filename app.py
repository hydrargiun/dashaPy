from flask import Flask, render_template, url_for, request
from datetime import date
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
dayID = 0

class Article(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    day_id = db.Column(db.INTEGER, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(50), default=None)
    homework = db.Column(db.TEXT, default=None)

    def __repr__(self):
        return '<Article %r>' % self.id


day_header = [None] * 32
raw = 0
for x in range(1, 32):
    if x - (1 + raw * 7) == 0:
        day_header[x] = 'Среда'
    elif x - (2 + raw * 7) == 0:
        day_header[x] = 'Четверг'
    elif x - (3 + raw * 7) == 0:
        day_header[x] = 'Пятница'
    elif x - (4 + raw * 7) == 0:
        day_header[x] = 'Суббота'
    elif x - (5 + raw * 7) == 0:
        day_header[x] = 'Воскресенье'
        raw += 1
    elif x - (6 + (raw - 1) * 7) == 0:
        day_header[x] = 'Понедельник'
    elif x - (7 + (raw - 1) * 7) == 0:
        day_header[x] = 'Вторник'
day_header[0] = 0


@app.route('/add_task', methods=['POST', 'GET'])
def add_task():
    if request.method == 'POST':
        day_id = request.args.get('day_id')
        title = request.form['title']
        task_node = Article()
    if request.method == 'GET':
        day_id = request.args.get('day_id')
        if day_id is not None:
            if 1 <= int(day_id) <= 31:
                pass
        else:
            return "Инвалид."
    option = ['1', '2', '3', '4']
    return render_template('add_task.html', option=option)


@app.route('/')
def index():
    today_num = int(date.today().strftime("%d"))
    day_mas = []
    for x in range(0, 32):
        day_mas.append(x)
    day_name = ['0']
    for x in range(1, 32):
        if x != today_num:
            day_name.append('day')
        else:
            day_name.append('today')
    global day_header
    return render_template('index.html', day_name=day_name, day_mas=day_mas, day_header=day_header)


if __name__ == '__main__':
    app.run(debug=True)
