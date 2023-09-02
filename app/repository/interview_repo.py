from typing import Dict

from app import Session
from app.repository.model.interview import Interview
from app.domain.request_domain import InterviewCreateInfo


class InterviewRepository:
    def __init__(self, session=None):
        self.session = Session()

    # def read_category_all(self):
        # try:
        #     category_items = self.session.query(CategoryItems).all()
        # except:
        #     self.session.rollback()
        #     raise
        # finally:
        #     self.session.close()
        # return category_items

    def create_interview(self, user_id: int, interview_info: InterviewCreateInfo):
        try:
            interview = Interview(user_id=user_id, **dict(interview_info))
            
            # self.session.add(interview)
            # self.session.commit()
            return 200
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
        return category_items