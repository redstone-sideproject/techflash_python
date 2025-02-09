from fastapi import APIRouter,status
from pydantic import BaseModel
from src.services.ask_services import generate_response

router = APIRouter(prefix="/ask")


class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    question: str
    answer: dict


@router.get("/", response_model=QuestionResponse, status_code=status.HTTP_200_OK)
async def ask(request: QuestionRequest):

    response = {
        "question": request.question,
        "answer": generate_response(request.question)
    }

    return response