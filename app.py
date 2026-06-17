import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="NEON M4 SURVIVAL 3D", layout="centered")

st.title("💥 M4 NEON SURVIVAL 3D")
st.caption("WASD로 이동하고 마우스로 화면을 조준해 몰려오는 NPC를 사격하세요.")

# 에러 가능성을 0%로 낮추기 위해 예외 처리를 극대화한 버전
fps_m4_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {
            margin: 0; overflow: hidden; background-color: #020617;
            font-family: sans-serif; user-select: none;
        }
        #game-container {
            position: relative; width: 100%; height: 530px;
            border: 4px solid #ff007f; border-radius: 15px; overflow: hidden;
            cursor: crosshair; background-color: #020617;
        }
        #hud {
            position: absolute; top: 20px; left: 20px; color: #fff;
            font-size: 20px; font-weight: bold; z-index: 10; pointer-events: none;
        }
        #hp-container {
            position: absolute; top: 20px; right: 20px; width: 200px; height: 20px;
            background: rgba(
