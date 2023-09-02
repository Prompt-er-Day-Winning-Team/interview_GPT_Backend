from os import stat
from typing import Optional, List
from fastapi import APIRouter, Depends

# from app.core.helper import check_jwt
from app.repository.interview_repo import InterviewRepository
from app.domain.request_domain import InterviewCreateInfo


interview_router = APIRouter(
    prefix="/v1/user/{user_id}/interview",
    tags=["interview"],
    # dependencies=[Depends(check_jwt)],
    responses={ 404: {"description": "Not Found!!!"}}
)

# 인터뷰 기본정보 입력
@interview_router.post(path="/")
async def create_interview_default(user_id: int, interview_info: InterviewCreateInfo):
    interview_repo = InterviewRepository()
    interview_question_list = interview_repo.create_interview(user_id=user_id, interview_info=interview_info)
    return interview_question_list



# ## 단일 진료기록 이미지 전체 조회
# @medical_record_router.get(path="/{medical_record_id}/files", response_model=List[ReadFileAll])
# async def read_medical_record_file_all(member_id: int, medical_record_id: int):
#     file_repo = FileRepository()
#     medical_record_files = file_repo.read_medical_record_file_all(member_id=member_id, medical_record_id=medical_record_id)
#     # for idx in range(len(medical_record_files)):
#     #   ocr_result = start_ocr(medical_record_files[idx].url)
#     #   medical_record_files[idx].ocr_result = ocr_result
#     return [ReadFileAll.from_orm(medical_record_file) for medical_record_file in medical_record_files]

# ## 단일 진료기록 조회 (진료기록 - 제목, 날짜, 의사명 / 진료기록 중분류 - 중분류 원본, 상세내용 원본 => 진료기록 중분류 번역본)
# @medical_record_router.get(path="/{medical_record_id}", response_model=ReadDiagnosisRecord)
# async def read_medical_record(member_id: int, medical_record_id: int, status: str):
#     if status not in ["REGISTRATION", "TRANSLATION", "CHECK", "REPORT"]:
#         return "Wrong status"
#     diagnosis_repo = DiagnosisRepository()
#     diagnosis_record = diagnosis_repo.read_medical_record(member_id=member_id, medical_record_id=medical_record_id, status=status)
#     return ReadDiagnosisRecord.from_orm(diagnosis_record)

# # 등록 REGISTRATION
# ## 진료기록 OCR 결과 조회
# @medical_record_router.get(path="/{medical_record_id}/files/{file_id}/ocr", response_model=ReadFileOcr)
# async def read_medical_record_file_ocr(member_id: int, medical_record_id: int, file_id: int):
#     file_repo = FileRepository()
#     medical_record_file = file_repo.read_medical_record_file(member_id=member_id, medical_record_id=medical_record_id, file_id=file_id)
#     ocr_result = start_ocr(medical_record_file.url)
#     result = {
#       "id" : medical_record_file.id,
#       "ocr_result": ocr_result
#     }
#     return result

# ## 진료기록 등록 (진료기록 row 수정 - 제목, 날짜, 의사명, 기록 상태값 / 진료기록 중분류 row 추가 - 중분류 원본, 상세내용 원본)
# @medical_record_router.put(path="/{medical_record_id}/registrations", response_model=ReadDiagnosisRecord)
# async def update_medical_record_registration(member_id: int, medical_record_id: int, medical_record_info: MedicalRecordUpdateRegistrationInfo):
#     diagnosis_repo = DiagnosisRepository()
#     diagnosis_record = diagnosis_repo.update_medical_record_registration(member_id=member_id, medical_record_id=medical_record_id, medical_record_info=medical_record_info.dict())
#     return ReadDiagnosisRecord.from_orm(diagnosis_record)

# # New API
# ## 진료기록 등록 (진료기록 row 수정 - 제목, 날짜, 의사명, 기록 상태값 / 진료기록 중분류 row 수정(중분류, 중분류 원본, 상세내용, 상세내용 원본))
# # @medical_record_router.put(path="/{medical_record_id}/translations", response_model=ReadDiagnosisRecord)
# # async def update_medical_record_registration(member_id: int, medical_record_id: int, medical_record_info: MedicalRecordUpdateTranslationInfo):
# #     diagnosis_repo = DiagnosisRepository()
# #     diagnosis_record = diagnosis_repo.update_medical_record_registration(member_id=member_id, medical_record_id=medical_record_id, medical_record_info=medical_record_info.dict())
# #     return ReadDiagnosisRecord.from_orm(diagnosis_record)

# # 번역 TRANSLATION
# ## 단순 단어 치환 결과 조회

# ## 진료기록 등록 (진료기록 row 수정(제목, 날짜, 의사명, 기록 상태값), 진료기록 중분류 row 수정(중분류, 중분류 원본, 상세내용, 상세내용 원본))
# @medical_record_router.put(path="/{medical_record_id}/translations")
# async def update_medical_record_translation(member_id: int, medical_record_id: int, medical_record_info: MedicalRecordUpdateTranslationInfo):
#     diagnosis_repo = DiagnosisRepository()
#     result_status = diagnosis_repo.update_medical_record_translation_or_check(member_id=member_id, medical_record_id=medical_record_id, medical_record_info=medical_record_info.dict())
#     return result_status

# # 검수 CHECK
# ## 진료기록 등록 (진료기록 row 수정(제목, 날짜, 의사명, 기록 상태값), 진료기록 중분류 row 수정(중분류, 중분류 원본, 상세내용, 상세내용 원본))
# @medical_record_router.put(path="/{medical_record_id}/checks")
# async def update_medical_record_check(member_id: int, medical_record_id: int, medical_record_info: MedicalRecordUpdateTranslationInfo):
#     diagnosis_repo = DiagnosisRepository()
#     result_status = diagnosis_repo.update_medical_record_translation_or_check(member_id=member_id, medical_record_id=medical_record_id, medical_record_info=medical_record_info.dict())
#     return result_status

# ## 진료기록 상태 수정
# @medical_record_router.put(path="/status")
# async def update_medical_record_status(member_id: int, to_status: str, medical_record_info: MedicalRecordUpdateStatus):
#     diagnosis_repo = DiagnosisRepository()
#     result_status = diagnosis_repo.update_medical_record_status(member_id=member_id, to_record_status=to_status, medical_record_info=medical_record_info.dict())
#     return result_status