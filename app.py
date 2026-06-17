import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="NEON M4 SURVIVAL 3D", layout="centered")
st.title("💥 M4 NEON SURVIVAL 3D")

# 소스코드 충돌을 완전 방지하기 위해 정적 페이지로 분리된 안정적인 게임 엔진을 로드합니다.
components.iframe("https://util-apps.github.io/fps-game/", height=550)
