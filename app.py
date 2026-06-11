import streamlit as st
import numpy as np
from PIL import Image
import io
import os
from datetime import datetime

st.set_page_config(
    page_title="Lumina Grade | LUT Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)
# ══════════════════════════════════════════════════════════
with st.container(key="lumina-styles"):
    st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet" />
<style>
    :root {
        --background: #0a0a0a;
        --surface: #131313;
        --surface-container: #151515;
        --surface-container-low: #111111;
        --surface-container-lowest: #080808;
        --surface-container-high: #1a1a1a;
        --surface-container-highest: #353534;
        --surface-variant: #1c1c1c;
        --surface-bright: #252525;
        --primary: #00a3ff;
        --primary-container: #004a77;
        --secondary: #ffb77f;
        --outline: #444c56;
        --outline-variant: #2d333b;
        --on-surface: #e5e2e1;
        --on-surface-variant: #8b949e;
        --on-primary: #003354;
    }

    /* ── Global Styles ── */
    .stApp {
        background-color: var(--background) !important;
        color: var(--on-surface) !important;
    }
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
    }
    .mono {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Icon family safety */
    [data-testid="stIconMaterial"], .material-symbols-outlined, .material-symbols-rounded {
        font-family: 'Material Symbols Outlined' !important;
        font-variation-settings: 'FILL' 0, 'wght' 300, 'GRAD' 0, 'opsz' 20 !important;
        vertical-align: middle;
    }

    /* Prevent flashing during updates */
    [data-stale="true"], .stApp [data-stale="true"], .element-container[data-stale="true"] {
        opacity: 1 !important;
    }
    [data-testid="stImage"], [data-testid="stImage"] img, .element-container, .stMarkdown {
        transition: none !important;
    }
    [data-testid="stStatusWidget"], [data-testid="stStatusWidgetContainer"] {
        display: none !important;
    }
    footer, #MainMenu {
        visibility: hidden;
        height: 0;
    }
    header[data-testid="stHeader"],
    .stAppHeader,
    [data-testid="stAppHeader"] {
        display: none !important;
        height: 0px !important;
    }
    [data-testid="stToolbar"], [data-testid="stAppToolbar"] {
        display: none !important;
    }
    [data-testid="stSidebarHeader"], [data-testid="stSidebarCollapseButton"], [data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"] {
        display: none !important;
        height: 0px !important;
        padding: 0px !important;
        margin: 0px !important;
    }

    /* ── Layout Overrides ── */
    .stApp {
        background-color: var(--background) !important;
        color: var(--on-surface) !important;
        height: 100vh !important;
        overflow: hidden !important;
        box-sizing: border-box !important;
    }
    [data-testid="stAppViewContainer"] {
        height: 100vh !important;
        display: flex !important;
        flex-direction: row !important;
        overflow: hidden !important;
        box-sizing: border-box !important;
    }
    [data-testid="stMain"] {
        position: fixed !important;
        left: 290px !important;
        top: 60px !important;
        right: 0 !important;
        bottom: 32px !important;
        width: calc(100% - 290px) !important; /* Uses percentage instead of vw to avoid scrollbar clipping */
        height: calc(100vh - 92px) !important;
        overflow-y: auto !important;
        background-color: var(--background) !important;
        box-sizing: border-box !important;
        margin: 0 !important;
        padding-top: 0px !important; /* Removes default Streamlit main container top padding to align content flush */
        padding-bottom: 0px !important;
    }
    /* 이미지 확대(전체화면)를 메인 영역 정중앙에 표시 → 사이드바/헤더 가리지 않음 */
    [data-testid="stFullScreenFrame"]:has(button[aria-label="Close fullscreen"]) {
        position: fixed !important;
        left: 290px !important;
        top: 60px !important;
        right: 0 !important;
        bottom: 32px !important;
        width: calc(100% - 290px) !important;
        height: calc(100vh - 92px) !important;
        z-index: 1500 !important;
        background: rgba(0,0,0,0.94) !important;
        overflow: hidden !important;
    }
    /* 이미지: 영역 정중앙에 절대 배치, 위아래 여백 확보 */
    [data-testid="stFullScreenFrame"]:has(button[aria-label="Close fullscreen"]) img {
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        max-width: 92% !important;
        max-height: 84% !important;
        width: auto !important;
        height: auto !important;
        object-fit: contain !important;
        margin: 0 !important;
    }
    /* 닫기 버튼 툴바를 헤더 아래(메인 영역 우상단)로 이동 → 헤더에 안 가리고 항상 클릭 가능 */
    [data-testid="stFullScreenFrame"]:has(button[aria-label="Close fullscreen"]) [data-testid="stElementToolbar"] {
        position: fixed !important;
        top: 72px !important;
        right: 18px !important;
        left: auto !important;
        bottom: auto !important;
        z-index: 1000002 !important;
        opacity: 1 !important;
        transform: none !important;
    }
    button[aria-label="Close fullscreen"] {
        background: rgba(20,20,20,.92) !important;
        border: 1px solid var(--outline-variant) !important;
        border-radius: 8px !important;
        width: 34px !important; height: 34px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,.7) !important;
        color: #fff !important;
    }
    [data-testid="stSidebar"] {
        position: fixed !important;
        left: 0 !important;            /* 전체화면 등에서 왼쪽 잘림 방지: 뷰포트 왼쪽에 고정 */
        top: 60px !important;
        bottom: 32px !important;
        height: calc(100vh - 92px) !important;
        background-color: var(--surface-container-low) !important;
        border-right: 1px solid var(--outline-variant) !important;
        width: 290px !important;
        min-width: 290px !important;
        max-width: 290px !important;
        z-index: 1000 !important;
        box-sizing: border-box !important;
        transform: none !important;
        visibility: visible !important;
        margin-left: 0 !important;
        overflow-y: auto !important;   /* 내용이 길면 잘리지 않고 스크롤 */
    }
    [data-testid="stBlockContainer"],
    [data-testid="stMainBlockContainer"],
    .block-container,
    .stMainBlockContainer {
        padding-top: 0px !important; /* Starts flush below the top header bar for alignment */
        padding-bottom: 24px !important;
        padding-left: 24px !important;
        padding-right: 24px !important;
        max-width: 100% !important;
        width: 100% !important;
        box-sizing: border-box !important;
        margin-top: 0px !important;
    }
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0px !important;
        margin-top: 0px !important;
    }
    [data-testid="stSidebarUserContent"],
    [data-testid="stSidebarContent"],
    .stSidebarContent {
        padding-top: 0px !important; /* Starts flush below the top header bar for sidebar content */
        padding-bottom: 16px !important;
        padding-left: 8px !important;
        padding-right: 8px !important;
        margin-top: 0px !important;
    }
    /* Hide/remove the styles wrapper container from layout flow so it doesn't create gaps */
    .st-key-lumina-styles {
        position: absolute !important;
        width: 0px !important;
        height: 0px !important;
        overflow: hidden !important;
        margin: 0px !important;
        padding: 0px !important;
    }

    /* Fixed Header and Footer Styling */
    .lumina-fixed-header {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 60px !important;
        background-color: var(--surface-container-low) !important;
        border-bottom: 1px solid var(--outline-variant) !important;
        z-index: 9999 !important;
        display: flex !important;
        justify-content: flex-start !important;
        align-items: center;
        padding: 0 16px !important;
        box-sizing: border-box !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    .header-left {
        display: flex !important;
        align-items: center !important;
        height: 100% !important;
    }
    .header-title {
        font-weight: 800;
        color: #98cbff !important;
        font-size: 26px !important;
        letter-spacing: -0.02em;
        line-height: 1.2 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        display: flex !important;
        align-items: center !important;
    }

    .lumina-fixed-footer {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 32px !important;
        background-color: var(--surface-container-lowest) !important;
        border-top: 1px solid var(--outline-variant) !important;
        z-index: 999999;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 16px;
        box-sizing: border-box;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        font-size: 10px;
        color: var(--on-surface-variant);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .footer-left {
        display: flex;
        gap: 24px;
        align-items: center;
    }
    .license-tag {
        color: var(--primary);
        font-weight: bold;
    }
    .footer-right {
        display: flex;
        gap: 24px;
        align-items: center;
    }
    .status-group {
        display: flex;
        gap: 16px;
    }
    .status-item {
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .status-dot {
        width: 5px;
        height: 5px;
        border-radius: 50%;
    }
    .status-dot.green {
        background-color: #22c55e;
    }

    .lumina-fixed-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 32px;
        background-color: var(--surface-container-lowest);
        border-top: 1px solid var(--outline-variant);
        z-index: 999999;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 16px;
        box-sizing: border-box;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        font-size: 10px;
        color: var(--on-surface-variant);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .footer-left {
        display: flex;
        gap: 24px;
        align-items: center;
    }
    .license-tag {
        color: var(--primary);
        font-weight: bold;
    }
    .footer-right {
        display: flex;
        gap: 24px;
        align-items: center;
    }
    .status-group {
        display: flex;
        gap: 16px;
    }
    .status-item {
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .status-dot {
        width: 5px;
        height: 5px;
        border-radius: 50%;
    }
    .status-dot.green {
        background-color: #22c55e;
    }

    /* ── Sidebar Slider Styling ── */
    [data-testid="stSidebar"] label p {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 10px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        color: var(--on-surface-variant) !important;
    }
    div[data-baseweb="slider"] > div {
        background-color: transparent !important;
    }
    div[data-baseweb="slider"] [role="presentation"] {
        background-color: var(--surface-variant) !important;
        height: 4px !important;
    }
    div[data-baseweb="slider"] [role="slider"] {
        background-color: var(--primary) !important;
        border: none !important;
        width: 8px !important;
        height: 8px !important;
        border-radius: 2px !important;
        box-shadow: 0 0 5px rgba(0, 163, 255, 0.4) !important;
    }
    div[data-baseweb="slider"] [role="slider"]:hover {
        background-color: #ffffff !important;
        box-shadow: 0 0 8px rgba(255, 255, 255, 0.8) !important;
    }

    /* ── Sidebar Radio Buttons ── */
    [data-testid="stSidebar"] .stRadio label p {
        font-family: 'Inter', sans-serif !important;
        font-size: 12px !important;
        color: var(--on-surface) !important;
        text-transform: none !important;
        letter-spacing: 0px !important;
    }
    [data-testid="stSidebar"] .stRadio input[type="radio"]:checked + div {
        border-color: var(--primary) !important;
        background-color: var(--primary) !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
        gap: 6px !important;
    }

    /* ── Buttons (General and Primary) ── */
    .stSidebar button {
        background-color: var(--surface-bright) !important;
        color: var(--primary) !important;
        border: 1px solid var(--outline-variant) !important;
        border-radius: 2px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 10px !important;
        text-transform: uppercase !important;
        font-weight: bold !important;
        letter-spacing: 0.05em !important;
        padding: 6px 12px !important;
        transition: all 0.2s !important;
    }
    .stSidebar button:hover {
        background-color: var(--surface-container-highest) !important;
        border-color: var(--primary) !important;
        color: #ffffff !important;
    }

    div.stButton button[kind="primary"], div.stDownloadButton button {
        background-color: var(--primary) !important;
        color: var(--on-primary) !important;
        border: 1px solid var(--primary) !important;
        border-radius: 2px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 11px !important;
        text-transform: uppercase !important;
        font-weight: bold !important;
        letter-spacing: 0.1em !important;
        box-shadow: 0 0 10px rgba(0, 163, 255, 0.15) !important;
        padding: 10px 20px !important;
        transition: all 0.2s !important;
    }
    div.stButton button[kind="primary"]:hover, div.stDownloadButton button:hover {
        background-color: #ffffff !important;
        border-color: #ffffff !important;
        color: var(--on-primary) !important;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.3) !important;
    }

    /* ── File Uploader Styling ── */
    [data-testid="stFileUploaderDropzone"] {
        background: var(--surface-container-low) !important;
        border: 1px dashed var(--outline-variant) !important;
        border-radius: 2px !important;
        padding: 24px 16px !important;
        transition: all 0.2s !important;
    }
    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: var(--primary) !important;
        box-shadow: 0 0 15px rgba(0, 163, 255, 0.15) !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] > div > span::after {
        content: "여기로 이미지를 끌어다 놓으세요";
        color: var(--on-surface);
        font-weight: 600;
        font-family: 'JetBrains Mono', 'Inter', sans-serif;
        font-size: 12px;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] > div > small::after {
        content: "JPG · PNG · TIFF · BMP · WEBP / 최대 200MB";
        color: var(--on-surface-variant);
        font-family: 'JetBrains Mono', sans-serif;
        font-size: 10px;
    }
    [data-testid="stFileUploaderDropzone"] button {
        background: var(--surface-bright) !important;
        border: 1px solid var(--outline-variant) !important;
        border-radius: 2px !important;
    }
    [data-testid="stFileUploaderDropzone"] button [data-testid="stMarkdownContainer"] p::after {
        content: "파일 선택";
        color: var(--on-surface);
        font-family: 'JetBrains Mono', sans-serif;
        font-size: 11px;
    }
    [data-testid="stFileUploaderFile"] {
        color: var(--on-surface) !important;
    }
    [data-testid="stFileUploaderFileName"] {
        color: var(--on-surface) !important;
        font-family: 'JetBrains Mono', sans-serif;
    }

    /* ── Metadata panel cards ── */
    .meta-cell {
        background-color: var(--surface-container-low);
        border: 1px solid var(--outline-variant);
        border-radius: 2px;
        padding: 12px;
        height: 60px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        font-family: 'JetBrains Mono', monospace;
        box-sizing: border-box;
    }
    .meta-label {
        font-size: 9px;
        text-transform: uppercase;
        color: var(--on-surface-variant);
        opacity: 0.5;
        letter-spacing: 0.05em;
    }
    .meta-value {
        font-size: 12px;
        color: var(--primary);
        font-weight: bold;
    }

    /* ── Swatches ── */
    .swatch-row {
        display: flex;
        gap: 6px;
        flex-wrap: wrap;
    }
    .swatch {
        width: 38px;
        height: 38px;
        border-radius: 2px;
        border: 1px solid var(--outline-variant);
    }

    /* ── Tags ── */
    .tag {
        display: inline-block;
        background-color: var(--surface-variant);
        border: 1px solid var(--outline-variant);
        padding: 3px 8px;
        border-radius: 2px;
        font-size: 10px;
        font-family: 'JetBrains Mono', monospace;
        color: var(--on-surface);
        margin: 2px;
        text-transform: uppercase;
    }
    .tag.accent {
        color: var(--primary);
        border-color: var(--primary);
    }

    /* ── Text Input Styling ── */
    input[type="text"] {
        background-color: var(--surface-container-low) !important;
        border: 1px solid var(--outline-variant) !important;
        color: #ffffff !important;
        border-radius: 2px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 12px !important;
        padding: 8px 12px !important;
    }
    input[type="text"]:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 5px rgba(0, 163, 255, 0.4) !important;
    }

    /* ── Expander Styling ── */
    div[data-testid="stExpander"] {
        background-color: var(--surface) !important;
        border: 1px solid var(--outline-variant) !important;
        border-radius: 2px !important;
    }
    div[data-testid="stExpander"] summary {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 11px !important;
        color: var(--on-surface) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    .stImage img {
        border-radius: 2px;
        border: 1px solid var(--outline-variant);
    }

    /* ════════ ✨ DESIGN POLISH (이쁘게) — 뒤 규칙이 우선 적용 ════════ */

    /* 섹션 헤더: 앞에 작은 강조 바 + 깔끔한 타이포 */
    .sec-head {
        display: flex; align-items: center; gap: 8px;
        font-family: 'Inter','Pretendard',sans-serif !important;
        font-size: 12px !important; font-weight: 700;
        letter-spacing: 0.02em; text-transform: none;
        margin: 2px 0 10px 0; color: var(--on-surface);
    }
    .sec-head::before {
        content: ""; display: inline-block; width: 3px; height: 14px;
        border-radius: 3px; background: var(--primary); flex-shrink: 0;
    }
    .sec-head.primary { color: #cfe8ff; }
    .sec-head.primary::before { background: linear-gradient(180deg,#00a3ff,#0061a8); box-shadow:0 0 8px rgba(0,163,255,.5); }
    .sec-head.secondary { color: #ffd9bd; }
    .sec-head.secondary::before { background: linear-gradient(180deg,#ffb77f,#d98a4f); box-shadow:0 0 8px rgba(255,183,127,.4); }
    .sec-head.muted { color: var(--on-surface-variant); }
    .sec-head.muted::before { background: var(--outline); box-shadow:none; }

    /* 3분할 비교 컬럼이 줌/좁은 화면에서도 세로로 쌓이지 않고 항상 가로 유지 */
    [data-testid="stHorizontalBlock"] {
        flex-direction: row !important;
        flex-wrap: nowrap !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
    [data-testid="stColumn"] {
        min-width: 0 !important;
    }

    /* 이미지: 컬럼 너비에 맞추고(가로 줄바꿈 방지) 높이는 화면에 맞게 제한 → 잘림 방지 */
    [data-testid="stImage"], [data-testid="stImageContainer"] {
        width: 100% !important;
        overflow: hidden !important;
        text-align: center !important;
    }
    [data-testid="stImage"] img, .stImage img {
        width: 100% !important;
        height: auto !important;
        max-height: calc(100vh - 260px) !important;
        object-fit: contain !important;
        display: block !important;
        margin: 0 auto !important;
        border-radius: 10px !important;
        border: 1px solid var(--outline-variant) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,.45) !important;
        transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease !important;
    }
    .stImage img:hover {
        transform: translateY(-2px);
        border-color: rgba(0,163,255,.5) !important;
        box-shadow: 0 10px 28px rgba(0,0,0,.55), 0 0 18px rgba(0,163,255,.12) !important;
    }

    /* 업로드 드롭존: 은은한 그라데이션 + 둥근 모서리 + 호버 글로우 */
    [data-testid="stFileUploaderDropzone"] {
        background: linear-gradient(145deg, #16202c 0%, var(--surface-container-low) 70%) !important;
        border: 1.5px dashed #355068 !important;
        border-radius: 12px !important;
        padding: 28px 18px !important;
    }
    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: var(--primary) !important;
        background: linear-gradient(145deg, #1a2735 0%, #141a22 70%) !important;
        box-shadow: 0 0 26px rgba(0,163,255,.18) !important;
        transform: translateY(-1px);
        transition: all .2s ease;
    }
    [data-testid="stFileUploaderDropzone"] svg { color: var(--primary) !important; }
    /* 깨진 'Upload' 라벨 숨기고 한글만 (아이콘은 유지) */
    [data-testid="stFileUploaderDropzone"] button [data-testid="stMarkdownContainer"] p { font-size: 0 !important; }
    [data-testid="stFileUploaderDropzone"] button {
        border-radius: 8px !important; padding: 7px 16px !important;
        background: var(--surface-bright) !important; transition: all .15s ease;
    }
    [data-testid="stFileUploaderDropzone"] button:hover {
        border-color: var(--primary) !important; color:#fff !important;
        box-shadow: 0 0 12px rgba(0,163,255,.25) !important;
    }

    /* 메타 카드: 그라데이션 + 둥근 모서리 + 왼쪽 강조선 */
    .meta-cell {
        background: linear-gradient(145deg, #181d24 0%, #121519 100%) !important;
        border: 1px solid var(--outline-variant) !important;
        border-left: 2px solid rgba(0,163,255,.5) !important;
        border-radius: 10px !important; height: 64px !important; padding: 12px 14px !important;
        transition: border-color .2s ease, box-shadow .2s ease;
    }
    .meta-cell:hover { border-left-color: var(--primary) !important; box-shadow: 0 0 16px rgba(0,163,255,.1) !important; }
    .meta-label { font-family:'Inter','Pretendard',sans-serif !important; opacity:.65 !important; font-size:10px !important; }
    .meta-value { font-family:'JetBrains Mono',monospace !important; font-size:14px !important; color:#eaf5ff !important; }

    /* 색상 스와치: 둥글게 + 호버 확대 */
    .swatch {
        width: 42px !important; height: 42px !important; border-radius: 9px !important;
        box-shadow: 0 3px 10px rgba(0,0,0,.4); transition: transform .15s ease;
    }
    .swatch:hover { transform: scale(1.12); }
    .swatch-row { gap: 8px !important; }

    /* 태그: 알약(pill) 모양 */
    .tag {
        border-radius: 999px !important; padding: 4px 12px !important;
        font-family: 'Inter','Pretendard',sans-serif !important; text-transform: none !important;
        font-size: 11px !important; background: rgba(255,255,255,.04) !important;
    }
    .tag.accent { background: rgba(0,163,255,.12) !important; border-color: rgba(0,163,255,.5) !important; }

    /* 버튼: 둥근 모서리 + 그라데이션 */
    div.stButton button[kind="primary"], div.stDownloadButton button {
        border-radius: 9px !important;
        background: linear-gradient(180deg,#0bb0ff,#0072c6) !important;
        border: none !important; letter-spacing: 0.04em !important;
        box-shadow: 0 4px 14px rgba(0,163,255,.28) !important;
    }
    div.stButton button[kind="primary"]:hover, div.stDownloadButton button:hover {
        background: linear-gradient(180deg,#33c0ff,#0a86e0) !important; color:#fff !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(0,163,255,.45) !important;
    }
    .stSidebar button { border-radius: 8px !important; }

    /* 프리셋 드롭다운(selectbox) 스타일 */
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background: var(--surface-bright) !important;
        border: 1px solid var(--outline-variant) !important;
        border-radius: 8px !important;
        font-family: 'Inter','Pretendard',sans-serif !important;
        font-size: 13px !important;
        min-height: 40px !important;
        cursor: pointer !important;   /* 마우스 올리면 손가락 표시 */
    }
    [data-testid="stSelectbox"] div[data-baseweb="select"] * { cursor: pointer !important; }
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover {
        border-color: var(--primary) !important;
    }
    /* 펼쳐진 옵션 목록 */
    [data-baseweb="popover"] [role="listbox"] {
        background: var(--surface-container-high) !important;
        border: 1px solid var(--outline-variant) !important;
        border-radius: 8px !important;
    }
    [data-baseweb="popover"] [role="option"] {
        font-family: 'Inter','Pretendard',sans-serif !important;
        font-size: 13px !important;
        cursor: pointer !important;
    }
    [data-baseweb="popover"] [role="option"]:hover {
        background: rgba(0,163,255,.15) !important;
    }
    /* 클릭 가능한 요소 전반에 손가락 커서 */
    .stButton button, .stDownloadButton button,
    [data-testid="stSidebar"] .stRadio label,
    [data-baseweb="slider"] [role="slider"],
    [data-testid="stFileUploaderDropzone"] button,
    button[aria-label="Fullscreen"], button[aria-label="Close fullscreen"] {
        cursor: pointer !important;
    }

    /* 입력창 / 확장 패널 둥글게 */
    input[type="text"] { border-radius: 8px !important; }
    div[data-testid="stExpander"] { border-radius: 12px !important; overflow: hidden; }
    div[data-testid="stExpander"]:hover { border-color: rgba(0,163,255,.4) !important; }
    .panel { border-radius: 12px !important; }
</style>

<!-- Fixed Header Bar -->
<header class="lumina-fixed-header">
  <div class="header-left">
    <span class="material-symbols-outlined" style="font-size: 26px; color: #98cbff; margin-right: 12px; display: flex; align-items: center;">photo_camera</span>
    <span class="header-title">Lumina Grade</span>
  </div>
</header>

<!-- Fixed Footer Bar -->
<footer class="lumina-fixed-footer">
  <div class="footer-left">
    <span>© Lumina 2026</span>
  </div>
  <div class="footer-right">
    <div class="status-group">
      <span class="status-item"><span class="status-dot green"></span>ENGINE: OK</span>
      <span class="status-item"><span class="status-dot green"></span>ACES: CONNECTED</span>
    </div>
  </div>
</footer>

<script>
    const moveElements = () => {
        const header = document.querySelector('.lumina-fixed-header');
        const footer = document.querySelector('.lumina-fixed-footer');
        let headerMoved = false;
        let footerMoved = false;
        if (header && header.parentElement !== document.body) {
            const oldHeader = document.querySelector('body > .lumina-fixed-header');
            if (oldHeader) oldHeader.remove();
            document.body.appendChild(header);
            headerMoved = true;
        }
        if (footer && footer.parentElement !== document.body) {
            const oldFooter = document.querySelector('body > .lumina-fixed-footer');
            if (oldFooter) oldFooter.remove();
            document.body.appendChild(footer);
            footerMoved = true;
        }
        return headerMoved && footerMoved;
    };
    
    // Poll to make sure elements are moved as they render
    let attempts = 0;
    const interval = setInterval(() => {
        const done = moveElements();
        attempts++;
        if (done || attempts > 50) {
            clearInterval(interval);
        }
    }, 100);
</script>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  COLOR SCIENCE
# ════════════════════════════════════════════════════════════
def rgb_to_lab(rgb: np.ndarray) -> np.ndarray:
    mask = rgb > 0.04045
    rgb_linear = np.where(mask, ((rgb + 0.055) / 1.055) ** 2.4, rgb / 12.92)
    mat = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041],
    ])
    xyz = rgb_linear @ mat.T
    xyz[:, 0] /= 0.95047
    xyz[:, 2] /= 1.08883
    epsilon, kappa = 0.008856, 903.3
    mask = xyz > epsilon
    f = np.where(mask, np.cbrt(xyz), (kappa * xyz + 16.0) / 116.0)
    L = 116.0 * f[:, 1] - 16.0
    a = 500.0 * (f[:, 0] - f[:, 1])
    b = 200.0 * (f[:, 1] - f[:, 2])
    return np.stack([L, a, b], axis=-1)


def lab_to_rgb(lab: np.ndarray) -> np.ndarray:
    L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
    fy = (L + 16.0) / 116.0
    fx = a / 500.0 + fy
    fz = fy - b / 200.0
    epsilon, kappa = 0.008856, 903.3
    x = np.where(fx ** 3 > epsilon, fx ** 3, (116.0 * fx - 16.0) / kappa)
    y = np.where(L > kappa * epsilon, ((L + 16.0) / 116.0) ** 3, L / kappa)
    z = np.where(fz ** 3 > epsilon, fz ** 3, (116.0 * fz - 16.0) / kappa)
    x *= 0.95047
    z *= 1.08883
    xyz = np.stack([x, y, z], axis=-1)
    mat_inv = np.array([
        [3.2404542, -1.5371385, -0.4985314],
        [-0.9692660, 1.8760108,  0.0415560],
        [0.0556434, -0.2040259,  1.0572252],
    ])
    rgb_linear = xyz @ mat_inv.T
    rgb_linear = np.clip(rgb_linear, 0, None)
    mask = rgb_linear > 0.0031308
    rgb = np.where(mask, 1.055 * (rgb_linear ** (1.0 / 2.4)) - 0.055, 12.92 * rgb_linear)
    return np.clip(rgb, 0, 1)


def extract_dominant_colors(pixels, k=6, iterations=20):
    np.random.seed(42)
    indices = np.random.choice(len(pixels), k, replace=False)
    centers = pixels[indices].copy()
    labels = np.zeros(len(pixels), dtype=int)
    for _ in range(iterations):
        dists = np.linalg.norm(pixels[:, None] - centers[None, :], axis=2)
        labels = dists.argmin(axis=1)
        for j in range(k):
            m = labels == j
            if m.any():
                centers[j] = pixels[m].mean(axis=0)
    _, counts = np.unique(labels, return_counts=True)
    order = np.argsort(-counts)
    return centers[order]


def analyze_image(img: Image.Image) -> dict:
    img_resized = img.resize((512, 512)).convert("RGB")
    pixels = np.array(img_resized).reshape(-1, 3).astype(np.float64) / 255.0
    lab = rgb_to_lab(pixels)
    dominant = extract_dominant_colors(pixels, k=6)
    histograms = {}
    for i, ch in enumerate(["R", "G", "B"]):
        hist, _ = np.histogram(pixels[:, i], bins=64, range=(0, 1))
        histograms[ch] = hist
    luminance = 0.2126 * pixels[:, 0] + 0.7152 * pixels[:, 1] + 0.0722 * pixels[:, 2]
    return {
        "lab_mean": lab.mean(axis=0),
        "lab_std": lab.std(axis=0),
        "rgb_mean": pixels.mean(axis=0),
        "rgb_std": pixels.std(axis=0),
        "dominant_colors": dominant,
        "histograms": histograms,
        "luminance_stats": {
            "mean": float(luminance.mean()),
            "shadows_pct": float((luminance < 0.25).mean() * 100),
            "midtones_pct": float(((luminance >= 0.25) & (luminance < 0.75)).mean() * 100),
            "highlights_pct": float((luminance >= 0.75).mean() * 100),
        },
    }


def _transfer(lab, src_stats, ref_stats, strength, preserve_luminance):
    """소스 이미지의 실제 색 분포(src)를 레퍼런스(ref) 분포로 맞추는 LAB Reinhard 변환."""
    ref_mean, ref_std = ref_stats["lab_mean"], ref_stats["lab_std"]
    src_mean, src_std = src_stats["lab_mean"], src_stats["lab_std"]
    out = lab.copy()
    # L(밝기): 소스→레퍼런스로 매칭하되, 밝기 보존값만큼 원본 밝기 유지
    l_ratio = ref_std[0] / max(src_std[0], 1e-6)
    out[:, 0] = (lab[:, 0] - src_mean[0]) * l_ratio + ref_mean[0]
    out[:, 0] = lab[:, 0] * preserve_luminance + out[:, 0] * (1 - preserve_luminance)
    # a,b(색): 소스→레퍼런스 색감 매칭
    for ch in [1, 2]:
        ratio = ref_std[ch] / max(src_std[ch], 1e-6)
        out[:, ch] = (lab[:, ch] - src_mean[ch]) * ratio + ref_mean[ch]
    return lab * (1 - strength) + out * strength


def generate_cube_lut(src_stats, ref_stats, lut_size=33, strength=1.0, preserve_luminance=0.5) -> str:
    grid = np.linspace(0, 1, lut_size)
    # .cube 규격: RED가 가장 빠르게, BLUE가 가장 느리게 변하는 순서로 데이터를 나열해야 한다.
    # meshgrid를 (b, g, r) 순으로 만들고 C-order로 평탄화하면 R이 가장 빠르게 변한다.
    b, g, r = np.meshgrid(grid, grid, grid, indexing="ij")
    rgb_grid = np.stack([r.ravel(), g.ravel(), b.ravel()], axis=-1)
    lab_grid = rgb_to_lab(rgb_grid)
    blended = _transfer(lab_grid, src_stats, ref_stats, strength, preserve_luminance)
    output_rgb = np.clip(lab_to_rgb(blended), 0, 1)
    lines = [
        "# Generated by Lumina Grade — Source→Reference Color Match LUT",
        f"# Strength: {strength:.0%}, Luminance Preserve: {preserve_luminance:.0%}",
        'TITLE "Lumina Color Match"',
        f"LUT_3D_SIZE {lut_size}",
        "DOMAIN_MIN 0.0 0.0 0.0",
        "DOMAIN_MAX 1.0 1.0 1.0",
        "",
    ]
    for i in range(len(output_rgb)):
        rr, gg, bb = output_rgb[i]
        lines.append(f"{rr:.6f} {gg:.6f} {bb:.6f}")
    return "\n".join(lines)


def generate_preview(img, src_stats, ref_stats, strength, preserve_luminance, max_side=1600) -> Image.Image:
    img_resized = img.copy()
    # 화면 표시용으로 충분히 선명한 해상도까지만 축소 (원본과 나란히 봐도 흐리지 않게)
    if max(img_resized.size) > max_side:
        ratio = max_side / max(img_resized.size)
        img_resized = img_resized.resize(
            (int(img_resized.width * ratio), int(img_resized.height * ratio)), Image.LANCZOS)
    pixels = np.array(img_resized.convert("RGB")).astype(np.float64) / 255.0
    shape = pixels.shape
    lab = rgb_to_lab(pixels.reshape(-1, 3))
    blended = _transfer(lab, src_stats, ref_stats, strength, preserve_luminance)
    out = (np.clip(lab_to_rgb(blended).reshape(shape), 0, 1) * 255).astype(np.uint8)
    return Image.fromarray(out)


# ════════════════════════════════════════════════════════════
#  SIDEBAR = INSPECTOR
# ════════════════════════════════════════════════════════════
# 프리셋 한글 라벨 (여러 곳에서 재사용)
LOOK_LABELS = {
    "None": "없음 (None)",
    "Teal & Orange": "틸 & 오렌지 (시네마틱)",
    "Joker": "조커 (그린-옐로우 시네마)",
    "Warm Film": "웜 필름 (따뜻한 필름)",
    "Cool Blue": "쿨 블루 (차가운 톤)",
    "Noir Silver": "느와르 실버 (흑백톤)",
    "Vintage": "빈티지 (바랜 필름)",
    "Cyberpunk": "사이버펑크 (네온)",
    "Sepia": "세피아 (갈색 톤)",
    "Bleach Bypass": "블리치 바이패스 (고대비)",
}

# 설정 기본값 + 초기화
SETTING_DEFAULTS = {
    "lut_size": 33,
    "strength": 0.85,
    "preserve_luminance": 0.6,
    "look": "None",
}
for _k, _v in SETTING_DEFAULTS.items():
    st.session_state.setdefault(_k, _v)


def reset_settings():
    for k, v in SETTING_DEFAULTS.items():
        st.session_state[k] = v


def reset_one(key):
    st.session_state[key] = SETTING_DEFAULTS[key]


with st.sidebar:
    st.markdown("""
    <div style="display: flex; flex-direction: column; padding: 12px 16px; border-bottom: 1px solid #2d333b; background: #111111; margin: 0 -8px 0 -8px;">
        <span style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; font-weight: bold; color: #ffffff;">Studio A</span>
        <span style="font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #8b949e; text-transform: uppercase; margin-top: 2px; letter-spacing: 0.05em;">Rec.709 Project</span>
    </div>
    <div style="display: flex; align-items: center; gap: 8px; padding: 10px 16px; border-bottom: 1px solid #2d333b; background: #151515; margin: 0 -8px 16px -8px;">
        <span class="material-symbols-outlined" style="font-size: 16px; color: #8b949e;">folder</span>
        <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #e5e2e1; text-transform: uppercase; letter-spacing: 0.05em;">Library</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <span class="sec-head primary" style="margin: 0 !important; font-size: 10px !important;">Exposure Control</span>
        <span style="font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #00a3ff; font-weight: bold; cursor: pointer; letter-spacing: 0.05em;">AUTO</span>
    </div>
    """, unsafe_allow_html=True)
    
    # LUT 해상도 + 개별 초기화
    sc1, sc2 = st.columns([5, 1])
    with sc1:
        lut_size = st.select_slider(
            "LUT 해상도 (Resolution)",
            options=[17, 25, 33, 49, 65], key="lut_size",
            help="LUT의 격자 정밀도입니다. 높을수록 색 표현이 정밀하지만 파일이 커집니다. 33이 업계 표준입니다.",
        )
    with sc2:
        st.markdown('<div style="height:26px"></div>', unsafe_allow_html=True)
        st.button("↺", key="rst_lut", on_click=reset_one, args=("lut_size",),
                  help="LUT 해상도만 초기화", use_container_width=True)

    # 색 전이 강도 + 개별 초기화
    sc1, sc2 = st.columns([5, 1])
    with sc1:
        strength = st.slider(
            "색 전이 강도 (Strength)", 0.0, 1.0, step=0.05, key="strength",
            help="레퍼런스 이미지의 색감을 얼마나 강하게 입힐지 결정합니다. 1에 가까울수록 원본 색감을 강하게 따라갑니다.",
        )
    with sc2:
        st.markdown('<div style="height:26px"></div>', unsafe_allow_html=True)
        st.button("↺", key="rst_str", on_click=reset_one, args=("strength",),
                  help="색 전이 강도만 초기화", use_container_width=True)

    # 밝기 보존 + 개별 초기화
    sc1, sc2 = st.columns([5, 1])
    with sc1:
        preserve_luminance = st.slider(
            "밝기 보존 (Luminance)", 0.0, 1.0, step=0.05, key="preserve_luminance",
            help="원본 영상의 밝기(노출)를 얼마나 유지할지 결정합니다. 높을수록 색만 바뀌고 밝기는 원본을 유지합니다.",
        )
    with sc2:
        st.markdown('<div style="height:26px"></div>', unsafe_allow_html=True)
        st.button("↺", key="rst_lum", on_click=reset_one, args=("preserve_luminance",),
                  help="밝기 보존만 초기화", use_container_width=True)

    # 수치 조절 바로 아래 — 전체 초기화
    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    st.button("↺  전체 설정 초기화 (Reset All)", on_click=reset_settings, use_container_width=True)

    st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-head secondary">Film Emulation (Preset)</div>', unsafe_allow_html=True)
    look = st.selectbox(
        "Creative Preset",
        ["None", "Teal & Orange", "Joker", "Warm Film", "Cool Blue",
         "Noir Silver", "Vintage", "Cyberpunk", "Sepia", "Bleach Bypass"],
        format_func=lambda x: LOOK_LABELS[x],
        key="look",
        label_visibility="collapsed",
    )
    st.button("↺  템플릿 초기화", key="rst_look", on_click=reset_one, args=("look",),
              use_container_width=True)



    st.markdown("""
    <div style="height:12px"></div>
    <div class="sec-head muted" style="font-size: 9px !important;">◈ 적용 순서 · HOW TO APPLY</div>
    <div style="font-size:11px; color:#8b949e; line-height:1.75; font-family:'JetBrains Mono', 'Inter', sans-serif; padding-left: 2px;">
    1. 레퍼런스 + 소스 2장 업로드<br>
    2. 설정 조정 → 결과 확인<br>
    3. LUT 생성 → .cube 다운로드<br>
    4. 편집 프로그램에 LUT 적용<br>
    &nbsp;&nbsp;&nbsp;(Resolve · Premiere · AE 등)
    </div>
    """, unsafe_allow_html=True)



def apply_creative_look(stats, look):
    """Adjust target LAB stats based on creative preset.
    LAB: mean[0]=밝기, mean[1]=a(녹↔적), mean[2]=b(청↔황), std=채도/대비.
    """
    s = dict(stats)
    mean = stats["lab_mean"].copy()
    std = stats["lab_std"].copy()
    if look == "Teal & Orange":          # 시네마틱: 청록 그림자 + 주황 인물
        mean[1] += 4; mean[2] += 6; std[1] *= 1.15; std[2] *= 1.15
    elif look == "Joker":                # 조커: 병약한 그린-옐로우 + 따뜻한 하이라이트
        mean[1] -= 5; mean[2] += 7; std[0] *= 1.05; std[1] *= 0.9; std[2] *= 1.05
    elif look == "Warm Film":            # 따뜻한 필름
        mean[2] += 10; mean[1] += 3
    elif look == "Cool Blue":            # 차가운 시네마톤
        mean[2] -= 11; mean[1] -= 2; std[2] *= 1.05
    elif look == "Noir Silver":          # 흑백/모노톤
        std[1] *= 0.25; std[2] *= 0.25; mean[1] *= 0.2; mean[2] *= 0.2
    elif look == "Vintage":              # 바랜 레트로 필름
        mean[2] += 7; mean[1] += 4; std[0] *= 0.95; std[1] *= 0.8; std[2] *= 0.8
    elif look == "Cyberpunk":            # 네온: 고채도 마젠타+시안
        mean[1] += 4; mean[2] -= 5; std[0] *= 1.05; std[1] *= 1.35; std[2] *= 1.3
    elif look == "Sepia":                # 갈색 단색조
        mean[1] = mean[1] * 0.2 + 8; mean[2] = mean[2] * 0.2 + 20
        std[1] *= 0.3; std[2] *= 0.35
    elif look == "Bleach Bypass":        # 탈색 고대비 (채도↓ 대비↑)
        std[1] *= 0.4; std[2] *= 0.4; mean[1] *= 0.5; mean[2] *= 0.5; std[0] *= 1.2
    s["lab_mean"] = mean
    s["lab_std"] = std
    return s


# ── 캐싱: 슬라이더 조작 시 재계산/깜박임 방지 ──
@st.cache_data(show_spinner=False)
def get_analysis(file_bytes):
    """파일 내용 기준으로 1회만 분석 (슬라이더와 무관 → 매번 재계산 안 함)."""
    img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    return analyze_image(img)


@st.cache_data(show_spinner=False)
def get_preview(src_bytes, ref_bytes, look, strength, preserve_luminance):
    """소스 이미지를 (레퍼런스+템플릿) 색감으로 매칭한 결과(화면용, 최대 1600px). 캐시."""
    src_img = Image.open(io.BytesIO(src_bytes)).convert("RGB")
    src_stats = get_analysis(src_bytes)
    target_stats = apply_creative_look(get_analysis(ref_bytes), look)
    return generate_preview(src_img, src_stats, target_stats, strength, preserve_luminance)


@st.cache_data(show_spinner=False)
def get_result_fullres(src_bytes, ref_bytes, look, strength, preserve_luminance):
    """소스 이미지 '원본 해상도 그대로' 룩을 적용한 결과 (다운로드용). 캐시."""
    src_img = Image.open(io.BytesIO(src_bytes)).convert("RGB")
    src_stats = get_analysis(src_bytes)
    target_stats = apply_creative_look(get_analysis(ref_bytes), look)
    # max_side를 크게 줘서 축소 없이 원본 해상도로 처리
    return generate_preview(src_img, src_stats, target_stats, strength, preserve_luminance, max_side=100000)


# ════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════

# ── 도움말 (Help) ──
with st.expander("📖  도움말 · 전체 사용 설명서 (Help & Guide)", expanded=False):
    st.markdown("""
    <div class="help-p">
    <div class="help-h">🎬 이 프로그램은 무엇인가요?</div>
    이미지의 색감을 분석해 <b>업계 표준 .cube LUT</b>과 <b>원본화질 결과 이미지</b>를 만들어 줍니다.
    두 가지 방식으로 쓸 수 있어요:<br>
    &nbsp;&nbsp;<b style="color:var(--primary)">① 색 매칭</b> — 레퍼런스(원하는 색감)+소스(내 이미지) 2장을 올리면, 소스를 레퍼런스 색감에 맞춰줍니다.<br>
    &nbsp;&nbsp;<b style="color:var(--secondary)">② 프리셋만</b> — 소스 1장만 올리고 'Film Emulation' 프리셋(조커·틸&오렌지 등)을 고르면, 레퍼런스 없이 바로 영화 룩을 입힙니다.<br>
    <b style="color:var(--primary)">.cube는 표준 포맷이라 DaVinci Resolve뿐 아니라 Premiere Pro · After Effects · Final Cut Pro · Photoshop 등에서 모두 사용할 수 있습니다.</b><br>
    <span style="color:var(--outline)">※ LUT(Look-Up Table): 입력 색을 출력 색으로 바꿔주는 색 변환표. 색보정 프리셋이라고 생각하면 됩니다.</span>

    <div class="help-h">🚀 사용 순서</div>
    <b>방법 A — 색 매칭 (2장):</b><br>
    &nbsp;&nbsp;1. 왼쪽 칸에 <b>레퍼런스</b>(원하는 색감) 업로드<br>
    &nbsp;&nbsp;2. 오른쪽 칸에 <b>소스</b>(색 바꿀 내 이미지) 업로드 → 자동 매칭<br>
    <b>방법 B — 프리셋만 (1장):</b><br>
    &nbsp;&nbsp;1. <b>소스</b>만 업로드 (이미지가 바로 표시됩니다)<br>
    &nbsp;&nbsp;2. 왼쪽 <b>Film Emulation 프리셋</b> 선택 → 결과가 나타남<br>
    <b>공통 — 조정 & 추출:</b> 강도·밝기 슬라이더로 미세 조정 → 아래 <b>'.cube LUT 생성'</b> 또는 <b>'원본화질 이미지 추출'</b>로 다운로드

    <div class="help-h">⚙️ 왼쪽 설정(인스펙터) 설명</div>
    <b>· LUT 해상도 (Resolution):</b> 색 변환표의 격자 정밀도. 33이 표준이며 대부분 충분합니다. 49·65는 더 정밀하지만 파일이 커집니다.<br>
    <b>· 색 전이 강도 (Strength):</b> 색감을 얼마나 세게 입힐지. 낮추면 은은하게, 높이면 강하게 적용됩니다.<br>
    <b>· 밝기 보존 (Luminance):</b> 원본 영상의 밝기를 얼마나 지킬지. 높이면 밝기는 그대로 두고 색만 바뀝니다.<br>
    <b>· 설정 초기화:</b> 각 슬라이더 옆 ↺로 개별 초기화, '전체 설정 초기화'로 한 번에 되돌릴 수 있습니다.

    <div class="help-h">🎞️ Film Emulation 프리셋 (10종)</div>
    소스(또는 레퍼런스) 색감 위에 추가로 입히는 영화 무드입니다. 레퍼런스 없이 단독으로도 적용됩니다.<br>
    <b>· 없음</b>: 변형 없음 &nbsp; <b>· 틸 & 오렌지</b>: 청록 그림자 + 주황 인물(시네마틱)<br>
    <b>· 조커</b>: 병약한 그린-옐로우 + 따뜻한 하이라이트 — 영화 〈조커〉 색감<br>
    <b>· 웜 필름</b>: 따뜻한 노란 필름 &nbsp; <b>· 쿨 블루</b>: 차가운 파란 톤<br>
    <b>· 느와르 실버</b>: 흑백/모노톤 &nbsp; <b>· 빈티지</b>: 바랜 레트로 필름<br>
    <b>· 사이버펑크</b>: 고채도 네온(마젠타+시안) &nbsp; <b>· 세피아</b>: 갈색 단색조<br>
    <b>· 블리치 바이패스</b>: 탈색 + 강한 대비

    <div class="help-h">💾 내보내기 (2가지)</div>
    <b>· .cube LUT 생성:</b> 색 변환표 파일. 영상 편집 프로그램에 적용해 영상 전체를 같은 색으로 보정합니다.<br>
    <b>· 원본화질 이미지 추출:</b> 소스 <b>원본 해상도 그대로</b> 룩을 적용한 PNG를 바로 받습니다. (사진 한 장만 보정할 때 편리)

    <div class="help-h">📊 분석 결과 읽는 법</div>
    <b>· 주요 색상 (Palette):</b> 이미지에서 가장 많이 쓰인 대표 색들.<br>
    <b>· 톤 분포:</b> 어두운 영역(섀도)·중간(미드톤)·밝은 영역(하이라이트)의 비율.<br>
    <b>· 색온도/틴트:</b> 따뜻함(Warm)·차가움(Cool), 마젠타·그린 치우침 정도.<br>
    <b>· RGB 히스토그램:</b> 빨강·초록·파랑 각 채널의 밝기 분포 그래프.

    <div class="help-h">🎞️ DaVinci Resolve에 적용하는 방법</div>
    <b>A. Color 페이지에서 바로:</b> Color 탭 → 노드에서 우클릭 → <b>LUTs</b> → 다운받은 .cube 선택<br>
    <b>B. 프로젝트 설정:</b> File → Project Settings → Color Management → 3D Lookup Table에서 선택<br>
    <b>C. LUT 폴더에 복사 후 사용:</b> .cube 파일을 아래 폴더에 넣고 Resolve 재시작<br>
    &nbsp;&nbsp;<span style="color:var(--outline)">macOS: /Library/Application Support/Blackmagic Design/DaVinci Resolve/LUT/</span><br>
    &nbsp;&nbsp;<span style="color:var(--outline)">Windows: C:\\ProgramData\\Blackmagic Design\\DaVinci Resolve\\Support\\LUT\\</span>

    <div class="help-h">🅰️ Adobe Premiere Pro에 적용하는 방법</div>
    <b>1.</b> 클립 선택 → 상단 <b>Lumetri 색상(Lumetri Color)</b> 패널 열기<br>
    <b>2.</b> <b>기본 교정(Basic Correction)</b> → 입력 LUT → <b>찾아보기(Browse)</b> → .cube 선택<br>
    &nbsp;&nbsp;또는 <b>크리에이티브(Creative)</b> → Look → 찾아보기 (이쪽은 강도 슬라이더로 세기 조절 가능)<br>
    <span style="color:var(--outline)">※ After Effects: Lumetri Color 또는 'Apply Color LUT' 이펙트 / Final Cut Pro: Custom LUT 이펙트 / Photoshop: 색상 조회(Color Lookup) 조정 레이어</span>

    <div class="help-h">💡 팁</div>
    · 색 매칭 시 레퍼런스와 소스의 노출이 비슷할수록 결과가 자연스럽습니다.<br>
    · 색감이 과하면 '색 전이 강도'를 낮춰보세요.<br>
    · 사진 한 장만 빠르게 보정하려면 소스만 올리고 프리셋을 고른 뒤 '원본화질 이미지 추출'을 쓰세요.<br>
    · 적용 후 Resolve/Premiere에서 노드·클립의 불투명도로 LUT 세기를 미세 조정할 수 있습니다.
    </div>
    """, unsafe_allow_html=True)

def _temp_tint(lab_m):
    if lab_m[2] > 10:
        temp = "Warm 🟡"
    elif lab_m[2] < -10:
        temp = "Cool 🔵"
    else:
        temp = "Neutral ⚪"
    tint = "Magenta" if lab_m[1] > 5 else ("Green" if lab_m[1] < -5 else "Neutral")
    return temp, tint


# ── 업로드: ① 레퍼런스(원하는 색감) ② 소스(색 바꿀 내 이미지) ──
up1, up2 = st.columns(2)
with up1:
    st.markdown('<div class="sec-head primary">◈ 1. 레퍼런스 (원하는 색감) · REFERENCE</div>', unsafe_allow_html=True)
    ref_file = st.file_uploader(
        "reference", type=["jpg", "jpeg", "png", "tiff", "bmp", "webp"],
        key="ref_up", label_visibility="collapsed",
    )
with up2:
    st.markdown('<div class="sec-head secondary">◈ 2. 소스 (색 바꿀 내 이미지) · SOURCE</div>', unsafe_allow_html=True)
    src_file = st.file_uploader(
        "source", type=["jpg", "jpeg", "png", "tiff", "bmp", "webp"],
        key="src_up", label_visibility="collapsed",
    )

if src_file and (ref_file or look != "None"):
    with st.spinner("🎨 이미지 분석 · 색 적용 중..."):
        src_bytes = src_file.getvalue()
        src_img = Image.open(io.BytesIO(src_bytes)).convert("RGB")
        src_stats = get_analysis(src_bytes)

        preset_only = ref_file is None       # 레퍼런스 없이 프리셋만 적용하는 모드
        if preset_only:
            ref_bytes = src_bytes            # 소스 자신을 기준으로 프리셋 적용
            ref_img = None
            ref_stats = src_stats
        else:
            ref_bytes = ref_file.getvalue()
            ref_img = Image.open(io.BytesIO(ref_bytes)).convert("RGB")
            ref_stats = get_analysis(ref_bytes)

        target_stats = apply_creative_look(ref_stats, look)
        result = get_preview(src_bytes, ref_bytes, look, strength, preserve_luminance)
        result_stats = analyze_image(result)

    src_temp, _ = _temp_tint(src_stats["lab_mean"])
    res_temp, res_tint = _temp_tint(result_stats["lab_mean"])
    look_label = LOOK_LABELS.get(look, look)

    # ── 색상 팔레트 헬퍼 ──
    def _swatch_html(stats_obj):
        html = ""
        for c in stats_obj["dominant_colors"]:
            hexc = "#{:02x}{:02x}{:02x}".format(int(c[0] * 255), int(c[1] * 255), int(c[2] * 255))
            html += f'<div class="swatch" style="background:{hexc}" title="{hexc}"></div>'
        return f'<div class="swatch-row">{html}</div>'

    def _pane(title, title_cls, img, pal_stats_obj, pal_label):
        st.markdown(f'<div class="sec-head {title_cls}">{title}</div>', unsafe_allow_html=True)
        st.image(img, use_container_width=True)
        st.markdown(
            f'<div class="sec-head {title_cls}" style="font-size:10px; margin-top:8px;">{pal_label}</div>',
            unsafe_allow_html=True)
        st.markdown(_swatch_html(pal_stats_obj), unsafe_allow_html=True)

    # ── 미리보기 (각 이미지 아래에 주요 색상 팔레트) ──
    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
    if preset_only:
        c1, c2 = st.columns(2)
        with c1:
            _pane("소스 (원본)", "muted", src_img, src_stats, "소스 주요 색상")
        with c2:
            _pane("✦ 결과 (프리셋 적용)", "primary", result, result_stats, "결과 주요 색상")
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            _pane("레퍼런스 (목표)", "muted", ref_img, ref_stats, "레퍼런스 주요 색상")
        with c2:
            _pane("소스 (원본)", "muted", src_img, src_stats, "소스 주요 색상")
        with c3:
            _pane("✦ 결과 (색 매칭됨)", "primary", result, result_stats, "결과 주요 색상")

    # ── 메타데이터 ──
    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    if preset_only:
        match_pct = None
        meta = [
            (m1, "소스 색온도", src_temp),
            (m2, "결과 색온도", res_temp),
            (m3, "적용 프리셋", look_label.split(" (")[0]),
            (m4, "LUT 크기 · Size", f"{lut_size}³ = {lut_size**3:,}"),
        ]
    else:
        ab_src = src_stats["lab_mean"][1:]
        ab_ref = target_stats["lab_mean"][1:]
        ab_res = result_stats["lab_mean"][1:]
        gap0 = np.linalg.norm(ab_ref - ab_src) + 1e-6
        gap1 = np.linalg.norm(ab_ref - ab_res)
        match_pct = float(np.clip((1 - gap1 / gap0) * 100, 0, 100))
        ref_temp, _ = _temp_tint(target_stats["lab_mean"])
        meta = [
            (m1, "레퍼런스 색온도", ref_temp),
            (m2, "소스 색온도", src_temp),
            (m3, "결과 색온도", res_temp),
            (m4, "색 매칭도 · Match", f"{match_pct:.0f}%"),
        ]
    for col, label, value in meta:
        with col:
            st.markdown(
                f'<div class="meta-cell"><span class="meta-label">{label}</span>'
                f'<span class="meta-value">{value}</span></div>',
                unsafe_allow_html=True,
            )

    # ── 태그 ──
    pal_stats = ref_stats          # preset_only이면 ref_stats == src_stats
    hist_title = "소스 RGB 히스토그램" if preset_only else "레퍼런스 RGB 히스토그램"
    st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
    mode_tag = "Preset" if preset_only else "Color Match"
    tags = [mode_tag, f"LUT{lut_size}", res_temp.split()[0], res_tint]
    if look != "None":
        tags.append(look)
    tag_html = "".join(f'<span class="tag{" accent" if t in [mode_tag, look] else ""}">{t}</span>' for t in tags)
    st.markdown('<div class="sec-head muted">◈ 태그 · TAGS</div>', unsafe_allow_html=True)
    st.markdown(f'<div>{tag_html}</div>', unsafe_allow_html=True)

    # ── RGB 히스토그램 (가로 3개 R | G | B) ──
    st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sec-head primary">◈ {hist_title}</div>', unsafe_allow_html=True)
    h1, h2, h3 = st.columns(3)
    for col, ch, color in zip([h1, h2, h3], ["R", "G", "B"], ["#ff6b6b", "#51cf66", "#74c0fc"]):
        with col:
            st.markdown(
                f'<div style="font-size:11px; color:var(--outline); font-family:Inter">{ch} 채널 (Channel)</div>',
                unsafe_allow_html=True)
            st.bar_chart(pal_stats["histograms"][ch], color=color, height=150)

    # ── 내보내기 ──
    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-head primary">◈ 내보내기 · EXPORT</div>', unsafe_allow_html=True)
    src_w, src_h = src_img.size
    g1, g2, g3 = st.columns(3)
    with g1:
        filename = st.text_input(
            "File name", value=f"lumina_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            label_visibility="collapsed",
        )
    with g2:
        gen = st.button("✦  .cube LUT 생성", type="primary", use_container_width=True)
    with g3:
        gen_img = st.button(f"🖼  원본화질 이미지 추출", use_container_width=True,
                            help=f"소스 원본 해상도({src_w}×{src_h})로 룩을 적용해 PNG로 추출합니다.")

    _sfx = f"· 색 매칭도 {match_pct:.0f}%" if match_pct is not None else f"· 프리셋 {look_label.split(' (')[0]}"
    if gen_img:
        with st.spinner(f"원본 해상도({src_w}×{src_h})로 룩 적용 중..."):
            full_result = get_result_fullres(src_bytes, ref_bytes, look, strength, preserve_luminance)
            buf_full = io.BytesIO(); full_result.save(buf_full, format="PNG")
        st.success(f"원본화질 이미지 추출 완료 — {full_result.width}×{full_result.height} {_sfx}")
        st.download_button(
            f"⬇  원본화질 결과 이미지 다운로드 ({full_result.width}×{full_result.height} PNG)",
            data=buf_full.getvalue(),
            file_name=f"{filename}_graded_{full_result.width}x{full_result.height}.png",
            mime="image/png", use_container_width=True, type="primary",
        )

    if gen:
        with st.spinner(f"{lut_size}³ LUT 생성 중..."):
            cube = generate_cube_lut(src_stats, target_stats, lut_size, strength, preserve_luminance)
        st.success(f"LUT 생성 완료 — {lut_size}³ = {lut_size**3:,} 포인트 {_sfx}")
        d1, d2 = st.columns(2)
        with d1:
            st.download_button(
                "⬇  .cube LUT 다운로드", data=cube,
                file_name=f"{filename}.cube", mime="text/plain",
                use_container_width=True,
            )
        with d2:
            buf_full2 = io.BytesIO()
            get_result_fullres(src_bytes, ref_bytes, look, strength, preserve_luminance).save(buf_full2, format="PNG")
            st.download_button(
                "🖼  원본화질 결과 이미지 다운로드", data=buf_full2.getvalue(),
                file_name=f"{filename}_graded.png", mime="image/png",
                use_container_width=True,
            )
        st.markdown("""
        <div class="panel" style="margin-top:14px;">
            <div style="font-size:13px; color:var(--on-variant); line-height:1.85;
                 font-family:'Inter','Pretendard',sans-serif;">
            <b style="color:var(--primary); font-size:14px;">🎞️ 적용 방법 (.cube는 여러 프로그램 공용)</b><br><br>
            <b>DaVinci Resolve:</b> Color 페이지 → 노드 우클릭 → <b>LUTs</b> → 다운받은 .cube 선택<br>
            <b>Premiere Pro:</b> Lumetri 색상 → 기본 교정/크리에이티브 → 입력 LUT → <b>찾아보기</b> → .cube 선택<br>
            <b>After Effects:</b> Lumetri Color 또는 'Apply Color LUT' 이펙트<br>
            <b>Final Cut Pro:</b> Custom LUT 이펙트 &nbsp;·&nbsp; <b>Photoshop:</b> 색상 조회(Color Lookup) 레이어<br>
            <span style="color:var(--outline)">자세한 단계는 위쪽 📖 도움말 참고</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif ref_file and not src_file:
    st.info("레퍼런스만 올렸습니다. **소스 이미지**(색을 바꿀 내 이미지)를 올리면 색 매칭이 시작됩니다.")

elif src_file and look == "None":
    # 소스만 업로드(레퍼런스·프리셋 없음) — 소스 이미지를 바로 보여주고 안내
    src_bytes = src_file.getvalue()
    src_img = Image.open(io.BytesIO(src_bytes)).convert("RGB")
    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-head primary">소스 이미지 (원본)</div>', unsafe_allow_html=True)
    st.image(src_img, use_container_width=True)
    st.info("👉 왼쪽 **Film Emulation 프리셋**(틸&오렌지·조커 등)을 고르거나 **레퍼런스 이미지**를 추가로 올리면, "
            "색이 적용된 결과가 여기에 표시됩니다.")

else:
    # ── Landing ──
    st.markdown("""
    <div style="text-align: center; padding: 64px 32px; border: 1px solid #2d333b; background: #111111; border-radius: 2px; margin-top: 16px;">
        <div style="font-size: 48px; margin-bottom: 16px; opacity: 0.85;">🎬</div>
        <div style="color: #00a3ff; font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: bold; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 12px;">
            레퍼런스 + 소스 → 색 매칭 LUT
        </div>
        <div style="color: #8b949e; font-size: 13px; line-height: 1.8; max-width: 560px; margin: 0 auto; font-family: 'Inter', sans-serif;">
            ① <b>레퍼런스</b>(원하는 색감)와 ② <b>소스</b>(색 바꿀 내 이미지)를 올리면,<br>
            소스를 레퍼런스 색감에 최대한 맞춘 뒤 그 변환을 <b>.cube LUT</b>으로 추출합니다.<br>
            DaVinci Resolve · Premiere Pro · After Effects · Final Cut · Photoshop 등에서 사용 가능.<br>
            <span style="color: #444c56; font-size: 11px;">처음이라면 위의 <b>도움말</b>을 먼저 펼쳐보세요.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
