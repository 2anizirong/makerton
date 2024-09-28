-- 테이블 생성 SQL - User
CREATE TABLE User
(
    `user_id`    INT            NOT NULL    AUTO_INCREMENT COMMENT 'user_id', 
    `user_name`  VARCHAR(10)    NOT NULL    COMMENT 'user_name', 
    `phone_num`  VARCHAR(20)    NOT NULL    COMMENT 'phone_num', 
    `signup_t`   TIMESTAMP      NOT NULL    COMMENT 'signup_t', 
     PRIMARY KEY (user_id)
);

-- 테이블 생성 SQL - UserPlace
CREATE TABLE UserPlace
(
    `place_id`    INT             NOT NULL    AUTO_INCREMENT COMMENT 'place_id', 
    `user_id`     INT             NOT NULL    COMMENT 'user_id', 
    `place_name`  VARCHAR(100)    NOT NULL    COMMENT 'place_name', 
     PRIMARY KEY (place_id)
);

-- Foreign Key 설정 SQL - UserPlace(user_id) -> User(user_id)
ALTER TABLE UserPlace
    ADD CONSTRAINT FK_UserPlace_user_id_User_user_id FOREIGN KEY (user_id)
        REFERENCES User (user_id) ON DELETE RESTRICT ON UPDATE RESTRICT;
        
-- 테이블 생성 SQL - savedplace
CREATE TABLE savedplace
(
    `savedplace_id`    INT             NOT NULL    AUTO_INCREMENT COMMENT 'savedplace_id', 
    `savedplace_name`  VARCHAR(100)    NULL        COMMENT 'savedplace_name', 
     PRIMARY KEY (savedplace_id)
);

-- 저장된 장소 테이블에 장소 저장해두기 
INSERT INTO savedplace (savedplace_name) 
VALUES ('서울 중구 필동로1길 30 동국대학교 중앙도서관 4F');

-- 사용자 데이터 삭제하고 초기화하기
DELETE FROM User;
ALTER TABLE User AUTO_INCREMENT = 1;
