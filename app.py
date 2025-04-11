import streamlit as st
from codegen import generate_manim_code, clean_code , fix_code
from manim_runner import run_manim

st.title("🎓 Manim Math Assistant")
prompt = st.text_input("Enter your math concept:")

if st.button("Generate Animation") and prompt.strip():
    with st.spinner("Generating Manim code..."):
        raw_code = generate_manim_code(prompt)
        code = clean_code(raw_code)
        fixed_code = fix_code(code)
        
    st.code(code, language="python")

    with st.spinner("Rendering animation..."):
        video_path = run_manim(code)

    if video_path:
        st.success("Animation generated!")
        st.video(video_path)
    else:
        st.error("Failed to render animation. Check your Manim code.")
