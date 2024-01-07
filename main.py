


def main():


    # User Input을 받아서 대화를 생성
    while True:
        
        user_input = input("User: ")
        # conversation Chain을 생성해서 응답 생성
        response = conversation_chain({"User Question: ": user_input})
        print("Bot Answer: " + response.answer)

if __name__ == '__main__':
    main()

