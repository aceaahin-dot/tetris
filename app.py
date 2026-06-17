import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="NEON M4 SURVIVAL 3D", layout="centered")

st.markdown("""
    <style>
    body { background-color: rgb(2, 6, 23); }
    h1 { color: rgb(255, 0, 127); text-align: center; font-family: 'Impact', sans-serif; text-shadow: 0 0 20px rgb(255, 0, 127); font-size: 3rem; }
    </style>
""", unsafe_allow_html=True)

st.title("💥 M4 NEON SURVIVAL 3D")
st.caption("안정성 업그레이드 완료 버전. WASD 이동 및 마우스 조준 사격으로 NPC를 저지하세요.")

# 에러 유발 가능성을 원천 차단한 HTML/JS 결합 소스
fps_m4_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {
            margin: 0;
            overflow: hidden;
            background-color: rgb(2, 6, 23);
            font-family: 'Segoe UI', sans-serif;
            user-select: none;
        }
        #game-container {
            position: relative;
            width: 100%;
            height: 550px;
            border: 4px solid rgb(255, 0, 127);
            border-radius: 15px;
            box-shadow: 0 0 40px rgba(255, 0, 127, 0.3);
            overflow: hidden;
            cursor: crosshair;
        }
        #hud {
            position: absolute;
            top: 20px;
            left: 20px;
            color: rgb(255, 255, 255);
            font-size: 20px;
            font-weight: bold;
            text-shadow: 0 0 10px rgb(0, 255, 255);
            z-index: 10;
            pointer-events: none;
        }
        #hp-container {
            position: absolute;
            top: 20px;
            right: 20px;
            width: 200px;
            height: 20px;
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid #fff;
            border-radius: 5px;
            overflow: hidden;
            z-index: 10;
        }
        #hp-bar {
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, rgb(239, 68, 68) 0%, rgb(220, 38, 38) 100%);
            transition: width 0.1s ease;
        }
        #info-overlay {
            position: absolute;
            bottom: 20px;
            left: 20px;
            color: rgb(148, 163, 184);
            font-size: 12px;
            line-height: 1.6;
            background: rgba(15, 23, 42, 0
