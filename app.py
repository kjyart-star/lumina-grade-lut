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

# ════════════════════════════════════════════════════════════
#  THEME / CSS — "Lumina Grade" professional dark UI
# ════════════════════════════════════════════════════════════
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" rel="stylesheet">
<style>
    :root {
        --bg: #131313;
        --surface: #201f1f;
        --surface-high: #2a2a2a;
        --surface-highest: #353534;
        --surface-low: #1c1b1b;
        --surface-lowest: #0e0e0e;
        --primary: #98cbff;
        --secondary: #ffb77f;
        --on-surface: #e5e2e1;
        --on-variant: #bec7d4;
        --outline: #88919d;
        --outline-variant: #3f4852;
        --primary-container: #00a3ff;
    }

    /* ── 전역 ── */
    .stApp { background: var(--bg); }
    html, body, [class*="css"] {
        font-family: 'Pretendard', 'Inter', -apple-system, sans-serif;
    }
    /* Material 아이콘 폰트는 절대 덮어쓰지 않음 (아이콘 깨짐 방지) */
    [data-testid="stIconMaterial"], .material-symbols-outlined, .material-symbols-rounded {
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined' !important;
    }
    footer, #MainMenu { visibility: hidden; height: 0; }
    /* 헤더/툴바 전체 숨김 (배포·메뉴 버튼 제거) */
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stToolbar"], [data-testid="stAppToolbar"] { display: none !important; }
    /* 사이드바 접기 기능 제거 — 접기 버튼 숨김 + 항상 펼친 상태로 강제 */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stSidebar"] {
        min-width: 300px !important; width: 300px !important;
        transform: translateX(0) !important; visibility: visible !important;
        margin-left: 0 !important;
    }
    [data-testid="stSidebar"][aria-expanded="false"] { transform: translateX(0) !important; }
    .block-container { padding: 1rem 1.5rem 2rem 1.5rem; max-width: 100%; }

    .mono { font-family: 'JetBrains Mono', 'Pretendard', sans-serif; letter-spacing: 0.05em; }

    /* ── Top bar ── */
    .lumina-topbar {
        display: flex; align-items: center; justify-content: space-between;
        height: 56px; margin: 0 -1.5rem 1rem -1.5rem; padding: 0 1.5rem;
        background: var(--surface); border-bottom: 1px solid var(--outline-variant);
        container-type: inline-size; gap: 16px; overflow: hidden;
    }
    .lumina-brand {
        font-size: 22px; font-weight: 700; color: var(--primary);
        font-family: 'Inter', sans-serif; letter-spacing: -0.01em;
        white-space: nowrap; flex-shrink: 0;
    }
    .lumina-subtitle {
        font-size: 12px; color: var(--outline); white-space: nowrap;
        overflow: hidden; text-overflow: ellipsis;
    }
    @container (max-width: 520px) { .lumina-subtitle { display: none !important; } }

    /* ── Section header (mono uppercase) ── */
    .sec-head {
        display: flex; align-items: center; gap: 8px;
        font-family: 'JetBrains Mono', 'Pretendard', sans-serif; text-transform: uppercase;
        letter-spacing: 0.12em; font-size: 11px; font-weight: 500;
        margin: 4px 0 2px 0;
    }
    .sec-head.primary { color: var(--primary); }
    .sec-head.secondary { color: var(--secondary); }
    .sec-head.muted { color: var(--outline); }

    /* ── Sidebar = Inspector ── */
    [data-testid="stSidebar"] {
        background: var(--surface-low);
        border-right: 1px solid var(--outline-variant);
    }
    [data-testid="stSidebar"] > div { padding-top: 1rem; }
    .inspector-title {
        font-size: 18px; font-weight: 600; color: var(--on-surface);
        padding: 8px 4px 12px 4px; border-bottom: 1px solid var(--outline-variant);
        margin-bottom: 16px; display: flex; align-items: center; gap: 8px;
    }

    /* ── Sliders ── */
    [data-testid="stSidebar"] label p {
        font-family: 'Inter', 'Pretendard', sans-serif !important;
        font-size: 13px !important; font-weight: 500; color: var(--on-surface) !important;
        text-transform: none; letter-spacing: 0;
    }
    [data-testid="stSidebar"] .stRadio label p {
        font-size: 13px !important; color: var(--on-surface) !important;
    }
    [data-baseweb="slider"] [role="slider"] { background: var(--primary) !important; }

    /* ── Buttons ── */
    .stButton button, .stDownloadButton button {
        font-family: 'Inter', 'Pretendard', sans-serif; font-weight: 600;
        letter-spacing: 0.01em; border-radius: 6px; border: none; font-size: 14px;
        transition: opacity .15s, transform .05s;
    }
    .stButton button[kind="primary"], .stDownloadButton button {
        background: var(--primary-container) !important; color: #00375a !important;
        font-weight: 700;
    }
    .stButton button:hover, .stDownloadButton button:hover { opacity: .9; }
    .stButton button:active { transform: scale(.98); }

    /* ── Cards / panels ── */
    .panel {
        background: var(--surface); border: 1px solid var(--outline-variant);
        border-radius: 6px; padding: 14px 16px;
    }
    .panel-head {
        background: var(--surface-high); margin: -14px -16px 14px -16px;
        padding: 10px 16px; border-bottom: 1px solid var(--outline-variant);
        border-radius: 6px 6px 0 0; font-weight: 600; font-size: 15px;
        color: var(--on-surface);
    }

    /* ── Metadata strip ── */
    .meta-cell {
        background: var(--surface); border: 1px solid var(--outline-variant);
        border-radius: 4px; padding: 10px 12px; height: 72px;
        display: flex; flex-direction: column; justify-content: space-between;
    }
    .meta-label {
        font-family: 'Inter', 'Pretendard', sans-serif; font-size: 11px;
        letter-spacing: 0.02em; color: var(--outline);
    }
    .meta-value {
        font-family: 'JetBrains Mono', 'Pretendard', sans-serif; font-size: 14px;
        color: var(--on-surface);
    }

    /* ── Color swatches ── */
    .swatch-row { display: flex; gap: 6px; flex-wrap: wrap; }
    .swatch {
        width: 44px; height: 44px; border-radius: 4px;
        border: 1px solid var(--outline-variant);
    }

    /* ── Tags ── */
    .tag {
        display: inline-block; background: var(--surface-high);
        padding: 4px 10px; border-radius: 4px; font-size: 12px;
        font-family: 'Inter', 'Pretendard', sans-serif; color: var(--on-variant);
        margin: 2px;
    }
    /* 도움말(Help) 스타일 */
    .help-h { color: var(--primary); font-weight: 700; font-size: 15px;
        margin: 14px 0 6px 0; font-family: 'Inter','Pretendard',sans-serif; }
    .help-p { color: var(--on-variant); font-size: 13.5px; line-height: 1.75;
        font-family: 'Inter','Pretendard',sans-serif; }
    .help-p b { color: var(--on-surface); }
    [data-testid="stExpander"] summary { font-size: 15px !important; font-weight: 600; }
    [data-testid="stExpander"] { border: 1px solid var(--outline-variant) !important;
        border-radius: 8px !important; background: var(--surface) !important; }
    .tag.accent { color: var(--primary); }

    /* ── Drag & drop zone ── */
    [data-testid="stFileUploaderDropzone"] {
        background: linear-gradient(135deg, #1a2332 0%, var(--surface-low) 100%);
        border: 2px dashed #3a6ea5 !important; border-radius: 8px !important;
        padding: 32px 20px !important; transition: all .2s;
    }
    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: var(--primary) !important;
        box-shadow: 0 0 24px rgba(152,203,255,.18);
    }
    [data-testid="stFileUploaderDropzone"] svg { color: var(--primary); }
    /* 영어 안내문 → 한글 (인라인 치환: 절대위치 없이 자연 흐름으로 배치해 파일칩과 겹침 방지) */
    [data-testid="stFileUploaderDropzoneInstructions"] > div > span { font-size: 0 !important; }
    [data-testid="stFileUploaderDropzoneInstructions"] > div > span::after {
        content: "여기로 이미지를 끌어다 놓으세요";
        color: var(--on-surface); font-weight: 600;
        font-family: 'JetBrains Mono', 'Pretendard', sans-serif; font-size: 13px;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] > div > small { font-size: 0 !important; }
    [data-testid="stFileUploaderDropzoneInstructions"] > div > small::after {
        content: "JPG · PNG · TIFF · BMP · WEBP / 최대 200MB";
        color: var(--outline); font-family: 'JetBrains Mono', 'Pretendard', sans-serif; font-size: 11px;
    }
    [data-testid="stFileUploaderDropzone"] button {
        background: var(--surface-highest) !important;
        border: 1px solid var(--outline-variant) !important;
    }
    /* 버튼 라벨 "Upload" → "파일 선택" (아이콘은 유지) */
    [data-testid="stFileUploaderDropzone"] button [data-testid="stMarkdownContainer"] p {
        font-size: 0 !important;
    }
    [data-testid="stFileUploaderDropzone"] button [data-testid="stMarkdownContainer"] p::after {
        content: "파일 선택"; color: var(--on-surface);
        font-family: 'JetBrains Mono', 'Pretendard', sans-serif; font-size: 12px;
    }
    /* 업로드된 파일 칩 — 글자/아이콘 정상 표시 */
    [data-testid="stFileUploaderFile"] { color: var(--on-surface) !important; }
    [data-testid="stFileUploaderFileName"] {
        color: var(--on-surface) !important; font-family: 'JetBrains Mono', 'Pretendard', sans-serif;
    }

    h1, h2, h3, h4 { color: var(--on-surface); }
    .stImage img { border-radius: 4px; border: 1px solid var(--outline-variant); }
</style>
""", unsafe_allow_html=True)

# ── Top bar ──
st.markdown("""
<div class="lumina-topbar">
    <span class="lumina-brand">Lumina Grade</span>
    <span class="lumina-subtitle mono">DaVinci Resolve · .cube LUT Generator</span>
</div>
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


def _transfer(lab, ref_stats, strength, preserve_luminance):
    ref_mean, ref_std = ref_stats["lab_mean"], ref_stats["lab_std"]
    src_mean = np.array([50.0, 0.0, 0.0])
    src_std = np.array([25.0, 10.0, 10.0])
    out = lab.copy()
    l_ratio = ref_std[0] / max(src_std[0], 1e-6)
    out[:, 0] = (lab[:, 0] - src_mean[0]) * l_ratio + ref_mean[0]
    out[:, 0] = lab[:, 0] * preserve_luminance + out[:, 0] * (1 - preserve_luminance)
    for ch in [1, 2]:
        ratio = ref_std[ch] / max(src_std[ch], 1e-6)
        out[:, ch] = (lab[:, ch] - src_mean[ch]) * ratio + ref_mean[ch]
    return lab * (1 - strength) + out * strength


def generate_cube_lut(ref_stats, lut_size=33, strength=1.0, preserve_luminance=0.5) -> str:
    grid = np.linspace(0, 1, lut_size)
    r, g, b = np.meshgrid(grid, grid, grid, indexing="ij")
    rgb_grid = np.stack([r, g, b], axis=-1).reshape(-1, 3)
    lab_grid = rgb_to_lab(rgb_grid)
    blended = _transfer(lab_grid, ref_stats, strength, preserve_luminance)
    output_rgb = np.clip(lab_to_rgb(blended), 0, 1)
    lines = [
        "# Generated by Lumina Grade — Image Color Transfer LUT",
        f"# Strength: {strength:.0%}, Luminance Preserve: {preserve_luminance:.0%}",
        'TITLE "Lumina Color Transfer"',
        f"LUT_3D_SIZE {lut_size}",
        "DOMAIN_MIN 0.0 0.0 0.0",
        "DOMAIN_MAX 1.0 1.0 1.0",
        "",
    ]
    for i in range(len(output_rgb)):
        rr, gg, bb = output_rgb[i]
        lines.append(f"{rr:.6f} {gg:.6f} {bb:.6f}")
    return "\n".join(lines)


def generate_preview(img, ref_stats, strength, preserve_luminance) -> Image.Image:
    img_resized = img.copy()
    if max(img_resized.size) > 800:
        ratio = 800 / max(img_resized.size)
        img_resized = img_resized.resize(
            (int(img_resized.width * ratio), int(img_resized.height * ratio)), Image.LANCZOS)
    pixels = np.array(img_resized.convert("RGB")).astype(np.float64) / 255.0
    shape = pixels.shape
    lab = rgb_to_lab(pixels.reshape(-1, 3))
    blended = _transfer(lab, ref_stats, strength, preserve_luminance)
    out = (np.clip(lab_to_rgb(blended).reshape(shape), 0, 1) * 255).astype(np.uint8)
    return Image.fromarray(out)


# ════════════════════════════════════════════════════════════
#  SIDEBAR = INSPECTOR
# ════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="inspector-title">⚙️ 인스펙터 (Inspector)</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head primary">◈ 기본 보정 · BASE GRADE</div>', unsafe_allow_html=True)
    lut_size = st.select_slider(
        "LUT 해상도 (Resolution)",
        options=[17, 25, 33, 49, 65], value=33,
        help="LUT의 격자 정밀도입니다. 높을수록 색 표현이 정밀하지만 파일이 커집니다. 33이 업계 표준입니다.",
    )
    strength = st.slider(
        "색 전이 강도 (Strength)", 0.0, 1.0, 0.85, 0.05,
        help="레퍼런스 이미지의 색감을 얼마나 강하게 입힐지 결정합니다. 1에 가까울수록 원본 색감을 강하게 따라갑니다.",
    )
    preserve_luminance = st.slider(
        "밝기 보존 (Luminance)", 0.0, 1.0, 0.6, 0.05,
        help="원본 영상의 밝기(노출)를 얼마나 유지할지 결정합니다. 높을수록 색만 바뀌고 밝기는 원본을 유지합니다.",
    )

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-head secondary">◈ 크리에이티브 룩 · LOOK</div>', unsafe_allow_html=True)
    look = st.radio(
        "Creative Preset",
        ["None", "Teal & Orange", "Noir Silver", "Warm Film"],
        format_func=lambda x: {
            "None": "없음 (None)",
            "Teal & Orange": "틸 & 오렌지 (시네마틱)",
            "Noir Silver": "느와르 실버 (흑백톤)",
            "Warm Film": "웜 필름 (따뜻한 필름)",
        }[x],
        label_visibility="collapsed",
    )

    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sec-head muted">◈ 적용 순서 · HOW TO APPLY</div>
    <div style="font-size:12.5px; color:var(--on-variant); line-height:1.75;
         font-family:'Inter','Pretendard',sans-serif;">
    1. 레퍼런스 이미지 업로드<br>
    2. 설정 조정 → LUT 생성<br>
    3. .cube 파일 다운로드<br>
    4. DaVinci Resolve의 Color 페이지 →<br>
    &nbsp;&nbsp;&nbsp;노드 우클릭 → LUTs → 적용
    </div>
    """, unsafe_allow_html=True)


def apply_creative_look(stats, look):
    """Adjust target LAB stats based on creative preset."""
    s = dict(stats)
    mean = stats["lab_mean"].copy()
    std = stats["lab_std"].copy()
    if look == "Teal & Orange":
        mean[1] += 4; mean[2] += 6; std[1] *= 1.15; std[2] *= 1.15
    elif look == "Noir Silver":
        std[1] *= 0.25; std[2] *= 0.25; mean[1] *= 0.2; mean[2] *= 0.2
    elif look == "Warm Film":
        mean[2] += 10; mean[1] += 3
    s["lab_mean"] = mean
    s["lab_std"] = std
    return s


# ════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════

# ── 도움말 (Help) ──
with st.expander("📖  도움말 · 전체 사용 설명서 (Help & Guide)", expanded=False):
    st.markdown("""
    <div class="help-p">
    <div class="help-h">🎬 이 프로그램은 무엇인가요?</div>
    마음에 드는 색감의 <b>레퍼런스 이미지</b>(영화 스틸컷, 사진, 색보정 샘플 등)를 올리면,
    그 이미지의 색을 분석해서 <b>DaVinci Resolve에서 바로 쓸 수 있는 .cube LUT 파일</b>을 만들어 줍니다.
    이 LUT을 내 영상에 적용하면 레퍼런스와 비슷한 색감/분위기로 보정됩니다.<br>
    <span style="color:var(--outline)">※ LUT(Look-Up Table): 입력 색을 출력 색으로 바꿔주는 색 변환표. 색보정 프리셋이라고 생각하면 됩니다.</span>

    <div class="help-h">🚀 사용 순서 (4단계)</div>
    <b>1단계 — 이미지 업로드:</b> 원하는 색감의 이미지를 점선 영역에 끌어다 놓거나 '파일 선택'으로 올립니다. (여러 장 올리고 하나를 고를 수도 있어요)<br>
    <b>2단계 — 설정 조정:</b> 왼쪽 인스펙터에서 강도·밝기·룩을 조절하며 오른쪽 미리보기를 확인합니다.<br>
    <b>3단계 — LUT 생성/다운로드:</b> 아래 'LUT 생성' 버튼을 누르고 .cube 파일을 받습니다.<br>
    <b>4단계 — Resolve에 적용:</b> 다운받은 파일을 DaVinci Resolve에 불러옵니다. (아래 '적용 방법' 참고)

    <div class="help-h">⚙️ 왼쪽 설정(인스펙터) 설명</div>
    <b>· LUT 해상도 (Resolution):</b> 색 변환표의 격자 정밀도. 33이 표준이며 대부분 충분합니다. 49·65는 더 정밀하지만 파일이 커집니다.<br>
    <b>· 색 전이 강도 (Strength):</b> 레퍼런스 색감을 얼마나 세게 입힐지. 낮추면 은은하게, 높이면 강하게 적용됩니다.<br>
    <b>· 밝기 보존 (Luminance):</b> 원본 영상의 밝기를 얼마나 지킬지. 높이면 밝기는 그대로 두고 색만 바뀝니다.<br>
    <b>· 크리에이티브 룩 (Look):</b> 분석 색감 위에 추가로 입히는 무드.<br>
    &nbsp;&nbsp;– <b>없음</b>: 레퍼런스 색감 그대로<br>
    &nbsp;&nbsp;– <b>틸 & 오렌지</b>: 그림자는 청록, 인물/하이라이트는 주황 — 시네마틱 영화 룩<br>
    &nbsp;&nbsp;– <b>느와르 실버</b>: 채도를 크게 낮춘 흑백/모노톤 느낌<br>
    &nbsp;&nbsp;– <b>웜 필름</b>: 전체적으로 따뜻하고 노란빛 도는 필름 감성

    <div class="help-h">📊 분석 결과 읽는 법</div>
    <b>· 주요 색상 (Palette):</b> 이미지에서 가장 많이 쓰인 대표 색들.<br>
    <b>· 톤 분포:</b> 어두운 영역(섀도)·중간(미드톤)·밝은 영역(하이라이트)의 비율.<br>
    <b>· 색온도/틴트:</b> 따뜻함(Warm)·차가움(Cool), 마젠타·그린 치우침 정도.<br>
    <b>· RGB 히스토그램:</b> 빨강·초록·파랑 각 채널의 밝기 분포 그래프.

    <div class="help-h">🎞️ DaVinci Resolve에 적용하는 3가지 방법</div>
    <b>A. Color 페이지에서 바로:</b> Color 탭 → 노드에서 우클릭 → <b>LUTs</b> → 다운받은 .cube 선택<br>
    <b>B. 프로젝트 설정:</b> File → Project Settings → Color Management → 3D Lookup Table에서 선택<br>
    <b>C. LUT 폴더에 복사 후 사용:</b> .cube 파일을 아래 폴더에 넣고 Resolve 재시작<br>
    &nbsp;&nbsp;<span style="color:var(--outline)">macOS: /Library/Application Support/Blackmagic Design/DaVinci Resolve/LUT/</span><br>
    &nbsp;&nbsp;<span style="color:var(--outline)">Windows: C:\\ProgramData\\Blackmagic Design\\DaVinci Resolve\\Support\\LUT\\</span>

    <div class="help-h">💡 팁</div>
    · 레퍼런스와 내 영상의 노출이 비슷할수록 결과가 자연스럽습니다.<br>
    · 색감이 과하면 '색 전이 강도'를 낮춰보세요.<br>
    · 적용 후 Resolve에서 노드의 Key(불투명도)로 LUT 세기를 미세 조정할 수 있습니다.
    </div>
    """, unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "reference", type=["jpg", "jpeg", "png", "tiff", "bmp", "webp"],
    accept_multiple_files=True, label_visibility="collapsed",
)

if uploaded_files:
    if len(uploaded_files) > 1:
        names = [f.name for f in uploaded_files]
        selected = st.radio(
            f"{len(uploaded_files)}개 업로드됨 — 분석할 이미지 선택",
            names, horizontal=True,
        )
        uploaded = next(f for f in uploaded_files if f.name == selected)
    else:
        uploaded = uploaded_files[0]

    img = Image.open(uploaded).convert("RGB")

    with st.spinner("색상 분석 중..."):
        base_stats = analyze_image(img)
    stats = apply_creative_look(base_stats, look)

    # ── Preview row: 원본 | LUT 적용 ──
    pv1, pv2 = st.columns(2)
    with pv1:
        st.markdown('<div class="sec-head muted">◈ 원본 · REFERENCE</div>', unsafe_allow_html=True)
        st.image(img, use_container_width=True)
    with pv2:
        st.markdown('<div class="sec-head primary">◈ 보정 미리보기 · GRADED</div>', unsafe_allow_html=True)
        with st.spinner("미리보기 생성 중..."):
            preview = generate_preview(img, stats, strength, preserve_luminance)
        st.image(preview, use_container_width=True)

    # ── Metadata strip ──
    lab_m = stats["lab_mean"]
    lum = stats["luminance_stats"]
    if lab_m[2] > 10:
        temp = "Warm 🟡"
    elif lab_m[2] < -10:
        temp = "Cool 🔵"
    else:
        temp = "Neutral ⚪"
    tint = "Magenta" if lab_m[1] > 5 else ("Green" if lab_m[1] < -5 else "Neutral")

    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    meta = [
        (m1, "색온도 · Temp", temp),
        (m2, "틴트 · Tint", tint),
        (m3, "평균 밝기 · Luma", f"{lum['mean']:.2f}"),
        (m4, "LUT 크기 · Size", f"{lut_size}³ = {lut_size**3:,}"),
    ]
    for col, label, value in meta:
        with col:
            st.markdown(
                f'<div class="meta-cell"><span class="meta-label">{label}</span>'
                f'<span class="meta-value">{value}</span></div>',
                unsafe_allow_html=True,
            )

    # ── Analysis panels ──
    st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
    an1, an2 = st.columns([1, 1])

    with an1:
        st.markdown('<div class="sec-head secondary">◈ 주요 색상 · PALETTE</div>', unsafe_allow_html=True)
        swatches = ""
        for c in base_stats["dominant_colors"]:
            hexc = "#{:02x}{:02x}{:02x}".format(
                int(c[0] * 255), int(c[1] * 255), int(c[2] * 255))
            swatches += f'<div class="swatch" style="background:{hexc}" title="{hexc}"></div>'
        st.markdown(f'<div class="swatch-row">{swatches}</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-head muted">◈ 톤 분포 · TONE</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:13px; color:var(--on-variant); line-height:2;
             font-family:'Inter','Pretendard',sans-serif;">
        🌑 섀도우 (Shadows)&nbsp;&nbsp;<b style="color:var(--on-surface)">{lum['shadows_pct']:.1f}%</b><br>
        🌓 미드톤 (Midtones)&nbsp;&nbsp;<b style="color:var(--on-surface)">{lum['midtones_pct']:.1f}%</b><br>
        🌕 하이라이트 (Highlights)&nbsp;&nbsp;<b style="color:var(--on-surface)">{lum['highlights_pct']:.1f}%</b>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
        tags = ["Cinematic", f"LUT{lut_size}", temp.split()[0], tint]
        if look != "None":
            tags.append(look)
        tag_html = "".join(f'<span class="tag">{t}</span>' for t in tags)
        st.markdown('<div class="sec-head muted">◈ 태그 · TAGS</div>', unsafe_allow_html=True)
        st.markdown(f'<div>{tag_html}</div>', unsafe_allow_html=True)

    with an2:
        st.markdown('<div class="sec-head primary">◈ RGB 히스토그램 · HISTOGRAM</div>', unsafe_allow_html=True)
        for ch, color in zip(["R", "G", "B"], ["#ff6b6b", "#51cf66", "#74c0fc"]):
            st.markdown(
                f'<div style="font-size:11px; color:var(--outline); font-family:Inter">{ch} 채널 (Channel)</div>',
                unsafe_allow_html=True)
            st.bar_chart(base_stats["histograms"][ch], color=color, height=90)

    # ── Generate ──
    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-head primary">◈ 내보내기 · EXPORT LUT</div>', unsafe_allow_html=True)

    g1, g2 = st.columns([3, 2])
    with g1:
        filename = st.text_input(
            "File name", value=f"lumina_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            label_visibility="collapsed",
        )
    with g2:
        gen = st.button("✦  .cube LUT 생성", type="primary", use_container_width=True)

    if gen:
        with st.spinner(f"{lut_size}³ LUT 생성 중..."):
            cube = generate_cube_lut(stats, lut_size, strength, preserve_luminance)
        st.success(f"LUT 생성 완료 — {lut_size}³ = {lut_size**3:,} 포인트")
        st.download_button(
            "⬇  .cube 파일 다운로드", data=cube,
            file_name=f"{filename}.cube", mime="text/plain",
            use_container_width=True,
        )
        st.markdown("""
        <div class="panel" style="margin-top:14px;">
            <div style="font-size:13px; color:var(--on-variant); line-height:1.85;
                 font-family:'Inter','Pretendard',sans-serif;">
            <b style="color:var(--primary); font-size:14px;">🎞️ DaVinci Resolve 적용 방법</b><br><br>
            <b>A. Color 페이지에서:</b> 노드 우클릭 → <b>LUTs</b> → 다운받은 .cube 선택<br>
            <b>B. 프로젝트 설정:</b> Project Settings → Color Management → 3D Lookup Table<br>
            <b>C. LUT 폴더에 복사:</b>
            <span style="color:var(--outline)">/Library/Application Support/Blackmagic Design/DaVinci Resolve/LUT/</span>
            에 넣고 Resolve 재시작
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    # ── Landing ──
    st.markdown("""
    <div class="panel" style="text-align:center; padding:48px 24px; margin-top:8px;
         background:linear-gradient(135deg,#1a2332 0%,var(--surface-low) 100%);">
        <div style="font-size:40px; margin-bottom:8px;">🎬</div>
        <div style="color:var(--primary); font-size:16px; font-weight:700; margin-bottom:8px;
             font-family:'Inter','Pretendard',sans-serif;">
            이미지 → DaVinci Resolve LUT
        </div>
        <div style="color:var(--on-variant); font-size:14.5px; line-height:1.75;">
            레퍼런스 이미지의 색감을 분석해 DaVinci Resolve용 <b>.cube LUT</b>을 생성합니다.<br>
            영화 스틸컷 · 사진 · 컬러 레퍼런스를 위 영역에 끌어다 놓으세요.<br>
            <span style="color:var(--outline); font-size:13px;">처음이라면 위의 <b>📖 도움말</b>을 먼저 펼쳐보세요.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
