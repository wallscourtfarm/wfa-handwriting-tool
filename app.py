import streamlit as st
import tempfile
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
import handwriting_sheet as hs

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title='WFA Handwriting Sheet Generator',
    page_icon='✏️',
    layout='centered',
)

# ── Fonts loaded once ─────────────────────────────────────────────────────────

@st.cache_resource
def load_fonts():
    hs._ensure_fonts()

load_fonts()

# ── Helpers ───────────────────────────────────────────────────────────────────

LOGO_PATH = Path('assets/wfa_logo.jpg')

def _b64_img(path):
    import base64
    return base64.b64encode(Path(path).read_bytes()).decode()

# ── Styles ────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
    div[data-testid="stMainBlockContainer"] { max-width: 860px; margin: 0 auto; }

    div[data-testid="stButton"] > button {
        background-color: #1798d3;
        color: white;
        border: none;
        padding: 0.6rem 1.4rem;
        font-size: 1rem;
        border-radius: 6px;
        width: 100%;
    }
    div[data-testid="stButton"] > button:hover {
        background-color: #1270a8;
    }
    div[data-testid="stDownloadButton"] > button {
        border: 1.5px solid #1798d3 !important;
        color: #1798d3 !important;
        background: #ffffff !important;
        padding: 0.6rem 1.4rem;
        font-size: 1rem;
        border-radius: 6px;
        width: 100%;
    }
    div[data-testid="stDownloadButton"] > button:hover {
        background: #f0f8ff !important;
    }
    .note {
        background: #eaf6fb;
        border-left: 4px solid #1798d3;
        padding: 0.6rem 1rem;
        border-radius: 4px;
        font-size: 0.9rem;
        color: #0e2841;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────

if LOGO_PATH.exists():
    logo_b64 = _b64_img(LOGO_PATH)
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:18px;margin-bottom:6px;">'
        f'<img src="data:image/jpeg;base64,{logo_b64}" style="height:60px;width:auto;">'
        f'<span style="font-size:1.75rem;font-weight:700;color:#1798d3;">'
        f'✏️ Handwriting Sheet Generator</span></div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<span style="font-size:1.75rem;font-weight:700;color:#1798d3;">'
        '✏️ Handwriting Sheet Generator</span>',
        unsafe_allow_html=True,
    )

st.divider()

st.markdown(
    '<div class="note">Type or paste your words or sentences below — '
    'one per line. Choose a font style and how many practice lines to '
    'add after each traced item, then generate your PDF.</div>',
    unsafe_allow_html=True,
)

# ── Form ──────────────────────────────────────────────────────────────────────

sheet_title = st.text_input(
    'Sheet title',
    value='Handwriting Practice',
    max_chars=80,
)

content_raw = st.text_area(
    'Words or sentences (one per line)',
    height=200,
    placeholder='The cat sat on the mat.\nShe ran quickly down the hill.\nbig brave brilliant',
)

col1, col2 = st.columns(2)

with col1:
    font_label = st.selectbox(
        'Font style',
        options=[
            'Print — Sassoon Dotted',
            'Pre-cursive — Linkpen Dotted',
            'Cursive — XCCW Dotted',
        ],
    )

with col2:
    practice_lines = st.selectbox(
        'Practice lines after each item',
        options=[0, 1, 2, 3],
        index=0,
        format_func=lambda n: f'{n} line{"s" if n != 1 else ""}',
    )

# ── Generate ──────────────────────────────────────────────────────────────────

FONT_MAP = {
    'Print — Sassoon Dotted':       'sassoon',
    'Pre-cursive — Linkpen Dotted': 'linkpen',
    'Cursive — XCCW Dotted':        'xccw',
}

def build_pdf(lines, title, font_style, practice_lines):
    rows = [{'type': 'word', 'text': line} for line in lines]

    if font_style == 'sassoon':
        ascend, descend = hs.SASS_ASCEND, hs.SASS_DESCEND
        draw_fn, fs     = hs._draw_sassoon, hs.SASS_FS
    elif font_style == 'linkpen':
        ascend, descend = hs.LINK_ASCEND, hs.LINK_DESCEND
        draw_fn, fs     = hs._draw_linkpen, hs.LINK_FS
    else:  # xccw
        ascend, descend = hs.XCCW_ASCEND, hs.XCCW_DESCEND
        draw_fn = lambda c, x, y, text, size: hs._draw_xccw(c, x, y, text, size, solid=False)
        fs = hs.XCCW_FS

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        tmp = f.name

    hs._generate_pdf(tmp, rows, title, None, ascend, descend, draw_fn, fs,
                     practice_lines=practice_lines)

    with open(tmp, 'rb') as f:
        pdf_bytes = f.read()
    os.unlink(tmp)
    return pdf_bytes


if st.button('Generate PDF'):
    lines = [l.strip() for l in content_raw.splitlines() if l.strip()]
    if not lines:
        st.error('Please enter at least one word or sentence.')
    else:
        font_style = FONT_MAP[font_label]
        with st.spinner('Building your sheet…'):
            try:
                pdf_bytes = build_pdf(lines, sheet_title, font_style, practice_lines)
                st.success(f'Sheet ready — {len(lines)} item{"s" if len(lines) != 1 else ""}, '
                           f'{practice_lines} practice line{"s" if practice_lines != 1 else ""} each.')
                safe_title = sheet_title.replace(' ', '_').lower()
                st.download_button(
                    label='⬇ Download PDF',
                    data=pdf_bytes,
                    file_name=f'{safe_title}.pdf',
                    mime='application/pdf',
                )
            except Exception as e:
                st.error(f'Something went wrong: {e}')

# ── Footer ────────────────────────────────────────────────────────────────────

st.markdown('---')
st.caption('Wallscourt Farm Academy · Cabot Learning Federation · For internal school use only.')
