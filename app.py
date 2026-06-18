import streamlit as st
import random
import time

# 페이지 설정
st.set_page_config(page_title="스트림릿 볼링 게임", page_icon="🎳", layout="centered")

# 세션 상태(Session State) 초기화
if "frame" not in st.session_state:
    st.session_state.frame = 1
    st.session_state.roll = 1
    st.session_state.pins_left = 10
    st.session_state.scores = []  # 각 투구별 쓰러뜨린 핀 수
    st.session_state.frame_scores = {}  # 프레임별 누적 점수
    st.session_state.game_over = False
    st.session_state.current_frame_rolls = []

st.title("🎳 스트림릿 텍스트 볼링 게임")
st.write("조준 게이지를 맞추고 공을 굴려 스트라이크를 노려보세요!")

# --- 게임 리셋 함수 ---
def reset_game():
    st.session_state.frame = 1
    st.session_state.roll = 1
    st.session_state.pins_left = 10
    st.session_state.scores = []
    st.session_state.frame_scores = {}
    st.session_state.game_over = False
    st.session_state.current_frame_rolls = []

# --- 볼링 핀 시각화 ---
def display_pins(pins_left):
    # 남은 핀 개수에 따라 간단하게 핀 모양 출력
    pin_symbol = "⚪"
    hit_symbol = "❌"
    
    # 10개 핀 위치 배열 (4열, 3열, 2열, 1열)
    # 실제 남은 개수만큼 앞에서부터 채우는 간단한 방식
    pins = [pin_symbol if i < pins_left else hit_symbol for i in range(10)]
    
    st.text(f"  {pins[6]}   {pins[7]}   {pins[8]}   {pins[9]}")
    st.text(f"    {pins[3]}   {pins[4]}   {pins[5]}")
    st.text(f"      {pins[1]}   {pins[2]}")
    st.text(f"        {pins[0]}")

# --- 볼링 점수 계산 로직 (간단 버전) ---
def calculate_total_score():
    # 복잡한 스페어/스트라이크 보너스 처리를 위한 기본 점수 합산
    # (여기서는 현재까지 쓰러뜨린 총 핀 수로 단순 합산 표시)
    return sum(st.session_state.scores)


# --- 메인 게임 루프 ---
if not st.session_state.game_over:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader(f"현재: {st.session_state.frame} 프레임 - {st.session_state.roll}번째 투구")
        st.write(f"남은 핀: **{st.session_state.pins_left}** 개")
        display_pins(st.session_state.pins_left)
        
    with col2:
        st.subheader("🎯 조준하기")
        # 사용자가 수동으로 조절하는 게이지 (게이지가 50에 가까울수록 스트라이크 확률 업)
        power = st.slider("파워 및 타이밍 조정 (50에 맞추세요!)", 0, 100, 50)
        
        if st.button("🎳 공 굴리기!!", use_container_width=True):
            # 조준도 계산 (50에서 멀어질수록 페널티)
            accuracy = 100 - abs(50 - power) # 최대 100점
            
            # 쓰러뜨릴 수 있는 최대 핀 수 범위 내에서 무작위 결정 (정확도가 높으면 최소 기댓값 상승)
            max_possible = st.session_state.pins_left
            min_possible = int(max_possible * (accuracy / 200)) # 정확도 100일 때 최소 절반은 쓰러뜨림
            
            if min_possible > max_possible:
                min_possible = max_possible
                
            pins_hit = random.randint(min_possible, max_possible)
            
            # 스트라이크/스페어 이펙트용 문구
            if st.session_state.roll == 1 and pins_hit == 10:
                st.balloons()
                st.success("🔥 STRIKE!!! 🔥")
            elif st.session_state.roll == 2 and st.session_state.pins_left - pins_hit == 0:
                st.success("✨ SPARE! ✨")
            else:
                st.info(f"🎉 {pins_hit}개의 핀을 쓰러뜨렸습니다!")
                
            # 데이터 업데이트
            st.session_state.scores.append(pins_hit)
            st.session_state.current_frame_rolls.append(pins_hit)
            st.session_state.pins_left -= pins_hit
            
            # 프레임 전환 로직
            # 1~9프레임 일반 규칙
            if st.session_state.frame < 10:
                if st.session_state.roll == 1 and st.session_state.pins_left == 0:
                    # 스트라이크 시 프레임 종료
                    st.session_state.frame_scores[st.session_state.frame] = f"X"
                    st.session_state.frame += 1
                    st.session_state.pins_left = 10
                    st.session_state.current_frame_rolls = []
                elif st.session_state.roll == 2:
                    # 2구 던졌으면 프레임 종료
                    if st.session_state.pins_left == 0:
                        st.session_state.frame_scores[st.session_state.frame] = f"{st.session_state.current_frame_rolls[0]}/"
                    else:
                        st.session_state.frame_scores[st.session_state.frame] = f"{st.session_state.current_frame_rolls[0]}-{pins_hit}"
                    st.session_state.frame += 1
                    st.session_state.roll = 1
                    st.session_state.pins_left = 10
                    st.session_state.current_frame_rolls = []
                else:
                    st.session_state.roll = 2
            
            # 10프레임 특수 규칙 (간단하게 2구 투구로 일단 마감 처리)
            else:
                if st.session_state.roll == 2 or st.session_state.pins_left == 0:
                    st.session_state.frame_scores[st.session_state.frame] = "Fin"
                    st.session_state.game_over = True
                else:
                    st.session_state.roll = 2
                    
            time.sleep(1)
            st.rerun()

else:
    st.balloons()
    st.subheader("🏁 게임 종료!")
    st.header(f"최종 총 점수: {calculate_total_score()} 점")
    
    if st.button("🔄 다시 도전하기", on_click=reset_game):
        st.rerun()

# --- 전광판(Scoreboard) 출력 ---
st.divider()
st.subheader("📊 현재 전광판")

# 표 형태로 전광판 시각화
cols = st.columns(10)
for i in range(1, 11):
    with cols[i-1]:
        st.metric(label=f"{i} F", value=st.session_state.frame_scores.get(i, "-"))

st.write(f"**현재 누적 점수:** {calculate_total_score()}점")
