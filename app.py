from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 세션 관리에 필요한 시크릿 키

# MySQL 데이터베이스 설정 (자신의 MySQL 정보로 수정)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:871006kiann*@localhost/makerton'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 전화번호를 국제 표준 형식으로 변환하는 함수
def format_phone_number(phone):
    # 한국 전화번호의 경우 국가 코드 +82 추가 및 앞자리 0 제거
    if phone.startswith('0'):
        return '+82' + phone[1:]
    return phone

# 해당 부분은 데이터베이스로 데이터를 저장하고 불러옴
# 사용자 모델 정의 (User 테이블)
class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(10), nullable=False)
    phone_num = db.Column(db.String(20), nullable=False, unique=True)
    signup_t = db.Column(db.TIMESTAMP, nullable=False, default=db.func.now())

# 즐겨찾기 장소 모델 정의 (UserPlace 테이블)
class UserPlace(db.Model):
    __tablename__ = 'UserPlace'
    place_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    place_name = db.Column(db.String(100), nullable=False)

# savedplace 테이블 모델 정의 (savedplace 테이블)
class SavedPlace(db.Model):
    __tablename__ = 'savedplace'
    savedplace_id = db.Column(db.Integer, primary_key=True)
    savedplace_name = db.Column(db.String(100), nullable=True)

# 데이터베이스 생성
with app.app_context():
    db.create_all()

# 메인 페이지 라우팅
@app.route('/')
def home():
    session.pop('place_name', None)             # 세션의 place_name 초기화
    user_name = session.get('user_name')        # 세션에서 사용자 이름 가져오기
    return render_template('html/index.html', user_name=user_name)

# 로그인 페이지 라우팅
@app.route('/signup')
def signup():
    return render_template('html/signup.html')

# 회원가입 페이지 라우팅
@app.route('/newsignup')
def newsignup():
    return render_template('html/newsignup.html', error_message=None)

# 회원 가입 처리
@app.route('/signup', methods=['POST'])
def register():
    name = request.form['name']
    phone = request.form['phone']

    # 전화번호 형식 변환 (필요에 따라 사용)
    formatted_phone = format_phone_number(phone)

    try:
        # 중복된 전화번호 확인
        existing_user = User.query.filter_by(phone_num=formatted_phone).first()
        if existing_user:
            error_message = "이미 존재하는 전화번호입니다."
            return render_template('html/newsignup.html', error_message=error_message)

        # 새로운 사용자 생성
        new_user = User(user_name=name, phone_num=formatted_phone)
        db.session.add(new_user)
        db.session.commit()

        # 회원가입 완료 후 메인 페이지로 재이동
        session['user_name'] = name
        return redirect(url_for('home'))

    except Exception as e:
        error_message = f"회원 가입 중 오류가 발생했습니다: {e}"
        return render_template('html/newsignup.html', error_message=error_message)

# 로그인 처리
@app.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    phone = request.form['phone']

    # 전화번호 형식 변환 (필요에 따라 사용)
    formatted_phone = format_phone_number(phone)

    # 데이터베이스에서 입력한 정보와 일치하는 사용자 조회
    user = User.query.filter_by(user_name=name, phone_num=formatted_phone).first()

    if user:
        # 로그인 성공: 세션에 사용자 정보 저장
        session['user_name'] = user.user_name
        return redirect(url_for('home'))
    else:
        # 로그인 실패: 오류 메시지 전달
        error_message = "입력한 정보와 일치하는 사용자가 없습니다."
        return render_template('html/signup.html', error_message=error_message)

# 유저 개인 페이지용 템플릿
@app.route('/user_profile')
def user_profile():
    user_name = session.get('user_name')
    if user_name:
        return render_template('html/user_profile.html', user_name=user_name, place_name=session.get('place_name'))
    else:
        return redirect(url_for('home'))

# 로그아웃 처리
@app.route('/logout')
def logout():
    session.pop('user_name', None)
    session.pop('place_name', None)
    return redirect(url_for('home'))

# # 검색된 장소를 세션에 저장
# @app.route('/save_search', methods=['POST'])
# def save_search():
#     data = request.get_json()
#     place = data['place']

#     # 데이터베이스에서 검색된 장소가 있는지 확인
#     saved_place = SavedPlace.query.filter_by(savedplace_name=place).first()

#     if saved_place:  # 장소가 데이터베이스에 존재하면
#         session['place_name'] = saved_place.savedplace_name  # 세션에 장소 저장
#         return jsonify({'status': 'success'})
#     else:
#         return jsonify({'status': 'error', 'message': '해당 장소는 데이터베이스에 저장되어 있지 않습니다.'})

# 화재 대처 서비스 페이지 라우팅
@app.route('/fireservice')
def fireservice():
    user_name = session.get('user_name')            # 세션에서 사용자 이름 가져오기
    place_name = session.get('place_name')          # 세션에서 장소 정보 가져오기
    if place_name:           # 검색된 장소가 있을 경우
        return render_template('html/fireservice.html', user_name=user_name, place_name=place_name)
    else:                    # 검색된 장소가 없을 경우
        return render_template('html/fireservice.html', user_name=user_name, place_name=None)

if __name__ == '__main__':
    app.run(debug=True)