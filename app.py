import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="NEON CYBER FPS 3D", layout="centered")

st.markdown("""
    <style>
    body { background-color: rgb(2, 6, 23); }
    h1 { color: rgb(255, 0, 127); text-align: center; font-family: 'Impact', sans-serif; text-shadow: 0 0 20px rgb(255, 0, 127); font-size: 3rem; }
    .stDescription { text-align: center; color: rgb(100, 116, 139); }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ NEON CYBER FPS 3D")
st.caption("클릭 오류 해결 완료! 화면 위에 마우스를 올리고 움직이면 바로 조준 및 사격이 가능합니다.")

# Pointer Lock을 제거하고 일반 마우스 좌표 추적(Mouse Tracking) 방식으로 변환한 코드
fps_3d_html = """
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
            cursor: crosshair; /* 마우스 커서 자체를 조준선 모양으로 변경 */
        }
        #hud {
            position: absolute;
            top: 20px;
            left: 20px;
            color: rgb(255, 255, 255);
            font-size: 24px;
            font-weight: bold;
            text-shadow: 0 0 10px rgb(0, 255, 255);
            z-index: 10;
            pointer-events: none;
        }
        #info-overlay {
            position: absolute;
            bottom: 20px;
            right: 20px;
            color: rgb(148, 163, 184);
            font-size: 12px;
            text-align: right;
            line-height: 1.6;
            background: rgba(15, 23, 42, 0.8);
            padding: 10px;
            border-radius: 8px;
            border: 1px solid rgb(51, 65, 85);
            pointer-events: none;
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

<div id="game-container">
    <div id="hud">SCORE: <span id="score-val">0</span> | AMMO: <span id="ammo-val">30</span></div>
    
    <div id="info-overlay">
        <b>[컨트롤]</b><br>
        마우스 무브: 화면 안에서 조준 시점 회전<br>
        마우스 클릭: <b>총기 발사 (클릭 즉시 작동)</b><br>
        W, A, S, D: 플레이어 이동<br>
        R 키: 재장전 (RELOAD)
    </div>
</div>

<script>
    let scene, camera, renderer;
    let score = 0;
    let ammo = 30;
    let isReloading = false;
    let targets = [];
    let bullets = [];
    let flashMuzzle;
    
    // 레이캐스터 및 마우스 벡터 생성
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    
    let pitch = 0, yaw = 0;
    const moveSpeed = 0.15;
    const keys = { w: false, a: false, s: false, d: false };

    const container = document.getElementById('game-container');

    function init() {
        scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x020617, 0.015);

        camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.set(0, 1.6, 0);

        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        container.appendChild(renderer.domElement);

        const ambientLight = new THREE.AmbientLight(0x0a0a20);
        scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0xff007f, 0.8);
        dirLight.position.set(10, 20, 10);
        scene.add(dirLight);

        const gridHelper = new THREE.GridHelper(200, 50, 0xff007f, 0x1e293b);
        gridHelper.position.y = 0;
        scene.add(gridHelper);

        const gunGeometry = new THREE.BoxGeometry(0.1, 0.1, 0.5);
        const gunMaterial = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.2, metalness: 0.8 });
        const gun = new THREE.Mesh(gunGeometry, gunMaterial);
        gun.position.set(0.2, -0.2, -0.4); 
        camera.add(gun);
        scene.add(camera);

        const flashGeo = new THREE.SphereGeometry(0.08, 8, 8);
        const flashMat = new THREE.MeshBasicMaterial({ color: 0xffff00, transparent: true, opacity: 0 });
        flashMuzzle = new THREE.Mesh(flashGeo, flashMat);
        flashMuzzle.position.set(0.2, -0.2, -0.65);
        camera.add(flashMuzzle);

        for(let i=0; i<15; i++) spawnTarget();

        // 마우스 록이 필요 없는 유연한 이벤트 리스너로 전면 교체
        container.addEventListener('mousemove', onMouseMove);
        container.addEventListener('mousedown', onMouseDown);
        document.addEventListener('keydown', onKeyDown);
        document.addEventListener('keyup', onKeyUp);
        window.addEventListener('resize', onWindowResize);

        animate();
    }

    // 마우스의 절대 위치를 계산하여 부드럽게 시선 방향 설정
    function onMouseMove(e) {
        const rect = container.getBoundingClientRect();
        // 캔버스 기준 마우스 상대 좌표 계산 (-1 ~ 1 변환)
        mouse.x = ((e.clientX - rect.left) / container.clientWidth) * 2 - 1;
        mouse.y = -((e.clientY - rect.top) / container.clientHeight) * 2 + 1;

        // 조준선 움직임에 맞춰 카메라 회전 각도 실시간 대입
        yaw = -mouse.x * 1.2; 
        pitch = mouse.y * 0.8;

        camera.quaternion.setFromEuler(new THREE.Euler(pitch, yaw, 0, 'YXZ'));
    }

    function spawnTarget() {
        const geometry = new THREE.IcosahedronGeometry(0.6 + Math.random()*0.4, 0);
        const colorPool = [0x00ffff, 0xff007f, 0x39ff14, 0xffff00];
        const randomColor = colorPool[Math.floor(Math.random() * colorPool.length)];
        
        const material = new THREE.MeshStandardMaterial({
            color: randomColor,
            emissive: randomColor,
            emissiveIntensity: 0.5,
            roughness: 0.1
        });
        
        const target = new THREE.Mesh(geometry, material);
        
        const angle = Math.random() * Math.PI * 2;
        const radius = 15 + Math.random() * 25;
        target.position.set(Math.cos(angle)*radius, 1 + Math.random()*4, Math.sin(angle)*radius);
        
        target.userData = {
            speed: 0.02 + Math.random() * 0.04,
            wobbleSpeed: Math.random() * 0.05
        };

        scene.add(target);
        targets.push(target);
    }

    function onMouseDown(e) {
        if (ammo <= 0 || isReloading) return;

        ammo--;
        document.getElementById('ammo-val').innerText = ammo;

        flashMuzzle.material.opacity = 1;
        setTimeout(() => { flashMuzzle.material.opacity = 0; }, 40);

        // 현재 마우스가 위치한 커서 포인트를 향해 레이저 광선 발사 판정
        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(targets);

        if (intersects.length > 0) {
            const hitTarget = intersects[0].object;
            createHitEffect(hitTarget.position);

            scene.remove(hitTarget);
            targets = targets.filter(t => t !== hitTarget);
            spawnTarget();

            score += 100;
            document.getElementById('score-val').innerText = score;
        }
    }

    function createHitEffect(pos) {
        const pCount = 8;
        const pGeo = new THREE.BoxGeometry(0.1, 0.1, 0.1);
        const pMat = new THREE.MeshBasicMaterial({ color: 0x00ffff });
        
        for(let i=0; i<pCount; i++) {
            const p = new THREE.Mesh(pGeo, pMat);
            p.position.copy(pos);
            p.userData = {
                vX: (Math.random() - 0.5) * 0.3,
                vY: (Math.random() - 0.5) * 0.3,
                vZ: (Math.random() - 0.5) * 0.3,
                life: 15
            };
            scene.add(p);
            bullets.push(p);
        }
    }

    function onKeyDown(e) {
        const key = e.key.toLowerCase();
        if (key in keys) keys[key] = true;

        if (key === 'r' && ammo < 30 && !isReloading) {
            isReloading = true;
            document.getElementById('ammo-val').innerText = "RELOAD";
            setTimeout(() => {
                ammo = 30;
                document.getElementById('ammo-val').innerText = ammo;
                isReloading = false;
            }, 1200);
        }
    }

    function onKeyUp(e) {
        const key = e.key.toLowerCase();
        if (key in keys) keys[key] = false;
    }

    function onWindowResize() {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    }

    function animate() {
        requestAnimationFrame(animate);

        const forward = new THREE.Vector3(0, 0, -1).applyQuaternion(camera.quaternion);
        const right = new THREE.Vector3(1, 0, 0).applyQuaternion(camera.quaternion);
        forward.y = 0; forward.normalize(); 
        right.y = 0; right.normalize();

        if (keys.w) camera.position.addScaledVector(forward, moveSpeed);
        if (keys.s) camera.position.addScaledVector(forward, -moveSpeed);
        if (keys.a) camera.position.addScaledVector(right, -moveSpeed);
        if (keys.d) camera.position.addScaledVector(right, moveSpeed);

        targets.forEach(target => {
            target.rotation.x += 0.01;
            target.rotation.y += 0.02;

            const dir = new THREE.Vector3(camera.position.x, target.position.y, camera.position.z).sub(target.position).normalize();
            target.position.addScaledVector(dir, target.userData.speed);
            target.position.y += Math.sin(Date.now() * target.userData.wobbleSpeed) * 0.01;

            if (target.position.distanceTo(camera.position) < 2) {
                scene.remove(target);
                targets = targets.filter(t => t !== target);
                spawnTarget();
                if(score > 0) score -= 50; 
                document.getElementById('score-val').innerText = score;
            }
        });

        for (let i = bullets.length - 1; i >= 0; i--) {
            const p = bullets[i];
            p.position.x += p.userData.vX;
            p.position.y += p.userData.vY;
            p.position.z += p.userData.vZ;
            p.userData.life--;
            if (p.userData.life <= 0) {
                scene.remove(p);
                bullets.splice(i, 1);
            }
        }

        renderer.render(scene, camera);
    }

    window.onload = init;
</script>
</body>
</html>
"""

# HTML 요소 렌더링
components.html(fps_3d_html, height=580)
