import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="3D 볼링 게임", page_icon="🎳", layout="wide")

st.title("🎳 스트림릿 고퀄리티 3D 볼링 게임")
st.write("아래 3D 화면을 클릭하고 **마우스를 드래그(또는 스와이프)해서 앞으로 던지면** 공이 굴러갑니다!")

# Three.js와 미니 물리엔진이 포함된 HTML/JS 게임 코드
three_js_bowling = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>3D Bowling</title>
    <style>
        body { margin: 0; overflow: hidden; background-color: #1a1a1a; font-family: sans-serif; }
        canvas { display: block; }
        #info {
            position: absolute; top: 10px; left: 10px; color: white;
            background: rgba(0,0,0,0.7); padding: 10px; border-radius: 5px;
            pointer-events: none;
        }
        #score-board {
            position: absolute; top: 10px; right: 10px; color: #fff;
            background: rgba(0,0,0,0.8); padding: 15px; border-radius: 8px;
            border: 2px solid #333; font-size: 18px;
        }
        #reset-btn {
            position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
            padding: 12px 24px; font-size: 16px; background-color: #ff4b4b;
            color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;
        }
        #reset-btn:hover { background-color: #ff3333; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

    <div id="info">🕹️ 조작법: 공을 마우스로 붙잡고 앞(위쪽)으로 빠르게 드래그해서 던지세요!</div>
    <div id="score-board">🎳 쓰러진 핀: <span id="score">0</span> / 10</div>
    <button id="reset-btn" onclick="resetGame()">🎳 다시 던지기 (리셋)</button>

    <script>
        let scene, camera, renderer;
        let ball, lane;
        let pins = [];
        let pinPositions = [];
        
        let ballVelocity = { x: 0, y: 0, z: 0 };
        let isThrown = false;
        let gravity = -0.005;
        
        let isMouseDown = false;
        let mouseStart = { x: 0, y: 0, time: 0 };

        init();
        animate();

        function init() {
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x14141f);
            
            camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(0, 5, 18);
            camera.lookAt(0, 1, -10);

            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.shadowMap.enabled = true;
            document.body.appendChild(renderer.domElement);

            const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
            scene.add(ambientLight);

            const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
            dirLight.position.set(5, 15, 10);
            dirLight.castShadow = true;
            scene.add(dirLight);

            const laneGeo = new THREE.BoxGeometry(4, 0.2, 30);
            const laneMat = new THREE.MeshStandardMaterial({ color: 0xd2a679, roughness: 0.1 });
            lane = new THREE.Mesh(laneGeo, laneMat);
            lane.position.set(0
