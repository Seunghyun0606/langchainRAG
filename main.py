import os
import openai
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter

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


def get_text_chunks(raw_text):
    # langChain 에서 지원하는 spliter 사용하여 chunk 나누기
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=512,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks


def main():

    # Embedding 할 path 선택
    current_path = os.getcwd()
    file_name = 'test.pdf'
    file_path = os.path.join(current_path, file_name)

    # Embedding 할 문서에서 Text 추출
    raw_text = get_pdf_text(file_path)

    # 문서 Embedding을 위한 Chunk 준비
    text_chunks = get_text_chunks(raw_text)


    # User Input을 받아서 대화를 생성
    while True:
        
        user_input = input("User: ")
        # conversation Chain을 생성해서 응답 생성
        response = conversation_chain({"User Question: ": user_input})
        print("Bot Answer: " + response.answer)

if __name__ == '__main__':
    main()

