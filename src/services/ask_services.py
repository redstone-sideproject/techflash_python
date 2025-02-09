from src.settings import Settings

settings =Settings()

def generate_response(question: str) -> dict:
    print(settings.GCP_LOCATION)
    dummy_response ={
        "question": question,
        "answer": "Virtual DOM은 실제 DOM을 변경하기 전에 가상으로 상태를 관리하는 개념입니다.",
    }
    return dummy_response