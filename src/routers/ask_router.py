from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from src.services.types import LearningCardResponse
from src.services.ask_services import generate_response

router = APIRouter(prefix="/ask")


class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    question: str
    answer: LearningCardResponse


@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_200_OK)
async def ask(request: QuestionRequest):
    try:
        question = request.question.strip()

        if not question:
            raise HTTPException(status_code=400, detail="질문을 입력해야 합니다.")
        
        if len(question) > 100:
            raise HTTPException(status_code=400, detail="질문은 100자 이내로 입력해야 합니다.")


        answer = generate_response(question)

        if not answer or not isinstance(answer, dict):
            raise HTTPException(status_code=500, detail="응답 데이터 형식이 올바르지 않습니다.")
        
        response = {
            "question": question,
            "answer": answer
        }

        return response
    
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="알 수 없는 오류 발생")