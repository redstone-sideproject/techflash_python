from typing import List
from pydantic import BaseModel

class LearningCard(BaseModel):
    question: str
    answer: str

# 객관식 문제 모델
class MultipleChoiceQuestion(BaseModel):
    question: str
    options: List[str]
    answer: str

# OX 문제 모델
class OXQuestion(BaseModel):
    question: str
    answer: str  # "O" 또는 "X"

# 주관식 문제 모델
class SubjectiveQuestion(BaseModel):
    question: str
    answer_example: str

# 퀴즈 응답 모델 (객관식 + OX + 주관식)
class QuizResponse(BaseModel):
    multiple_choice_questions: List[MultipleChoiceQuestion]
    ox_questions: List[OXQuestion]
    subjective_questions: List[SubjectiveQuestion]

# 최종 응답 모델
class LearningCardResponse(BaseModel):
    learning_cards: List[LearningCard]
    quiz: QuizResponse
    topic_explanation: str

    class Config:
        schema_extra = {
            "example": {
                "learning_cards": [
                    {
                        "question": "Virtual DOM이란 무엇인가요?",
                        "answer": "Virtual DOM은 실제 DOM의 가벼운 추상화된 복사본입니다. UI를 업데이트할 때마다 실제 DOM을 직접 조작하는 대신, Virtual DOM에서 변경 사항을 먼저 적용하고, 변경된 부분만 실제 DOM에 반영하여 성능을 최적화합니다."
                    },
                    {
                        "question": "Virtual DOM을 사용하는 이유는 무엇인가요?",
                        "answer": "Virtual DOM은 실제 DOM 조작 횟수를 줄여 불필요한 리렌더링을 방지하고, 효율적인 업데이트를 가능하게 합니다. 이를 통해 애플리케이션의 성능을 향상시키고 사용자 경험을 개선할 수 있습니다."
                    }
                ],
                "quiz": {
                    "multiple_choice_questions": [
                        {
                            "question": "Virtual DOM의 주요 목표는 무엇인가요?",
                            "options": [
                                "A) 모든 DOM 변경 사항을 즉시 실제 DOM에 반영한다.",
                                "B) 실제 DOM 업데이트를 최소화하여 성능을 향상시킨다.",
                                "C) 브라우저의 렌더링 엔진을 직접 제어한다.",
                                "D) 서버 측 렌더링을 수행한다."
                            ],
                            "answer": "B) 실제 DOM 업데이트를 최소화하여 성능을 향상시킨다."
                        }
                    ],
                    "ox_questions": [
                        {
                            "question": "Virtual DOM은 실제 DOM을 직접 업데이트한다. (O / X)",
                            "answer": "X"
                        }
                    ],
                    "subjective_questions": [
                        {
                            "question": "Virtual DOM이 상태 변화 후 어떻게 작동하는지 설명하세요.",
                            "answer_example": "Virtual DOM은 UI 컴포넌트의 변경 사항을 추적하고, 실제 DOM에 필요한 최소한의 업데이트만 적용하여 성능을 최적화합니다. 변경 사항이 발생하면 Virtual DOM은 이전 상태와 현재 상태를 비교하여 변경된 부분을 식별하고, 해당 부분만 실제 DOM에 반영합니다."
                        }
                    ]
                },
                "topic_explanation": "Virtual DOM은 실제 DOM(Document Object Model)의 가벼운 추상화된 복사본입니다. 웹 애플리케이션에서 UI를 업데이트할 때마다 실제 DOM을 직접 조작하는 대신, Virtual DOM에서 변경 사항을 먼저 적용하고, 변경된 부분만 실제 DOM에 반영하여 성능을 최적화합니다. 이를 통해 불필요한 리렌더링을 줄이고, 애플리케이션의 반응성을 향상시킬 수 있습니다. React, Vue.js 등 많은 현대적인 JavaScript 프레임워크와 라이브러리가 Virtual DOM을 사용하여 UI를 관리합니다."
            }
        }