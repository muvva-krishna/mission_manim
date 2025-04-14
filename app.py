import streamlit as st
import os
import time
from codegen import AnimationGenerator  # Import the class instead of individual functions
from manim_runner import run_manim

# Groq API key should be set in the environment variables
animation_generator = AnimationGenerator(api_key=os.environ.get("GROQ_API_KEY"))

def wait_for_file(file_path, timeout=10):
    """Waits until the video file is fully written."""
    for _ in range(timeout * 10):  # check every 0.1s
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            return True
        time.sleep(0.1)
    return False

st.set_page_config(page_title="Manim Math Assistant", page_icon="🎓")
st.title("🎓 Manim Math Assistant")

# Take input from user
prompt = st.text_input("Enter your math concept:")

if st.button("Generate Animation") and prompt.strip():
    with st.spinner("🧠 Thinking like an animator..."):
        animation_plan, final_code = animation_generator.generate_final_manim_code(prompt)

    # Display the animation plan
    st.subheader("🪄 Animation Plan")
    st.markdown(animation_plan)

    # Display the generated Manim code
    st.subheader("📜 Generated Code")
    st.code(final_code, language="python")

    with st.spinner("🎞️ Rendering animation..."):
        video_path = run_manim(final_code)

    if video_path and wait_for_file(video_path):
        st.success("✅ Animation generated!")
        st.video(video_path)
    else:
        st.error("❌ Failed to render animation or video file not found.")
