import sys
sys.path.append('/Users/eunji/Documents/prompter_day/interview_GPT_Backend')
from app.prompt.request_validation import request_validation
from app.prompt.question import question


from app.prompt.question_validation import question_validation
from app.prompt.persona import persona
from app.prompt.summarize import summarize
from app.prompt.virtual_interview import virtual_interview
from app.prompt.total_statistics import total_statistics
from omegaconf import OmegaConf
import pandas as pd
import json
import time

def main():
    status_dict = {
    1: '아이디어 - 초기 단계로 진출하고자 하는 시장과 해당 시장의 소비자를 이해하는 단계',
    2: '컨셉 기획 - 아이디어를 바탕으로 제품의 컨셉을 기획하는 단계',
    3: '프로토타입 - 컨셉을 구체화한 후 만든 프로토타입을 기준으로, 개선이 필요한 사항을 발견하는 단계',
    4: '출시 - 의도한 대로 제품을 사용하고 있는지를 확인하고, 테스트를 위한 리서치를 시작하는 단계'
    }

    test_data = OmegaConf.load("app/test/test_data.yaml")
    status = test_data.eng.status
    status = status_dict[status]
    service = test_data.eng.product_name
    product_detail = test_data.eng.product_detail
    interview_goal = test_data.eng.interview_goal
    target = test_data.org.target_user
    print("========== request_validation ===============")
    start = time.time()
    validation_res = request_validation(service, product_detail, interview_goal,target)
    end = time.time()
    validation_res = json.loads(validation_res)
    print(validation_res)
    print('시간: ', end - start)
    
    if validation_res['type'] == '문제없음' :
        print("========== question ===============")
        start = time.time()
        question_res = question(status, service, product_detail, interview_goal, target)
        end = time.time()
        print('시간: ', end - start)
        print(question_res)

        print("========== persona ===============")
        start = time.time()
        persona_res = persona(status, service, product_detail, interview_goal, target)
        end = time.time()
        print('시간: ', end - start)
        print(persona_res)

        print("========== virtual_interview ===============")
        start = time.time()
        interview_res = virtual_interview(status, service, product_detail, interview_goal, target, persona_res, question_res)
        end = time.time()
        print('시간: ', end - start)
        print(interview_res)

        print("========== summarize ===============")
        start = time.time()
        summarize_res = summarize(status, service, product_detail, interview_goal, target, interview_res)
        end = time.time()
        print('시간: ', end - start)
        print(summarize_res)
        
    else:
        question_res = validation_res['answer']
        print(question_res)

if __name__ == "__main__" :
    main()