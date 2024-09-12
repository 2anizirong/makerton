from flask import Flask, render_template  # Flask 클래스, render_template 함수 가져오기

app = Flask(__name__)

# 메인 페이지 라우팅
@app.route('/')
def home():
    return render_template('/html/index.html')  # templates 폴더 안의 index.html 파일을 렌더링

# 회원가입 페이지 라우팅
@app.route('/signup')
def signup():
    return render_template('/html/signup.html')  # templates 폴더 안의 signup.html 파일을 렌더링

# 화재 대처 서비스 페이지 라우팅
@app.route('/fireservice')
def fireservice():
    return render_template('/html/fireservice.html')  # templates 폴더 안의 fireservice.html 파일을 렌더링

if __name__ == '__main__':
    app.run(debug=True)
