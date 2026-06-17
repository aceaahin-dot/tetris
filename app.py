import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="NEON M4 SURVIVAL 3D", layout="centered")
st.title("💥 M4 NEON SURVIVAL 3D")
st.caption("WASD로 이동하고 마우스로 화면을 움직여 몰려오는 NPC를 사격하세요.")

# 1. 파일 경로 정의
html_path = os.path.join(os.path.dirname(__file__), "game.html")

# 2. 문법 오류 방지를 위해 백엔드에서 game.html 파일을 동적으로 안전하게 생성
html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { margin: 0; overflow: hidden; background-color: rgb(2,6,23); font-family: sans-serif; user-select: none; }
        #game-container { position: relative; width: 100%; height: 530px; border: 4px solid rgb(255,0,127); border-radius: 15px; overflow: hidden; cursor: crosshair; background-color: rgb(2,6,23); }
        #hud { position: absolute; top: 20px; left: 20px; color: rgb(255,255,255); font-size: 20px; font-weight: bold; z-index: 10; pointer-events: none; }
        #hp-container { position: absolute; top: 20px; right: 20px; width: 200px; height: 20px; background: rgba(255,255,255,0.2); border: 2px solid rgb(255,255,255); border-radius: 5px; z-index: 10; }
        #hp-bar { width: 100%; height: 100%; background: rgb(239,68,68); }
        #damage-flash { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(239,68,68,0); pointer-events: none; z-index: 5; }
        #gameover-screen { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(2,6,23,0.95); display: none; flex-direction: column; justify-content: center; align-items: center; color: rgb(255,255,255); z-index: 20; }
        .btn-restart { background: rgb(0,255,255); border: none; color: rgb(0,0,0); padding: 10px 25px; font-size: 16px; font-weight: bold; border-radius: 5px; cursor: pointer; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
<div id="game-container">
    <div id="damage-flash"></div>
    <div id="hud">SCORE: <span id="score-val">0</span> | AMMO: <span id="ammo-val">30</span></div>
    <div id="hp-container"><div id="hp-bar"></div></div>
    <div id="gameover-screen">
        <h2 style="color:rgb(239,68,68); font-size:2.5rem;">GAME OVER</h2>
        <button class="btn-restart" onclick="restartGame()">다시 시작</button>
    </div>
</div>
<script>
    let scene, camera, renderer, score = 0, playerHp = 100, ammo = 30, isReloading = false, gameActive = true, npcList = [], bullets = [], flashMuzzle, m4GunGroup;
    const raycaster = new THREE.Raycaster(), mouse = new THREE.Vector2(), keys = { w: false, a: false, s: false, d: false }, container = document.getElementById('game-container');
    function init() {
        scene = new THREE.Scene(); scene.fog = new THREE.FogExp2(0x020617, 0.015);
        camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000); camera.position.set(0, 1.6, 0);
        renderer = new THREE.WebGLRenderer({ antialias: true }); renderer.setSize(container.clientWidth, container.clientHeight); container.appendChild(renderer.domElement);
        scene.add(new THREE.AmbientLight(0x151525)); const dirLight = new THREE.DirectionalLight(0xff007f, 1.0); dirLight.position.set(10, 30, 10); scene.add(dirLight); scene.add(new THREE.GridHelper(200, 40, 0xff007f, 0x1e293b));
        m4GunGroup = new THREE.Group(); const gunMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.6 }); m4GunGroup.add(new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.07, 0.25), gunMat));
        const barrel = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.01, 0.25), new THREE.MeshStandardMaterial({ color: 0x0f172a })); barrel.rotation.x = Math.PI / 2; barrel.position.set(0, 0.01, -0.2); m4GunGroup.add(barrel);
        const mag = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.1, 0.05), gunMat); mag.position.set(0, -0.07, -0.03); mag.rotation.x = 0.15; m4GunGroup.add(mag); m4GunGroup.position.set(0.2, -0.2, -0.4); camera.add(m4GunGroup); scene.add(camera);
        flashMuzzle = new THREE.Mesh(new THREE.SphereGeometry(0.05
