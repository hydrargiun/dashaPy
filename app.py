from flask import Flask, render_template, url_for
from datetime import date

app = Flask(__name__)


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
    return render_template('index.html', day_name=day_name, day_mas=day_mas)


if __name__ == '__main__':
    app.run(debug=True)
