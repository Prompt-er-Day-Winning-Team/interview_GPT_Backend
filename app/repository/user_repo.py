import bcrypt
from fastapi import HTTPException
from typing import Dict

from app import Session
from app.repository.model.user import User
from app.domain.request_domain import UserInfo, InterviewCreateInfo


class UserRepository:
    def __init__(self, session=None):
        self.session = Session()

    def create_user(self, user_info: UserInfo):
        try:
            exist_user = (
                self.session.query(User).filter(User.id == user_info.id).first()
            )
            if exist_user:
                raise HTTPException(status_code=401, detail="이미 존재하는 아이디입니다.")
            user_info.password = bcrypt.hashpw(
                user_info.password.encode("utf-8"), bcrypt.gensalt()
            )
            user = User(**dict(user_info))
            self.session.add(user)
            self.session.commit()
            return {"userId": user.user_id}
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def check_user(self, user_info: UserInfo):
        try:
            user = self.session.query(User).filter(User.id == user_info.id).first()
            check_result = bcrypt.checkpw(
                user_info.password.encode("utf-8"), user.password.encode("utf-8")
            )
            if check_result:
                return {"userId": user.user_id}
            raise HTTPException(status_code=401, detail="로그인 정보가 틀립니다.")
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
