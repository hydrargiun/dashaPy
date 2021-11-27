from flask import Flask, render_template, url_for
from datetime import date

app = Flask(__name__)
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
