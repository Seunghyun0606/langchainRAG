import os
import openai
from dotenv import load_dotenv
from PyPDF2 import PdfReader

# env에서 Open API 키 가져오기
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY 


def get_pdf_text(file_path):
    # pypdf 를 통해서 pdf 문서 읽기
    doc_reader = PdfReader(file_path)
    raw_text = ''
    for i, page in enumerate(doc_reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text
    return raw_text

def main():

    # Embedding 할 path 선택
    current_path = os.getcwd()
    file_name = 'test.pdf'
    file_path = os.path.join(current_path, file_name)

    # Embedding 할 문서에서 Text 추출
    raw_text = get_pdf_text(file_path)

    # User Input을 받아서 대화를 생성
    while True:
        
        user_input = input("User: ")
        # conversation Chain을 생성해서 응답 생성
        response = conversation_chain({"User Question: ": user_input})
        print("Bot Answer: " + response.answer)

if __name__ == '__main__':
    main()

