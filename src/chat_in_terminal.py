import time
from utils.basic_chatbot_v1 import Chatbot
from utils.chatbot_agentic_v2 import Chatbot as Chatbot_v2
from utils.chatbot_agentic_v3 import Chatbot as Chatbot_v3

# If you'd like to chat with a different chatbot, modify the code manually.

if __name__ == "__main__":
    chatbot = Chatbot_v3()
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
