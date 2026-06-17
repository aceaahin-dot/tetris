import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="NEON M4 SURVIVAL 3D", layout="centered")
st.title("💥 M4 NEON SURVIVAL 3D")
st.caption("구문 오류 원천 차단 버전. WASD 이동 및 마우스 조준 사격으로 NPC를 저지하세요.")

html_path = os.path.join(os.path.dirname(__file__), "game.html")

# 텍스트 파싱 에러를 막기 위해 바이트 조각으로 나누어 안전하게 파일 생성
html_chunks = [
    b"<!DOCTYPE html><html><head><meta charset='utf-8'><style>",
    b"body { margin: 0; overflow: hidden; background-color: rgb(2,6,23); font-family: sans-serif; user-select: none; }",
    b"#game-container { position: relative; width: 100%; height: 530px; border: 4px solid rgb(255,0,127); border-radius: 15px; overflow: hidden; cursor: crosshair; background-color: rgb(2,6,23); }",
    b"#hud { position: absolute; top: 20px; left: 20px; color: rgb(255,255,255); font-size: 20px; font-weight: bold; z-index: 10; pointer-events: none; }",
    b"#hp-container { position: absolute; top: 20px; right: 20px; width: 200px; height: 20px; background: rgba(255,255,255,0.2); border: 2px solid rgb(255,255,255); border-radius: 5px; z-index: 10; }",
    b"#hp-bar { width: 100%; height: 100%; background: rgb(239,68,68); }",
    b"#damage-flash { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(239,68,68,0); pointer-events: none; z-index: 5; }",
    b"#gameover-screen { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(2,6,23,0.95); display: none; flex-direction: column; justify-content: center; align-items: center; color: rgb(255,255,255); z-index: 20; }",
    b".btn-restart { background: rgb(0,255,255); border: none; color: rgb(0,0,0); padding: 10px 25px; font-size: 16px; font-weight: bold; border-radius: 5px; cursor: pointer; }",
    b"</style><script src='https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js'></script></head><body>",
    b"<div id='game-container'><div id='damage-flash'></div><div id='hud'>SCORE: <span id='score-val'>0</span> | AMMO: <span id='ammo-val'>30</span></div>",
    b"<div id='hp-container'><div id='hp-bar'></div></div><div id='gameover-screen'><h2 style='color:rgb(239,68,68); font-size:2.5rem;'>GAME OVER</h2>",
    b"<button class='btn-restart' onclick='restartGame()'>\xeb\x8a\xac\xec\x8b\x9c \xec\x8b\x9c\xec\x9e\x91</button></div></div>",
    b"<script>let scene, camera, renderer, score = 0, playerHp = 100, ammo = 30, isReloading = false, gameActive = true, npcList = [], bullets = [], flashMuzzle, m4GunGroup;",
    b"const raycaster = new THREE.Raycaster(), mouse = new THREE.Vector2(), keys = { w: false, a: false, s: false, d: false }, container = document.getElementById('game-container');",
    b"function init() {
    
