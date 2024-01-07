import os
import openai
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from chromadb.config import Settings
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

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



def get_vectorstore(text_chunks, collection_name):
    # Embedding에 사용할 Embedding 모델 생성
    # In-house 개발을 위해서는 모델을 직접 내려받아서 사용해야함
    # embeddings = SentenceTransformerEmbeddings(model_name="hkunlp/instructor-large")
    embeddings = OpenAIEmbeddings()

    # Vector 스토어 생성. 편의성을 위하여 ChromaDB 사용
    # local 에서 Docker 사용하여 Chroma DB 업로드 할 예정
    # Docker에서 띄워놓지 않으면 데이터가 in-memory에서 휘발됨
    client_settings = Settings(
            # chroma_api_impl="rest",
            chroma_server_host="localhost",
            chroma_server_http_port="8000"
        )
    # metadata가 별도로 있는 document 집합이 아니므로, from_texts로 바로 Chroma에 embedding 저장
    # FYI https://github.com/langchain-ai/langchain/issues/10622
    vectorstore = Chroma.from_texts(
        # documents=text_chunks
        texts=text_chunks
        ,embedding=embeddings
        ,client_settings = client_settings
        ,collection_name = collection_name
    )
    return vectorstore


def main():

    # Embedding 할 path 선택
    current_path = os.getcwd()
    file_name = 'test.pdf'
    file_path = os.path.join(current_path, file_name)

    # Embedding 할 문서에서 Text 추출
    raw_text = get_pdf_text(file_path)

    # 문서 Embedding을 위한 Chunk 준비
    text_chunks = get_text_chunks(raw_text)

    # Embedding 시작하기
    collection_name = "my_document"
    vectorstore = get_vectorstore(text_chunks, collection_name)

    # 사용할 LLM 모델 생성, 편의를 위하여 Open AI API 사용
    llm = ChatOpenAI()

    # RAG 구현을 위하여, chat history를 저장할 BufferMemory 생성
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    # RAG를 위한 Retrieval Chain 생성 및 chat_history 바탕으로 대화 가능하도록 기능생성
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=memory,
        retriever=vectorstore.as_retriever()
    )

    # User Input을 받아서 대화를 생성
    while True:
        
        user_input = input("User: ")
        # conversation Chain을 생성해서 응답 생성
        response = conversation_chain({"User Question: ": user_input})
        print("Bot Answer: " + response.answer)

        # 대화 이력 업데이트
        memory.load_memory_variables({})
        
if __name__ == '__main__':
    main()

