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
st.caption("M4 소총으로 몰려오는 인간형 NPC들을 처치하세요! 적이 접근하면 데미지를 입습니다.")

# Three.js 엔진 기반 M4 + NPC 슈팅 게임 HTML
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
        /* HUD 및 UI 레이어 */
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
        /* 실시간 HP 체력바 UI */
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
            background: rgba(15, 23, 42, 0.8);
            padding: 10px;
            border-radius: 8px;
            border: 1px solid rgb(51, 65, 85);
            pointer-events: none;
        }
        /* 피격 시 화면 붉어짐 이펙트 */
        #damage-flash {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba
