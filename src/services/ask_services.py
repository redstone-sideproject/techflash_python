from src.settings import Settings
from google import genai
from google.genai import types
import json

settings =Settings()

def generate_response(question: str) -> dict:
    result = run_vertex(question)
    return result

def run_vertex(question:str) -> dict:
    try:
        client = genai.Client(
            vertexai=True,
            project=settings.GCP_PROJECT,
            location=settings.GCP_LOCATION,
        )

        prompt = types.Part.from_text(text=f"""다음 주제에 대해 학습 카드와 퀴즈를 자동 생성해주세요. 각 카드에는 '문제'와 '답변'을 포함하고, 문제는 주제와 관련된 중요한 개념을 묻는 질문이어야 합니다. 퀴즈는 OX 문제, 객관식 문제, 주관식 문제를 포함해야 하며, 예시 답안도 제공해야합니다. 퀴즈는 주제에 대한 이해도를 테스트하는 질문이어야 합니다. 그리고 또한 주제에 대한 상세한 설명이 제일 처음에 주어져야 합니다.

    퀴즈는 OX 문제 10개, 객관식 문제 10개 주관식 문제 10개로 이루어져 있어야합니다. 주제가 기술질문이 아닐경우 예외처리를 해야합니다. 또한 질문한 기술에 따로 설명이 없다면 가능한 최신 버전을 토대로 설명을 해야합니다. 문제 또한 마찬가지입니다.
    예외처리 입력: 오늘 날씨가 어때?
    예외처리 결과 예시: 해당 응답은 제공하지 않습니다.

    주제: {question}

    1. 학습 카드 예시:
      - 문제: Virtual DOM이란 무엇인가요?
      - 답변: Virtual DOM은 실제 DOM의 추상화된 버전으로, 성능 최적화를 위해 사용됩니다.
      - 문제: Virtual DOM을 사용하는 이유는 무엇인가요?
      - 답변: Virtual DOM을 사용하면 불필요한 DOM 업데이트를 줄여 성능을 최적화할 수 있습니다.

    2. 퀴즈 예시:
      - OX 문제: Virtual DOM은 실제 DOM을 직접 업데이트한다. (O / X)
      - 객관식 문제: Virtual DOM의 주요 목적은 무엇인가요?
      - A) 실제 DOM을 효율적으로 업데이트하기 위해
       - B) 성능을 최적화하기 위해
       - C) 코드의 복잡성을 줄이기 위해
      - 주관식 문제: Virtual DOM이 상태 변화 후 어떻게 작동하는지 설명하세요.""")

        model = "gemini-2.0-flash-001"
        contents = [
            types.Content(
            role="user",
            parts=[
                prompt
            ]
            )
        ]
        generate_content_config = types.GenerateContentConfig(
            temperature = 1,
            top_p = 0.95,
            max_output_tokens = 8192,
            response_modalities = ["TEXT"],
            safety_settings = [types.SafetySetting(
            category="HARM_CATEGORY_HATE_SPEECH",
            threshold="OFF"
            ),types.SafetySetting(
            category="HARM_CATEGORY_DANGEROUS_CONTENT",
            threshold="OFF"
            ),types.SafetySetting(
            category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
            threshold="OFF"
            ),types.SafetySetting(
            category="HARM_CATEGORY_HARASSMENT",
            threshold="OFF"
            )],
            response_mime_type = "application/json",
            response_schema = {
                "type": "object",
                "properties": {
                    "response": {
                    "type": "object",
                    "properties": {
                        "topic_explanation": {
                        "type": "string"
                        },
                        "learning_cards": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                            "question": {
                                "type": "string"
                            },
                            "answer": {
                                "type": "string"
                            }
                            },
                            "required": ["question", "answer"]
                        }
                        },
                        "quiz": {
                        "type": "object",
                        "properties": {
                            "ox_questions": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                "question": {
                                    "type": "string"
                                },
                                "answer": {
                                    "type": "string",
                                    "enum": ["O", "X"]
                                }
                                },
                                "required": ["question", "answer"]
                            }
                            },
                            "multiple_choice_questions": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                "question": {
                                    "type": "string"
                                },
                                "options": {
                                    "type": "array",
                                    "items": {
                                    "type": "string"
                                    },
                                    "minItems": 2
                                },
                                "answer": {
                                    "type": "string"
                                }
                                },
                                "required": ["question", "options", "answer"]
                            }
                            },
                            "subjective_questions": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                "question": {
                                    "type": "string"
                                },
                                "answer_example": {
                                    "type": "string"
                                }
                                },
                                "required": ["question", "answer_example"]
                            }
                            }
                        },
                        "required": [
                            "ox_questions",
                            "multiple_choice_questions",
                            "subjective_questions"
                        ]
                        }
                    },
                    "required": [
                        "topic_explanation",
                        "learning_cards",
                        "quiz"
                    ]
                    }
                },
                "required": ["response"]
                },
        )

        response = client.models.generate_content(
            model = model,
            contents = contents,
            config = generate_content_config,
            )
        # response = {
        #     "response": {
        #         "learning_cards": [
        #             {
        #                 "answer": "Virtual DOM은 실제 DOM의 가벼운 추상화된 복사본입니다. UI를 업데이트할 때마다 실제 DOM을 직접 조작하는 대신, Virtual DOM에서 변경 사항을 먼저 적용하고, 변경된 부분만 실제 DOM에 반영하여 성능을 최적화합니다.",
        #                 "question": "Virtual DOM이란 무엇인가요?"
        #             },
        #             {
        #                 "answer": "Virtual DOM은 실제 DOM 조작 횟수를 줄여 불필요한 리렌더링을 방지하고, 효율적인 업데이트를 가능하게 합니다. 이를 통해 애플리케이션의 성능을 향상시키고 사용자 경험을 개선할 수 있습니다.",
        #                 "question": "Virtual DOM을 사용하는 이유는 무엇인가요?"
        #             },
        #             {
        #                 "answer": "Virtual DOM은 UI의 상태 변화를 감지하면, 먼저 Virtual DOM에 변경 사항을 적용합니다. 그 후, Virtual DOM은 이전 상태와 현재 상태를 비교하여 변경된 부분(Diff)을 찾아내고, 이 변경된 부분만 실제 DOM에 업데이트합니다.",
        #                 "question": "Virtual DOM은 상태 변화 후 어떻게 작동하나요?"
        #             },
        #             {
        #                 "answer": "React, Vue.js, Angular 등 많은 현대적인 JavaScript 프레임워크와 라이브러리가 Virtual DOM을 사용하여 UI를 관리하고 있습니다.",
        #                 "question": "Virtual DOM을 사용하는 주요 프레임워크 또는 라이브러리에는 어떤 것들이 있나요?"
        #             },
        #             {
        #                 "answer": "Virtual DOM은 메모리 내에서 작동하므로, 실제 DOM 조작보다 훨씬 빠릅니다. 또한, 변경 사항을 일괄적으로 처리하여 브라우저의 리렌더링 횟수를 줄여줍니다.",
        #                 "question": "Virtual DOM의 성능상의 이점은 무엇인가요?"
        #             }
        #         ],
        #         "quiz": {
        #             "multiple_choice_questions": [
        #                 {
        #                     "answer": "B) 실제 DOM 업데이트를 최소화하여 성능을 향상시킨다.",
        #                     "options": [
        #                         "A) 모든 DOM 변경 사항을 즉시 실제 DOM에 반영한다.",
        #                         "B) 실제 DOM 업데이트를 최소화하여 성능을 향상시킨다.",
        #                         "C) 브라우저의 렌더링 엔진을 직접 제어한다.",
        #                         "D) 서버 측 렌더링을 수행한다."
        #                     ],
        #                     "question": "Virtual DOM의 주요 목표는 무엇인가요?"
        #                 },
        #                 {
        #                     "answer": "A) Virtual DOM은 실제 DOM의 추상화된 표현이다.",
        #                     "options": [
        #                         "A) Virtual DOM은 실제 DOM의 추상화된 표현이다.",
        #                         "B) Virtual DOM은 실제 DOM과 완전히 동일하다.",
        #                         "C) Virtual DOM은 서버에서만 사용된다.",
        #                         "D) Virtual DOM은 사용자 인터랙션을 처리하지 않는다."
        #                     ],
        #                     "question": "Virtual DOM에 대한 올바른 설명은 무엇인가요?"
        #                 },
        #                 {
        #                     "answer": "C) 변경 사항을 감지하고 최소한의 업데이트만 실제 DOM에 적용한다.",
        #                     "options": [
        #                         "A) 모든 변경 사항을 즉시 실제 DOM에 적용한다.",
        #                         "B) 변경 사항을 무시하고 이전 상태를 유지한다.",
        #                         "C) 변경 사항을 감지하고 최소한의 업데이트만 실제 DOM에 적용한다.",
        #                         "D) 실제 DOM을 직접 조작하지 않는다."
        #                     ],
        #                     "question": "Virtual DOM은 상태 업데이트를 어떻게 처리하나요?"
        #                 },
        #                 {
        #                     "answer": "D) 애플리케이션의 성능을 최적화하고 사용자 경험을 향상시킨다.",
        #                     "options": [
        #                         "A) 코드의 복잡성을 증가시킨다.",
        #                         "B) 브라우저 호환성을 감소시킨다.",
        #                         "C) 초기 로딩 시간을 증가시킨다.",
        #                         "D) 애플리케이션의 성능을 최적화하고 사용자 경험을 향상시킨다."
        #                     ],
        #                     "question": "Virtual DOM을 사용함으로써 얻을 수 있는 주요 이점은 무엇인가요?"
        #                 },
        #                 {
        #                     "answer": "A) React",
        #                     "options": [
        #                         "A) React",
        #                         "B) jQuery",
        #                         "C) PHP",
        #                         "D) Ruby"
        #                     ],
        #                     "question": "다음 중 Virtual DOM을 사용하는 JavaScript 라이브러리는 무엇인가요?"
        #                 },
        #                 {
        #                     "answer": "B) Diffing",
        #                     "options": [
        #                         "A) Compiling",
        #                         "B) Diffing",
        #                         "C) Minifying",
        #                         "D) Polyfilling"
        #                     ],
        #                     "question": "Virtual DOM에서 변경 사항을 비교하는 과정을 무엇이라고 하나요?"
        #                 },
        #                 {
        #                     "answer": "C) 메모리",
        #                     "options": [
        #                         "A) 디스크",
        #                         "B) 네트워크",
        #                         "C) 메모리",
        #                         "D) 데이터베이스"
        #                     ],
        #                     "question": "Virtual DOM은 주로 어디에 저장되나요?"
        #                 },
        #                 {
        #                     "answer": "D) 실제 DOM 업데이트 횟수를 줄인다.",
        #                     "options": [
        #                         "A) 브라우저의 CSS 엔진을 변경한다.",
        #                         "B) JavaScript 코드를 난독화한다.",
        #                         "C) 서버 측 렌더링을 수행한다.",
        #                         "D) 실제 DOM 업데이트 횟수를 줄인다."
        #                     ],
        #                     "question": "Virtual DOM은 어떻게 성능을 향상시키나요?"
        #                 },
        #                 {
        #                     "answer": "A) UI의 상태를 효율적으로 관리한다.",
        #                     "options": [
        #                         "A) UI의 상태를 효율적으로 관리한다.",
        #                         "B) 데이터베이스 쿼리를 최적화한다.",
        #                         "C) 서버와의 통신을 간소화한다.",
        #                         "D) CSS 스타일을 자동으로 생성한다."
        #                     ],
        #                     "question": "Virtual DOM의 주된 역할은 무엇인가요?"
        #                 },
        #                 {
        #                     "answer": "B) DOM 조작을 추상화한다.",
        #                     "options": [
        #                         "A) 브라우저의 버그를 수정한다.",
        #                         "B) DOM 조작을 추상화한다.",
        #                         "C) 서버의 부하를 줄인다.",
        #                         "D) 네트워크 속도를 향상시킨다."
        #                     ],
        #                     "question": "Virtual DOM은 주로 어떤 문제를 해결하나요?"
        #                 }
        #             ],
        #             "ox_questions": [
        #                 {
        #                     "answer": "X",
        #                     "question": "Virtual DOM은 실제 DOM을 직접 업데이트한다. (O / X)"
        #                 },
        #                 {
        #                     "answer": "O",
        #                     "question": "Virtual DOM은 실제 DOM의 추상화된 버전이다. (O / X)"
        #                 },
        #                 {
        #                     "answer": "X",
        #                     "question": "Virtual DOM은 브라우저에 직접적으로 표시된다. (O / X)"
        #                 },
        #                 {
        #                     "answer": "O",
        #                     "question": "Virtual DOM은 애플리케이션의 성능을 향상시키는 데 도움이 된다. (O / X)"
        #                 },
        #                 {
        #                     "answer": "X",
        #                     "question": "Virtual DOM은 서버 측 렌더링에만 사용된다. (O / X)"
        #                 },
        #                 {
        #                     "answer": "O",
        #                     "question": "Virtual DOM은 상태 변화를 감지하고 필요한 부분만 업데이트한다. (O / X)"
        #                 },
        #                 {
        #                     "answer": "X",
        #                     "question": "Virtual DOM은 모든 JavaScript 프레임워크에서 기본적으로 사용된다. (O / X)"
        #                 },
        #                 {
        #                     "answer": "O",
        #                     "question": "Virtual DOM은 메모리 내에서 작동하여 실제 DOM 조작 횟수를 줄인다. (O / X)"
        #                 },
        #                 {
        #                     "answer": "X",
        #                     "question": "Virtual DOM은 코드의 복잡성을 증가시킨다. (O / X)"
        #                 },
        #                 {
        #                     "answer": "O",
        #                     "question": "Virtual DOM은 사용자 인터페이스의 반응성을 개선할 수 있다. (O / X)"
        #                 }
        #             ],
        #             "subjective_questions": [
        #                 {
        #                     "answer_example": "Virtual DOM은 UI 컴포넌트의 변경 사항을 추적하고, 실제 DOM에 필요한 최소한의 업데이트만 적용하여 성능을 최적화합니다. 변경 사항이 발생하면 Virtual DOM은 이전 상태와 현재 상태를 비교하여 변경된 부분을 식별하고, 해당 부분만 실제 DOM에 반영합니다.",
        #                     "question": "Virtual DOM이 상태 변화 후 어떻게 작동하는지 설명하세요."
        #                 },
        #                 {
        #                     "answer_example": "Virtual DOM을 사용하면 전체 페이지를 다시 렌더링하는 대신 변경된 부분만 업데이트할 수 있으므로 애플리케이션의 성능이 향상됩니다. 또한, DOM 조작 횟수를 줄여 브라우저의 부하를 줄이고 사용자 경험을 개선할 수 있습니다.",
        #                     "question": "Virtual DOM을 사용함으로써 얻을 수 있는 성능상의 이점을 설명하세요."
        #                 },
        #                 {
        #                     "answer_example": "React는 Virtual DOM을 사용하여 컴포넌트의 상태 변화를 관리하고 UI를 업데이트합니다. Vue.js 또한 Virtual DOM을 사용하여 효율적인 DOM 업데이트를 수행합니다. 이 외에도 Angular와 같은 프레임워크에서도 Virtual DOM의 개념을 활용하여 성능을 최적화합니다.",
        #                     "question": "Virtual DOM을 사용하는 주요 프레임워크 또는 라이브러리를 예시로 들어 설명하세요."
        #                 },
        #                 {
        #                     "answer_example": "Virtual DOM은 실제 DOM의 가벼운 복사본으로, 메모리 내에서 작동합니다. 반면, 실제 DOM은 브라우저에 표시되는 실제 UI 요소의 트리 구조입니다. Virtual DOM은 실제 DOM을 직접 조작하는 대신 변경 사항을 먼저 적용하고, 필요한 부분만 실제 DOM에 업데이트합니다.",
        #                     "question": "Virtual DOM과 실제 DOM의 차이점을 설명하세요."
        #                 },
        #                 {
        #                     "answer_example": "Virtual DOM은 UI를 효율적으로 업데이트하고 관리하기 위한 기술입니다. UI 개발에서 DOM 조작은 비용이 많이 드는 작업이므로, Virtual DOM은 이를 최소화하여 애플리케이션의 성능을 향상시킵니다.",
        #                     "question": "Virtual DOM이 UI 개발에서 중요한 이유는 무엇인가요?"
        #                 },
        #                 {
        #                     "answer_example": "Virtual DOM은 UI의 현재 상태를 나타내는 가상적인 트리 구조입니다. 이 트리는 JavaScript 객체로 표현되며, UI의 변경 사항을 추적하고 실제 DOM 업데이트를 최적화하는 데 사용됩니다.",
        #                     "question": "Virtual DOM의 구조에 대해 설명하세요."
        #                 },
        #                 {
        #                     "answer_example": "Virtual DOM은 'Diffing'이라는 과정을 통해 변경 사항을 감지합니다. Diffing 알고리즘은 Virtual DOM의 이전 상태와 현재 상태를 비교하여 변경된 부분을 찾아내고, 해당 부분만 실제 DOM에 업데이트합니다.",
        #                     "question": "Virtual DOM에서 변경 사항을 감지하는 방법(Diffing)에 대해 설명하세요."
        #                 },
        #                 {
        #                     "answer_example": "Virtual DOM을 사용하면 개발자는 UI를 더 쉽게 관리하고 디버깅할 수 있습니다. 또한, UI 컴포넌트의 재사용성을 높이고 애플리케이션의 유지보수성을 향상시킬 수 있습니다.",
        #                     "question": "Virtual DOM이 개발자에게 제공하는 이점을 설명하세요."
        #                 },
        #                 {
        #                     "answer_example": "Virtual DOM은 초기 렌더링 성능을 향상시키고, 리렌더링 비용을 줄이며, UI 업데이트의 일관성을 유지하는 데 도움이 됩니다. 또한, 사용자 인터랙션에 대한 응답성을 높여 사용자 경험을 개선할 수 있습니다.",
        #                     "question": "Virtual DOM이 사용자 경험에 미치는 영향을 설명하세요."
        #                 },
        #                 {
        #                     "answer_example": "Virtual DOM을 사용하면 코드의 복잡성을 줄이고 UI 개발 과정을 간소화할 수 있습니다. 또한, 컴포넌트 기반 아키텍처를 지원하여 UI를 모듈화하고 재사용성을 높일 수 있습니다.",
        #                     "question": "Virtual DOM이 코드 유지보수에 어떤 영향을 미치나요?"
        #                 }
        #             ]
        #         },
        #         "topic_explanation": "Virtual DOM은 실제 DOM(Document Object Model)의 가벼운 추상화된 복사본입니다. 웹 애플리케이션에서 UI를 업데이트할 때마다 실제 DOM을 직접 조작하는 대신, Virtual DOM에서 변경 사항을 먼저 적용하고, 변경된 부분만 실제 DOM에 반영하여 성능을 최적화합니다. 이를 통해 불필요한 리렌더링을 줄이고, 애플리케이션의 반응성을 향상시킬 수 있습니다. React, Vue.js 등 많은 현대적인 JavaScript 프레임워크와 라이브러리가 Virtual DOM을 사용하여 UI를 관리합니다."
        #     }
        # }
        # return response.get("response")
        return json.loads(response.text).get("response")
    
    except json.JSONDecodeError:
        raise ValueError("API 응답이 JSON 형식이 아닙니다.")
    
    except Exception as e:
        raise RuntimeError(str(e))