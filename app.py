from flask import Flask, render_template, url_for, request
from datetime import date
from flask_sqlalchemy import SQLAlchemy
import calendar
import locale
import math
from datetime import datetime, date, time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
today_num = int(date.today().strftime("%d"))
current_month = int(date.today().strftime("%m"))
current_year = int(date.today().strftime("%y"))


class Article(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    day_id = db.Column(db.INTEGER, nullable=False)
    month_id = db.Column(db.INTEGER, nullable=False)
    year_id = db.Column(db.INTEGER, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(100), default=None)
    homework = db.Column(db.TEXT, default=None)
    is_homework_exists = db.Column(db.TEXT, default='0')

    def __repr__(self):
        return '<Article %r>' % self.id


def return_days(moth_id):
    classes = Article.query.filter_by(month_id=moth_id).all()
    return classes


def return_one_day(day_id, year_id, month_id):
    classes = Article.query.filter_by(month_id=month_id, year_id="20" + year_id, day_id=day_id).all()
    return classes


def days_mass(year, month):
    x = calendar.monthrange(year, month)[1]
    mas = [None] * (x + 1)
    for day in range(1, x + 1):
        mas[day] = calendar.day_name[calendar.weekday(year, month, day)].title()
    return mas


def dates(parm, year, month):
    c = calendar.Calendar(firstweekday=parm)
    monthcal = c.monthdatescalendar(year, month)

    try:
        dates = [day for week in monthcal for day in week if
                 day.weekday() == parm and day.month == month]
        return dates
    except IndexError:
        print('No date found')


@app.route('/db_add')
def db_routine():
    with open("classes.txt", encoding='utf-8') as file:
        content = file.read()
        content = content.split("BEGIN")
        i = 0
        for x in content:
            x = x.split("\n")
            content[i] = list(filter(None, x))
            i += 1
        j = [calendar.MONDAY, calendar.TUESDAY, calendar.WEDNESDAY, calendar.THURSDAY, calendar.FRIDAY]
        ptr = 0
        for x in content:
            dat = dates(j[ptr], 2021, 12)
            for z in dat:
                for y in x:
                    y = y.split("=")
                    article = Article(day_id=z.day, month_id=z.month, year_id=z.year, type=y[0], subject=y[1],
                                      link=y[2])
                    db.session.add(article)  # remove to recreate
            ptr += 1
    db.session.commit()  # remove to recreate
    return '0'
    # article = Article(day_id=)


@app.route('/get_task', methods=['GET'])
def get_task():
    day_id = request.args.get('day_id')
    year_id = request.args.get('year_id')
    month_id = request.args.get('month_id')
    classes = return_one_day(day_id, year_id, month_id)
    header = calendar.day_name[calendar.weekday(int(year_id), int(month_id), int(day_id))].title()
    return render_template('get_task.html', classes=classes, day_id=day_id, year_id=year_id, month_id=month_id,
                           header=header, size=len(classes))


@app.route('/add_task', methods=['POST', 'GET'])
def add_task():
    if request.method == 'POST':
        day_id = request.args.get('day_id')
        month_id = request.args.get('month_id')
        year_id = request.args.get('year_id')
        subject = request.form['subject']
        homework = request.form['homework']
        Node = Article.query.filter_by(month_id=month_id, year_id="20" + year_id, day_id=day_id,
                                       subject=subject)
        if Node is not None:
            Node.update(dict(homework=homework, is_homework_exists=1))
            db.session.commit()
        return '0'
    if request.method == 'GET':
        day_id = request.args.get('day_id')
        month_id = request.args.get('month_id')
        year_id = request.args.get('year_id')
        classes = return_one_day(day_id, year_id, month_id)
        return render_template('add_task.html', classes=classes, size=len(classes))


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
            month_name = calendar.month_name[int(month)]
            classes = return_days(int(month))
            return render_template('index.html', day_name=day_name, day_amount=day_amount, day_header=day_header,
                                   working_month=int(month), year=year, align_before=align_before,
                                   day_in_prev=day_in_prev, aligin_after=aligin_after, month_name=month_name,
                                   classes=classes)
        else:
            pass
    else:
        pass
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
    month_name = calendar.month_name[current_month]
    classes = return_days(current_month)
    return render_template('index.html', day_name=day_name, day_amount=day_amount, day_header=day_header,
                           working_month=current_month, year=str(current_year), align_before=align_before,
                           day_in_prev=day_in_prev, aligin_after=aligin_after, month_name=month_name, classes=classes)


if __name__ == '__main__':
    app.run(debug=True)
