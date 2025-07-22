import time
import gradio as gr

from utils.basic_chatbot_v1 import Chatbot
from utils.chatbot_agentic_v2 import Chatbot as Chatbot_v2
from utils.chatbot_agentic_v3 import Chatbot as Chatbot_v3

# Initialize chatbot instances
chatbots = {
    "Basic-Chatbot": Chatbot(),
    "Chatbot-Agentic-v2": Chatbot_v2(),
    "Chatbot-Agentic-v3": Chatbot_v3(),
}

def respond(selected_bot, history, user_input):
    if not user_input.strip():
        return history, ""
    chatbot = chatbots[selected_bot]
    start_time = time.time()
    response = chatbot.chat(user_input)
    end_time = time.time()
    history.append((user_input, f"{response} ({round(end_time - start_time, 2)}s)"))
    return history, ""

custom_css = """
:root, [data-theme] {
    --body-text-color: #1f2937 !important;      /* force dark text */
    --text-color: #1f2937 !important;
}

#chatbot {
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    background: #0f1321;
}

/* Bot bubble */
#chatbot .message.bot, 
#chatbot .message.bot * {
    background:#ffffff !important;
    color:#1f2937 !important;
    opacity:1 !important;
    filter:none !important;
}

/* User bubble */
#chatbot .message.user, 
#chatbot .message.user * {
    background:#6366f1 !important;
    color:#ffffff !important;
    border-radius:14px !important;
    opacity:1 !important;
}
"""

with gr.Blocks(theme=gr.themes.Soft(primary_hue="indigo", secondary_hue="pink"), css=custom_css) as demo:
    with gr.Tabs():
        with gr.TabItem("Chatbot with Agentic Memory"):
            gr.Markdown("<div id='app-title'>Agentic Chatbot</div><div id='subtitle'>Choose a model and start chatting</div>")
            with gr.Row():
                chatbot = gr.Chatbot(
                    [],
                    elem_id="chatbot",
                    height=480,
                    avatar_images=("images/AI_RT.png", "images/openai.png"),
                    show_copy_button=True,
                )
            with gr.Row():
                input_txt = gr.Textbox(
                    lines=2,
                    placeholder="Type your message and press Enter...",
                    label="Your Message",
                    scale=7,
                )
            with gr.Row():
                text_submit_btn = gr.Button("Send ✈️", variant="primary", scale=2)
                clear_button = gr.ClearButton([input_txt, chatbot], value="Clear")
                selected_bot = gr.Dropdown(
                    choices=["Basic-Chatbot", "Chatbot-Agentic-v2", "Chatbot-Agentic-v3"],
                    value="Chatbot-Agentic-v3",
                    label="Chatbot Version",
                )

            # Submission handlers
            input_txt.submit(fn=respond, inputs=[selected_bot, chatbot, input_txt], outputs=[chatbot, input_txt])
            text_submit_btn.click(fn=respond, inputs=[selected_bot, chatbot, input_txt], outputs=[chatbot, input_txt])

if __name__ == "__main__":
    demo.launch()
