import sys
sys.path.append('/Users/eunji/Documents/prompter_day/interview_GPT_Backend')
from app.prompt.request_validation import request_validation
from app.prompt.question import question
from app.prompt.persona import persona
from app.prompt.summarize import summarize
from app.prompt.virtual_interview import virtual_interview
from app.prompt.total_statistics import total_statistics
from omegaconf import OmegaConf
import pandas as pd
import json

def main():
    test_data = OmegaConf.load("app/test/test_data.yaml")
    service = test_data.haruzogak.product_name
    product_detail = test_data.haruzogak.product_detail
    interview_goal = test_data.haruzogak.interview_goal
    target = test_data.haruzogak.target_user
    validation_res = request_validation(service, product_detail, interview_goal,target)
    validation_res = json.loads(validation_res)
    print(validation_res)
    
    if validation_res['type'] == '문제없음' :
        question_res = question(service, product_detail, interview_goal,target)
        print(question_res)
        persona_res = persona(service, product_detail, interview_goal, target)
        print(persona_res)
        interview_res = virtual_interview(service, product_detail, interview_goal, target, persona_res, question_res)
        print(interview_res)
        summarize_res = summarize(service, product_detail, interview_goal, target, interview_res)
        print(summarize_res)
        
    else:
        question_res = validation_res['answer']
        print(question_res)

if __name__ == "__main__" :
    main()