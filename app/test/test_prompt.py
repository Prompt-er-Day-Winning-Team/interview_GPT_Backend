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
    test_data = OmegaConf.load("app/test/test_data.yaml")
    service = test_data.carrot.product_name
    product_detail = test_data.carrot.product_detail
    interview_goal = test_data.carrot.interview_goal
    target = test_data.carrot.target_user
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
        question_res = question(service, product_detail, interview_goal,target)
        end = time.time()
        print('시간: ', end - start)
        print(question_res)

        print("========== persona ===============")
        start = time.time()
        persona_res = persona(service, product_detail, interview_goal, target)
        end = time.time()
        print('시간: ', end - start)
        print(persona_res)

        print("========== virtual_interview ===============")
        start = time.time()
        interview_res = virtual_interview(service, product_detail, interview_goal, target, persona_res, question_res)
        end = time.time()
        print('시간: ', end - start)
        print(interview_res)

        print("========== summarize ===============")
        start = time.time()
        summarize_res = summarize(service, product_detail, interview_goal, target, interview_res)
        end = time.time()
        print('시간: ', end - start)
        print(summarize_res)
        
    else:
        question_res = validation_res['answer']
        print(question_res)

if __name__ == "__main__" :
    main()