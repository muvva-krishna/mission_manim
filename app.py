import streamlit as st
import os
import time
from codegen import generate_manim_code, clean_code, fix_code
from manim_runner import run_manim

def wait_for_file(file_path, timeout=10):
    """Waits until the video file is fully written."""
    for _ in range(timeout * 10):  # check every 0.1s
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            return True
        time.sleep(0.1)
    return False

st.set_page_config(page_title="Manim Math Assistant", page_icon="🎓")
st.title("🎓 Manim Math Assistant")

prompt = st.text_input("Enter your math concept:")

if st.button("Generate Animation") and prompt.strip():
    with st.spinner("🔧 Generating Manim code..."):
        raw_code = generate_manim_code(prompt)
        code = clean_code(raw_code)
        fixed_code = fix_code(code)

    st.subheader("📜 Generated Code")
    st.code(fixed_code, language="python")

    with st.spinner("🎞️ Rendering animation..."):
        video_path = run_manim(fixed_code)

    if video_path and wait_for_file(video_path):
        st.success("✅ Animation generated!")
        st.video(video_path)
    else:
        st.error("❌ Failed to render animation or video file not found.")
