from flask import Flask, render_template        #  flasck 클래스, render_template 함수 가져오기

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('/html/index.html')

if __name__ == '__main__':
    app.run(debug=True)
