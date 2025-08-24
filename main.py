from App import Moral_world  # your class in moral_world.py
import gradio as gr
import atexit

if __name__ == "__main__":
    # Initialize assistant
    guru = Moral_world()

    # Function to report total questions on exit
    def report_final_count():
        print(f"Final question count for this session: {guru.question_count}", flush=True)

    atexit.register(report_final_count)

    # Launch Gradio chat
    gr.ChatInterface(
        guru.chat, 
        type="messages", 
        title="Life Lessons",
        description=(
            "Hello! I am a Life Advisor here to help you navigate important life decisions "
            "using the timeless wisdom of the Bhagavad Gita. Only questions related to life "
            "guidance and spiritual wisdom will be addressed."
        )
    ).launch(share=True)
