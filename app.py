import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="NEON M4 SURVIVAL 3D", layout="centered")

st.title("💥 M4 NEON SURVIVAL 3D")
st.caption("구문 에러 완전 해결판. WASD 이동 및 마우스 조준 사격으로 NPC를 저지하세요.")

# 파이썬 주석 기호(#)를 단 하나도 사용하지 않은 안전한 HTML/JS 텍스트
fps_m4_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {
            margin: 0; overflow: hidden; background-color: rgb(2, 6, 23);
            font-family: sans-serif; user-select: none;
        }
        #game-container {
            position: relative; width: 100%; height: 530px;
            border: 4px solid rgb(255, 0, 127); border-radius: 15px; overflow: hidden;
            cursor: crosshair; background-color: rgb(2, 6, 23);
        }
        #hud {
            position: absolute; top: 20px; left: 20px; color: rgb(255, 255, 255);
            font-size: 20px; font-weight: bold; z-index: 10; pointer-events: none;
        }
        #hp-container {
            position: absolute; top: 20px; right: 20px; width: 200px; height: 20px;
            background: rgba(255, 255, 255, 0.2); border: 2px solid rgb(255, 255, 255); border-radius: 5px; z-index: 10;
        }
        #hp-bar { width: 100%; height: 100%; background: rgb(239, 68, 68); }
        #damage-flash {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(239, 68, 68, 0); pointer-events: none; z-index: 5;
        }
        #gameover-screen {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(2, 6, 23, 0.95); display: none;
            flex-direction: column; justify-content: center; align-items: center; color: rgb(255, 255, 255); z-index: 20;
        }
        .btn-restart {
            background: rgb(0, 255, 255); border: none; color: rgb(0, 0, 0); padding: 10px 25px;
            font-size: 16px; font-weight: bold; border-radius: 5px; cursor: pointer;
        }
    </style>
    <script src="https://cdnjs
