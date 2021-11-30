from flask import Flask, render_template, url_for, request
from datetime import date
from flask_sqlalchemy import SQLAlchemy
import calendar
import locale
import math

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
dayID = 0
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
today_num = int(date.today().strftime("%d"))
current_month = int(date.today().strftime("%m"))
current_year = int(date.today().strftime("%y"))


class Article(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    day_id = db.Column(db.INTEGER, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(50), default=None)
    homework = db.Column(db.TEXT, default=None)

    def __repr__(self):
        return '<Article %r>' % self.id


def days_mass(year, month):
    x = calendar.monthrange(year, month)[1]
    cur_month = int(date.today().strftime("%m"))
    cal = calendar.Calendar()
    mas = [None] * (x + 1)
    for day in range(1, x + 1):
        mas[day] = calendar.day_name[calendar.weekday(year, month, day)].title()
    return mas


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


@app.route('/', methods=['GET'])
def index():
    month = request.args.get('month')
    year = request.args.get('year')
    if month and year is not None:
        if int(month) != current_month or int(year) != current_year:
            day_amount = calendar.monthrange(int(year), int(month))[1]
            day_name = ['day'] * (day_amount + 1)
            day_header = days_mass(int(year), int(month))
            align_before = calendar.weekday(int(year), int(month), 1)
            if int(month) == 1:
                month_prev = 12
            else:
                month_prev = int(month) - 1
            day_amount_in_prev = calendar.monthrange(int(year), month_prev)[1]
            day_in_prev = []
            for x in range(0, align_before):
                day_in_prev.insert(0, day_amount_in_prev - x)
            aligin_after = (math.ceil((align_before + day_amount) / 7) * 7) - (align_before + day_amount)
            return render_template('index.html', day_name=day_name, day_amount=day_amount, day_header=day_header,
                                   working_month=int(month), year=year, align_before=align_before,
                                   day_in_prev=day_in_prev, aligin_after=aligin_after)
        else:
            pass
    else:
        return "Инвалид."
    day_header = days_mass(current_year, current_month)
    day_name = ['0']
    for x in range(1, 32):
        if x != today_num:
            day_name.append('day')
        else:
            day_name.append('today')
    day_amount = calendar.monthrange(current_year, current_month)[1]
    align_before = calendar.weekday(current_year, current_month, 1)
    if current_month == 1:
        month_prev = 12
    else:
        month_prev = current_month - 1
    day_amount_in_prev = calendar.monthrange(current_year, month_prev)[1]
    day_in_prev = []
    for x in range(0, align_before):
        day_in_prev.insert(0, day_amount_in_prev - x)
    aligin_after = (math.ceil((align_before + day_amount) / 7) * 7) - (align_before + day_amount)
    return render_template('index.html', day_name=day_name, day_amount=day_amount, day_header=day_header,
                           working_month=current_month, year=current_year, align_before=align_before,
                           day_in_prev=day_in_prev, aligin_after=aligin_after)


if __name__ == '__main__':
    app.run(debug=True)
