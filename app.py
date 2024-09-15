from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from twilio.rest import Client  # Twilio 라이브러리 임포트

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 세션 관리에 필요한 시크릿 키

# # Twilio 설정 (SID와 인증 토큰, 발신 번호를 자신의 Twilio 계정에 맞게 설정하세요)
# TWILIO_ACCOUNT_SID = 'ACed496a6db67ecbafb1106b254414d520'
# TWILIO_AUTH_TOKEN = '3278676f39c7df21eb2c2b5066826005'
# TWILIO_PHONE_NUMBER = '+12078132256'
# client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# # 전화번호를 국제 표준 형식으로 변환하는 함수
# def format_phone_number(phone):
#     # 한국 전화번호의 경우 국가 코드 +82 추가 및 앞자리 0 제거
#     if phone.startswith('0'):
#         return '+82' + phone[1:]
#     return phone

# 사용자 정보 저장 (배열로 간단하게 처리)
users = [{'name': '김이안', 'phone': '01036946460'}]

# 검색 가능한 장소 데이터 예시
available_places = [
    "서울 중구 필동로1길 30 동국대학교 중앙도서관 4F"
]

# 메인 페이지 라우팅
@app.route('/')
def home():
    session.pop('place_name', None)  # 세션의 place_name 초기화
    user_name = session.get('user_name')  # 세션에서 사용자 이름 가져오기
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

    # 회원 가입을 막기 위한 조건 (임의로 항상 오류 처리)
    error_message = "회원 가입이 현재 불가능합니다."

    # try:
    #     # Twilio를 사용해 입력한 번호로 문자 보내기
    #     message = client.messages.create(
    #         body=f"안녕하세요, {name}님. 현재 회원 가입이 불가능합니다.",
    #         from_=TWILIO_PHONE_NUMBER,
    #         to=phone
    #     )
    # except Exception as e:
    #     error_message += f" 문자 발송에 실패했습니다: {e}"


    return render_template('html/newsignup.html', error_message=error_message)

# 로그인 처리
@app.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    phone = request.form['phone']

    # 사용자 정보 확인
    for user in users:
        if user['name'] == name and user['phone'] == phone:
            session['user_name'] = name  # 세션에 사용자 이름 저장
            return redirect(url_for('home'))

    # 로그인 실패 시 오류 메시지 전달
    error_message = "로그인에 실패하셨습니다. 다시 한 번 확인해주세요."
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

# 검색어에 따른 장소 미리보기 제공
@app.route('/search_suggestions')
def search_suggestions():
    query = request.args.get('query', '').lower()
    suggestions = [place for place in available_places if query in place.lower()]
    return jsonify({'suggestions': suggestions})

# 검색된 장소를 세션에 저장
@app.route('/save_search', methods=['POST'])
def save_search():
    data = request.get_json()
    place = data['place']
    if place in available_places:  # 검색된 장소가 available_places에 있는지 확인
        session['place_name'] = place
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': '해당 장소를 저장되어 있지 않습니다.'})


# 화재 대처 서비스 페이지 라우팅
@app.route('/fireservice')
def fireservice():
    user_name = session.get('user_name')  # 세션에서 사용자 이름 가져오기
    place_name = session.get('place_name')  # 세션에서 장소 정보 가져오기
    if place_name:  # 검색된 장소가 있을 경우
        return render_template('html/fireservice.html', user_name=user_name, place_name=place_name)
    else:  # 검색된 장소가 없을 경우
        return render_template('html/fireservice.html', user_name=user_name, place_name=None)

if __name__ == '__main__':
    app.run(debug=True)