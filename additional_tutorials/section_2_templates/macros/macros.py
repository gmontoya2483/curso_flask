from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    myList = [123, 345, 4343, 545]
    myOtherList = [122, 3234, 34534, 65464]
    return render_template('index.html', name='Gsbriel', my_list=myList, my_other_list=myOtherList)


if __name__ == '__main__':
    app.run(debug=True)
