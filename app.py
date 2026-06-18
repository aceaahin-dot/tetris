import streamlit as st
import streamlit.components.v1 as components
import base64

# 1. 페이지 및 레이아웃 설정
st.set_page_config(page_title="3D 볼링 게임", page_icon="🎳", layout="wide")

st.title("🎳 스트림릿 고퀄리티 3D 볼링 게임")
st.write("아래 3D 화면을 클릭하고 **마우스를 드래그해서 앞으로 던지면** 공이 굴러갑니다!")

# 2. 문법 에러를 완벽히 차단하기 위한 Base64 데이터
b64_html = (
    "PCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImtvIj4KPGhlYWQ+CiAgICA8bWV0YSBjaGFyc2V0"
    "PSJVVEYtOCI+CiAgICA8dGl0bGU+M0QgQm93bGluZyBHYW1lPC90aXRsZT4KICAgIDxzdHlsZT4K"
    "ICAgICAgICBib2R5IHsgbWFyZ2luOiAwOyBvdmVyZmxvdzogaGlkZGVuOyBiYWNrZ3JvdW5kLWNv"
    "bG9yOiAjMWExYTFhOyBmb250LWZhbWlseTogc2Fucy1zZXJpZjsgfQogICAgICAgIGNhbnZhcyB7"
    "IGRpc3BsYXk6IGJsb2NrOyB9CiAgICAgICAgI2luZm8geyBwb3NpdGlvbjogYWJzb2x1dGU7IHRv"
    "cDogMTBweDsgbGVmdDogMTBweDsgY29sb3I6IHdoaXRlOyBiYWNrZ3JvdW5kOiByZ2JhKDAsMCww"
    "LDAuNyk7IHBhZGRpbmc6IDEwcHg7IGJvcmRlci1yYWRpdXM6IDVweDsgcG9pbnRlci1ldmVudHM6"
    "IG5vbmU7IHotaW5kZXg6IDEwOyB9CiAgICAgICAgI
