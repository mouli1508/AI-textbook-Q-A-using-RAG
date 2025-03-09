import time
from utils.chatbot import Chatbot
from utils.chatbot_agentic_v1 import Chatbot as Chatbot_v1
from utils.chatbot_agentic_v2 import Chatbot as Chatbot_v2


if __name__ == "__main__":
    chatbot = Chatbot_v2()
    print("Chatbot initialized. Type 'exit' to end the conversation.")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # Get response from the chatbot
        print("\nThinking...")
        start_time = time.time()
        response = chatbot.chat(user_input)
        end_time = time.time()

        print(f"\nAssistant ({round(end_time - start_time, 2)}s): {response}")
