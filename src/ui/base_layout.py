"""Shared animated background styling for SnapClass."""

import streamlit as st

from src.ui.assets import static_data_uri


BACKGROUND_IMAGE_URL = static_data_uri("classroom-group-light-animated.png")

_BACKGROUND_CSS = """
<style>
    html, body, .stApp,
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > .main,
    section.main,
    .main .block-container {
        background-color: transparent !important;
    }

    [data-testid="stAppViewContainer"] {
        background-image:
            linear-gradient(120deg, rgba(255,182,218,.62), rgba(203,239,255,.62), rgba(255,244,172,.45), rgba(221,203,255,.54)),
            url("__CLASSROOM_IMAGE__") !important;
        background-size: 320% 320%, cover !important;
        background-position: 0% 50%, center 42% !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
        min-height: 100vh !important;
        overflow-x: hidden !important;
        animation: snap-gradient-flow 14s ease-in-out infinite, classroom-drift 18s ease-in-out infinite alternate;
    }

    [data-testid="stAppViewContainer"]::before,
    [data-testid="stAppViewContainer"]::after {
        content: "";
        position: fixed;
        z-index: 0;
        left: 8vw;
        bottom: -9rem;
        width: 5rem;
        height: 5rem;
        border-radius: 50%;
        pointer-events: none;
        background: radial-gradient(circle at 30% 25%, white 0 8%, #ff9fc6 24%, #ed75aa 68%, #cb4d8a 100%);
        box-shadow:
            16vw 18vh 0 -1rem #82d8ff,
            34vw -4vh 0 1.2rem #c7b5ff,
            50vw 28vh 0 -.4rem #ffe385,
            67vw 4vh 0 .7rem #89edb1,
            82vw 31vh 0 -.8rem #ffaaa5;
        filter: drop-shadow(0 15px 16px rgba(70,85,145,.22));
        opacity: .72;
        animation: snap-bubbles-rise 14s linear infinite;
        will-change: transform;
    }

    [data-testid="stAppViewContainer"]::after {
        left: 16vw;
        bottom: -16rem;
        width: 7rem;
        height: 7rem;
        background: radial-gradient(circle at 30% 25%, white 0 7%, #8ce9ff 25%, #56c8ed 68%, #399bc6 100%);
        box-shadow:
            20vw 8vh 0 -1.8rem #ff98c3,
            39vw 25vh 0 -.8rem #fff09c,
            58vw -2vh 0 .5rem #b99cff,
            76vw 19vh 0 -1rem #8ff0b7;
        animation-duration: 20s;
        animation-delay: -9s;
        opacity: .60;
    }

    .main .block-container {
        position: relative;
        z-index: 1;
    }

    /* Glassmorphism cards for Streamlit containers, forms and visual blocks */
    [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stForm"],
    [data-testid="stMetric"],
    div[data-testid="stExpander"] details {
        background: rgba(255, 255, 255, .42) !important;
        border: 1px solid rgba(255, 255, 255, .58) !important;
        border-radius: 28px !important;
        box-shadow: 0 20px 55px rgba(72, 100, 160, .18), inset 0 1px 0 rgba(255,255,255,.65) !important;
        backdrop-filter: blur(18px) saturate(145%) !important;
        -webkit-backdrop-filter: blur(18px) saturate(145%) !important;
    }

    .stButton > button {
        position: relative !important;
        overflow: hidden !important;
        border-radius: 50px !important;
        border: 1px solid rgba(255,255,255,.72) !important;
        background: linear-gradient(135deg, #ff2d75 0%, #ff8a00 34%, #18c7ff 70%, #7c4dff 100%) !important;
        background-size: 240% 240% !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        letter-spacing: .02em !important;
        box-shadow: 0 14px 34px rgba(255,45,117,.30), 0 8px 18px rgba(24,199,255,.22) !important;
        transition: transform .25s ease, box-shadow .25s ease, filter .25s ease, background-position .45s ease !important;
    }

    .stButton > button::before {
        content: "";
        position: absolute;
        inset: 0;
        transform: translateX(-120%) skewX(-18deg);
        background: linear-gradient(90deg, transparent, rgba(255,255,255,.42), transparent);
        transition: transform .55s ease;
        pointer-events: none;
    }

    .stButton > button:hover {
        transform: translateY(-5px) scale(1.035) !important;
        background-position: 100% 50% !important;
        box-shadow: 0 22px 48px rgba(255,45,117,.36), 0 14px 30px rgba(24,199,255,.30) !important;
        filter: saturate(1.18) brightness(1.04) !important;
    }

    .stButton > button:hover::before {
        transform: translateX(120%) skewX(-18deg);
    }

    .stButton > button:active {
        transform: translateY(-1px) scale(.99) !important;
        box-shadow: 0 10px 24px rgba(124,77,255,.26) !important;
    }

    .snap-floating-icons {
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        overflow: hidden;
    }

    .snap-floating-icons span {
        position: absolute;
        display: grid;
        place-items: center;
        width: 3.2rem;
        height: 3.2rem;
        border-radius: 1.1rem;
        background: rgba(255,255,255,.34);
        border: 1px solid rgba(255,255,255,.52);
        box-shadow: 0 16px 35px rgba(76,108,168,.16);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        animation: snap-icon-float 9s ease-in-out infinite;
    }

    .snap-floating-icons svg {
        width: 2rem;
        height: 2rem;
        filter: drop-shadow(0 8px 12px rgba(74, 99, 170, .18));
    }

    .snap-floating-icons span:nth-child(1) { top: 18%; left: 7%; animation-delay: -1s; }
    .snap-floating-icons span:nth-child(2) { top: 24%; right: 9%; animation-delay: -4s; }
    .snap-floating-icons span:nth-child(3) { bottom: 22%; left: 12%; animation-delay: -6s; }
    .snap-floating-icons span:nth-child(4) { bottom: 16%; right: 13%; animation-delay: -2s; }
    .snap-floating-icons span:nth-child(5) { top: 52%; right: 4%; animation-delay: -7s; }

    @keyframes snap-gradient-flow {
        0% { background-position: 0% 50%, center 42%; }
        50% { background-position: 100% 50%, center 45%; }
        100% { background-position: 0% 50%, center 42%; }
    }

    @keyframes classroom-drift {
        from { filter: saturate(1); }
        to { filter: saturate(1.08) brightness(1.03); }
    }

    @keyframes snap-bubbles-rise {
        0% { transform: translate3d(0, 0, -80px) rotate(0deg) scale(.72); }
        35% { transform: translate3d(4vw, -42vh, 70px) rotate(130deg) scale(1); }
        70% { transform: translate3d(-3vw, -82vh, 120px) rotate(270deg) scale(.88); }
        100% { transform: translate3d(2vw, -132vh, -50px) rotate(420deg) scale(.65); }
    }

    @keyframes snap-icon-float {
        0%, 100% { transform: translate3d(0, 0, 0) rotate(-6deg); }
        50% { transform: translate3d(1.2rem, -1.8rem, 0) rotate(8deg); }
    }


    @media (max-width: 768px) {
        html, body, .stApp {
            overflow-x: hidden !important;
        }

        .main .block-container {
            padding-left: .85rem !important;
            padding-right: .85rem !important;
            padding-top: .75rem !important;
            max-width: 100vw !important;
        }

        [data-testid="stAppViewContainer"] {
            background-size: 360% 360%, cover !important;
            background-position: 50% 50%, center top !important;
            background-attachment: scroll !important;
        }

        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: .85rem !important;
        }

        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 0 !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"],
        [data-testid="stForm"],
        [data-testid="stMetric"],
        div[data-testid="stExpander"] details {
            width: 100% !important;
            border-radius: 20px !important;
            box-shadow: 0 12px 30px rgba(72, 100, 160, .16) !important;
        }

        h1 { font-size: 2rem !important; }
        h2 { font-size: 1.55rem !important; }
        h3 { font-size: 1.25rem !important; }
        p, label, .stMarkdown, .stCaptionContainer { font-size: .95rem !important; }

        img {
            max-width: 100% !important;
            height: auto !important;
        }

        .stButton > button {
            width: 100% !important;
            min-height: 3rem !important;
            font-size: .95rem !important;
            border-radius: 50px !important;
            padding: .7rem 1rem !important;
            white-space: normal !important;
        }

        [data-testid="stDataFrame"],
        [data-testid="stTable"],
        .stDataFrame {
            width: 100% !important;
            overflow-x: auto !important;
        }

        input, textarea, select,
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stDateInput"] input {
            font-size: 16px !important;
        }

        [data-testid="stChatMessage"] {
            max-width: 100% !important;
        }

        .snap-floating-icons span {
            width: 2.25rem;
            height: 2.25rem;
            opacity: .45;
        }

        .snap-floating-icons svg {
            width: 1.35rem;
            height: 1.35rem;
        }

        .snap-floating-icons span:nth-child(3),
        .snap-floating-icons span:nth-child(4),
        .snap-floating-icons span:nth-child(5) {
            display: none;
        }
    }

    @media (max-width: 420px) {
        .main .block-container {
            padding-left: .65rem !important;
            padding-right: .65rem !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"],
        [data-testid="stForm"],
        [data-testid="stMetric"],
        div[data-testid="stExpander"] details {
            border-radius: 16px !important;
        }

        .stButton > button {
            min-height: 2.85rem !important;
            font-size: .9rem !important;
        }
    }
    @media (prefers-reduced-motion: reduce) {
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"]::before,
        [data-testid="stAppViewContainer"]::after,
        .snap-floating-icons span {
            animation: none !important;
        }
    }
</style>
"""


_UI_ENHANCEMENTS_CSS = """
<style>
    :root {
        --snap-accent-a: __ACCENT_A__;
        --snap-accent-b: __ACCENT_B__;
        --snap-accent-c: __ACCENT_C__;
    }

    .main .block-container {
        animation: snap-page-enter .55s ease both;
    }

    .element-container,
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"] {
        animation: snap-soft-rise .55s ease both;
    }

    [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stMetric"],
    [data-testid="stForm"] {
        transition: transform .24s ease, box-shadow .24s ease, border-color .24s ease !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:hover,
    [data-testid="stMetric"]:hover,
    [data-testid="stForm"]:hover {
        transform: translateY(-4px) scale(1.008) !important;
        box-shadow: 0 26px 64px rgba(72, 100, 160, .24), inset 0 1px 0 rgba(255,255,255,.72) !important;
        border-color: rgba(255,255,255,.78) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--snap-accent-a), var(--snap-accent-b), var(--snap-accent-c)) !important;
        background-size: 240% 240% !important;
    }

    .snap-particles {
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        overflow: hidden;
    }

    .snap-particles i {
        position: absolute;
        display: block;
        width: .55rem;
        height: .55rem;
        border-radius: 999px;
        background: linear-gradient(135deg, var(--snap-accent-a), var(--snap-accent-b));
        opacity: .45;
        filter: blur(.2px);
        animation: snap-particle-drift 12s linear infinite;
    }

    .snap-particles i:nth-child(1) { left: 7%; top: 85%; animation-delay: -1s; }
    .snap-particles i:nth-child(2) { left: 18%; top: 72%; animation-delay: -4s; width: .75rem; height: .75rem; }
    .snap-particles i:nth-child(3) { left: 40%; top: 92%; animation-delay: -7s; }
    .snap-particles i:nth-child(4) { left: 61%; top: 78%; animation-delay: -2s; width: .8rem; height: .8rem; }
    .snap-particles i:nth-child(5) { left: 82%; top: 88%; animation-delay: -5s; }
    .snap-particles i:nth-child(6) { left: 93%; top: 69%; animation-delay: -9s; width: .7rem; height: .7rem; }

    .snap-ai-float {
        position: fixed;
        right: 1.1rem;
        bottom: 1.1rem;
        z-index: 20;
        display: flex;
        align-items: center;
        gap: .65rem;
        padding: .7rem .95rem;
        border-radius: 999px;
        color: #17213f;
        background: rgba(255,255,255,.68);
        border: 1px solid rgba(255,255,255,.75);
        box-shadow: 0 18px 42px rgba(54, 88, 160, .22);
        backdrop-filter: blur(18px) saturate(160%);
        -webkit-backdrop-filter: blur(18px) saturate(160%);
        animation: snap-ai-float 3s ease-in-out infinite;
    }

    .snap-ai-float-bot {
        display: grid;
        place-items: center;
        width: 2.45rem;
        height: 2.45rem;
        border-radius: 999px;
        color: white;
        font-weight: 900;
        background: linear-gradient(135deg, var(--snap-accent-a), var(--snap-accent-b), var(--snap-accent-c));
        box-shadow: 0 10px 24px rgba(124,77,255,.28);
    }

    .snap-ai-float-text {
        display: grid;
        line-height: 1.1;
        font-weight: 800;
        font-size: .82rem;
    }

    .snap-counter-card {
        position: relative;
        overflow: hidden;
        padding: 1.05rem;
        border-radius: 24px;
        background: rgba(255,255,255,.42);
        border: 1px solid rgba(255,255,255,.62);
        box-shadow: 0 18px 44px rgba(72,100,160,.16);
        backdrop-filter: blur(16px);
    }

    .snap-counter-card::after {
        content: "";
        position: absolute;
        inset: 0;
        transform: translateX(-100%);
        background: linear-gradient(90deg, transparent, rgba(255,255,255,.42), transparent);
        animation: snap-shimmer 3s ease-in-out infinite;
    }

    .snap-counter-number {
        font-size: clamp(1.8rem, 4vw, 2.8rem);
        font-weight: 950;
        line-height: 1;
        background: linear-gradient(90deg, var(--snap-accent-a), var(--snap-accent-b), var(--snap-accent-c));
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        animation: snap-counter-pop .9s cubic-bezier(.2, 1.2, .25, 1) both;
    }

    .snap-skeleton-card {
        padding: 1rem;
        border-radius: 22px;
        background: rgba(255,255,255,.36);
        border: 1px solid rgba(255,255,255,.54);
        backdrop-filter: blur(14px);
    }

    .snap-skeleton-line,
    .snap-skeleton-pill {
        border-radius: 999px;
        background: linear-gradient(90deg, rgba(255,255,255,.35), rgba(255,255,255,.85), rgba(255,255,255,.35));
        background-size: 220% 100%;
        animation: snap-loading-skeleton 1.25s ease-in-out infinite;
    }

    .snap-skeleton-line { height: .9rem; margin: .7rem 0; }
    .snap-skeleton-pill { width: 42%; height: 1.8rem; margin-top: 1rem; }




    .snap-pink-bubbles {
        position: fixed;
        inset: 0;
        z-index: 0;
        overflow: hidden;
        pointer-events: none;
        background: linear-gradient(135deg, rgba(255,211,222,.16), rgba(178,96,121,.12) 48%, rgba(255,235,225,.15));
    }

    .snap-pink-bubbles span {
        --bubble-size: 9rem;
        --bubble-left: 8%;
        --bubble-time: 18s;
        --bubble-delay: 0s;
        position: absolute;
        left: var(--bubble-left);
        bottom: calc(var(--bubble-size) * -1.3);
        width: var(--bubble-size);
        height: var(--bubble-size);
        border-radius: 50%;
        opacity: .72;
        border: 1px solid rgba(255,255,255,.72);
        background:
            radial-gradient(circle at 29% 22%, rgba(255,255,255,.96) 0 3%, rgba(255,255,255,.42) 4% 9%, transparent 18%),
            radial-gradient(circle at 68% 76%, rgba(255,153,196,.48), transparent 44%),
            radial-gradient(circle at 38% 34%, rgba(255,239,246,.72), rgba(227,114,160,.36) 48%, rgba(113,36,71,.22) 76%, rgba(255,255,255,.45));
        box-shadow:
            inset -20px -24px 35px rgba(112,38,70,.17),
            inset 14px 16px 28px rgba(255,255,255,.55),
            0 25px 45px rgba(126,48,82,.18),
            0 0 24px rgba(255,179,211,.22);
        backdrop-filter: blur(2px) saturate(145%);
        animation: snap-pink-bubble-rise var(--bubble-time) ease-in-out var(--bubble-delay) infinite;
        will-change: transform;
    }

    .snap-pink-bubbles span::after {
        content: "";
        position: absolute;
        inset: 8%;
        border-radius: 50%;
        border-top: 2px solid rgba(255,255,255,.74);
        filter: blur(.3px);
    }

    .snap-pink-bubbles span:nth-child(1) { --bubble-size: 13rem; --bubble-left: 3%; --bubble-time: 24s; --bubble-delay: -9s; }
    .snap-pink-bubbles span:nth-child(2) { --bubble-size: 6rem; --bubble-left: 18%; --bubble-time: 17s; --bubble-delay: -2s; opacity: .58; }
    .snap-pink-bubbles span:nth-child(3) { --bubble-size: 10rem; --bubble-left: 34%; --bubble-time: 21s; --bubble-delay: -14s; }
    .snap-pink-bubbles span:nth-child(4) { --bubble-size: 4rem; --bubble-left: 48%; --bubble-time: 14s; --bubble-delay: -5s; opacity: .5; }
    .snap-pink-bubbles span:nth-child(5) { --bubble-size: 15rem; --bubble-left: 61%; --bubble-time: 27s; --bubble-delay: -18s; opacity: .64; }
    .snap-pink-bubbles span:nth-child(6) { --bubble-size: 7rem; --bubble-left: 76%; --bubble-time: 18s; --bubble-delay: -11s; }
    .snap-pink-bubbles span:nth-child(7) { --bubble-size: 3rem; --bubble-left: 88%; --bubble-time: 13s; --bubble-delay: -4s; opacity: .55; }
    .snap-pink-bubbles span:nth-child(8) { --bubble-size: 11rem; --bubble-left: 93%; --bubble-time: 23s; --bubble-delay: -16s; }
    .snap-pink-bubbles span:nth-child(9) { --bubble-size: 5rem; --bubble-left: 56%; --bubble-time: 16s; --bubble-delay: -8s; opacity: .5; }

    @keyframes snap-pink-bubble-rise {
        0% { transform: translate3d(0, 12vh, 0) scale(.78) rotate(0deg); }
        30% { transform: translate3d(2.2rem, -34vh, 0) scale(1.02) rotate(7deg); }
        62% { transform: translate3d(-1.6rem, -76vh, 0) scale(.9) rotate(-5deg); }
        100% { transform: translate3d(1.1rem, -126vh, 0) scale(.72) rotate(4deg); }
    }


    /* Keep face capture clear: hide decorative bubbles only while camera input is visible. */
    [data-testid="stAppViewContainer"]:has([data-testid="stCameraInput"]) .snap-pink-bubbles,
    [data-testid="stAppViewContainer"]:has([data-testid="stCameraInput"]) .snap-particles {
        display: none !important;
    }

    [data-testid="stAppViewContainer"]:has([data-testid="stCameraInput"])::before,
    [data-testid="stAppViewContainer"]:has([data-testid="stCameraInput"])::after {
        content: none !important;
        display: none !important;
        animation: none !important;
        box-shadow: none !important;
    }
    /* Always-visible pastel bubble layer shared by every SnapClass screen. */
    .element-container:has(.snap-pink-bubbles),
    [data-testid="stElementContainer"]:has(.snap-pink-bubbles),
    .stHtml:has(.snap-pink-bubbles) {
        position: static !important;
        transform: none !important;
        animation: none !important;
    }

    .snap-pink-bubbles {
        display: block !important;
        position: fixed !important;
        inset: 0 !important;
        z-index: 3 !important;
        pointer-events: none !important;
        overflow: hidden !important;
        background: transparent !important;
    }

    .snap-pink-bubbles span {
        position: absolute !important;
        bottom: auto !important;
        opacity: .76 !important;
        animation: snap-pastel-bob 6s ease-in-out infinite alternate !important;
        background: radial-gradient(circle at 28% 20%, #fff 0 5%, transparent 18%), radial-gradient(circle at 38% 35%, #ffd5e3, #ed91af 58%, #ad5775 88%) !important;
        box-shadow: inset -12px -15px 24px rgba(110,45,70,.24), inset 10px 12px 20px rgba(255,255,255,.75), 0 16px 28px rgba(95,48,76,.22) !important;
    }

    .snap-pink-bubbles span:nth-child(even) {
        background: radial-gradient(circle at 28% 20%, #fff 0 5%, transparent 18%), radial-gradient(circle at 38% 35%, #fffde9, #f7e8b1 58%, #d6b86f 88%) !important;
        box-shadow: inset -12px -15px 24px rgba(145,108,42,.18), inset 10px 12px 20px rgba(255,255,255,.86), 0 16px 28px rgba(130,101,54,.18) !important;
    }

    .snap-pink-bubbles span:nth-child(3n) {
        background: radial-gradient(circle at 28% 20%, #fff 0 5%, transparent 18%), radial-gradient(circle at 38% 35%, #e4effb, #a6c5df 58%, #7084ac 88%) !important;
    }

    .snap-pink-bubbles span:nth-child(1) { background: radial-gradient(circle at 28% 20%,#fff 0 5%,transparent 18%),radial-gradient(circle at 38% 35%,#ffd2dc,#ef8ea4 58%,#a9516d 88%) !important; }
    .snap-pink-bubbles span:nth-child(2) { background: radial-gradient(circle at 28% 20%,#fff 0 5%,transparent 18%),radial-gradient(circle at 38% 35%,#ffe4d2,#f4b18e 58%,#bc705d 88%) !important; }
    .snap-pink-bubbles span:nth-child(3) { background: radial-gradient(circle at 28% 20%,#fff 0 5%,transparent 18%),radial-gradient(circle at 38% 35%,#dcedf9,#91b9d6 58%,#5e759e 88%) !important; }
    .snap-pink-bubbles span:nth-child(4) { background: radial-gradient(circle at 28% 20%,#fff 0 5%,transparent 18%),radial-gradient(circle at 38% 35%,#eee4f8,#bca4d3 58%,#79628e 88%) !important; }
    .snap-pink-bubbles span:nth-child(5) { background: radial-gradient(circle at 28% 20%,#fff 0 5%,transparent 18%),radial-gradient(circle at 38% 35%,#fffbe6,#f6dfa4 58%,#c5a35b 88%) !important; }
    .snap-pink-bubbles span:nth-child(6) { background: radial-gradient(circle at 28% 20%,#fff 0 5%,transparent 18%),radial-gradient(circle at 38% 35%,#eaf4e8,#b9cfb0 58%,#738d76 88%) !important; }
    .snap-pink-bubbles span:nth-child(7) { background: radial-gradient(circle at 28% 20%,#fff 0 5%,transparent 18%),radial-gradient(circle at 38% 35%,#fbd7e8,#dc88b3 58%,#985075 88%) !important; }
    .snap-pink-bubbles span:nth-child(8) { background: radial-gradient(circle at 27% 19%,#fff 0 5%,#ffffff73 6% 13%,transparent 22%),radial-gradient(circle at 65% 72%,#c69bdd55,transparent 44%),radial-gradient(circle at 40% 35%,#f3e8fb99,#b58dce77 62%,#6d527a4f) !important; border:2px solid rgba(255,255,255,.74) !important; }
    .snap-pink-bubbles span:nth-child(9) { background: radial-gradient(circle at 28% 20%,#fff8d6 0 5%,transparent 18%),radial-gradient(circle at 38% 35%,#ffe89a,#d8a53e 58%,#88551f 88%) !important; box-shadow:inset -8px -10px 14px rgba(91,49,13,.28),inset 7px 8px 12px rgba(255,255,255,.72),0 12px 20px rgba(91,54,22,.24) !important; }
    /* Golden glass material inspired by the warm amber bubble reference. */
    .snap-pink-bubbles span:nth-child(n) {
        opacity: .82 !important;
        border: 1px solid rgba(255,248,205,.92) !important;
        background:
            radial-gradient(circle at 28% 19%, rgba(255,255,255,.98) 0 4%, rgba(255,255,255,.48) 5% 10%, transparent 17%),
            radial-gradient(circle at 68% 72%, rgba(255,225,132,.22), transparent 42%),
            radial-gradient(circle at 39% 36%, rgba(255,251,218,.75), rgba(255,238,164,.42) 53%, rgba(215,180,92,.24) 76%, rgba(255,242,174,.55)) !important;
        box-shadow:
            inset -13px -16px 24px rgba(151,118,45,.14),
            inset 10px 12px 21px rgba(255,255,255,.72),
            inset 0 0 9px rgba(255,222,110,.58),
            0 0 18px rgba(255,226,139,.30),
            0 16px 28px rgba(139,81,14,.20) !important;
        filter: saturate(1.12) drop-shadow(0 8px 12px rgba(170,135,54,.12)) !important;
    }

    .snap-pink-bubbles span:nth-child(n)::before {
        content: "";
        position: absolute;
        inset: 17%;
        border-radius: 50%;
        background:
            radial-gradient(circle at 18% 72%, rgba(255,255,255,.92) 0 2%, transparent 3%),
            radial-gradient(circle at 36% 82%, rgba(255,233,157,.88) 0 1.5%, transparent 3%),
            radial-gradient(circle at 57% 75%, rgba(255,255,255,.82) 0 2%, transparent 3.5%),
            radial-gradient(circle at 73% 84%, rgba(255,214,87,.9) 0 1.5%, transparent 3%),
            radial-gradient(circle at 47% 61%, rgba(255,255,255,.7) 0 1.4%, transparent 3%);
        opacity: .9;
    }

    .snap-pink-bubbles span:nth-child(n)::after {
        content: "";
        position: absolute;
        inset: 7%;
        border-radius: 50%;
        border-top: 2px solid rgba(255,255,255,.92);
        border-left: 1px solid rgba(255,248,205,.56);
        box-shadow: inset 4px 5px 9px rgba(255,255,255,.24);
    }
    /* Ruby red glass bubble material. */
    .snap-pink-bubbles span:nth-child(n) {
        opacity: .82 !important;
        border: 1px solid rgba(255,190,184,.90) !important;
        background:
            radial-gradient(circle at 28% 19%, rgba(255,255,255,.98) 0 4%, rgba(255,218,211,.58) 5% 10%, transparent 17%),
            radial-gradient(circle at 68% 72%, rgba(255,54,45,.34), transparent 42%),
            radial-gradient(circle at 39% 36%, rgba(255,139,125,.72), rgba(209,19,32,.68) 52%, rgba(91,0,16,.64) 78%, rgba(255,74,60,.54)) !important;
        box-shadow:
            inset -13px -16px 24px rgba(74,0,13,.42),
            inset 10px 12px 21px rgba(255,220,213,.52),
            inset 0 0 9px rgba(255,69,58,.52),
            0 0 18px rgba(235,31,39,.34),
            0 16px 28px rgba(82,0,17,.24) !important;
        filter: saturate(1.2) drop-shadow(0 8px 12px rgba(112,0,18,.20)) !important;
    }

    .snap-pink-bubbles span:nth-child(n)::before {
        background:
            radial-gradient(circle at 18% 72%, rgba(255,242,237,.95) 0 2%, transparent 3%),
            radial-gradient(circle at 36% 82%, rgba(255,129,112,.90) 0 1.5%, transparent 3%),
            radial-gradient(circle at 57% 75%, rgba(255,255,255,.86) 0 2%, transparent 3.5%),
            radial-gradient(circle at 73% 84%, rgba(255,74,61,.92) 0 1.5%, transparent 3%),
            radial-gradient(circle at 47% 61%, rgba(255,215,207,.76) 0 1.4%, transparent 3%) !important;
    }
    .snap-pink-bubbles span:nth-child(1) { width: 3.2rem !important; height: 3.2rem !important; left: 3% !important; top: 15% !important; }
    .snap-pink-bubbles span:nth-child(2) { width: 2.2rem !important; height: 2.2rem !important; left: 18% !important; top: 40% !important; animation-delay: -2s !important; }
    .snap-pink-bubbles span:nth-child(3) { width: 3.8rem !important; height: 3.8rem !important; left: 31% !important; top: 8% !important; animation-delay: -4s !important; }
    .snap-pink-bubbles span:nth-child(4) { width: 2.7rem !important; height: 2.7rem !important; left: 45% !important; top: 72% !important; animation-delay: -1s !important; }
    .snap-pink-bubbles span:nth-child(5) { width: 3.3rem !important; height: 3.3rem !important; left: 59% !important; top: 18% !important; animation-delay: -3s !important; }
    .snap-pink-bubbles span:nth-child(6) { width: 2rem !important; height: 2rem !important; left: 71% !important; top: 58% !important; animation-delay: -5s !important; }
    .snap-pink-bubbles span:nth-child(7) { width: 3.6rem !important; height: 3.6rem !important; left: 84% !important; top: 28% !important; animation-delay: -2.5s !important; }
    .snap-pink-bubbles span:nth-child(8) { width: 2.4rem !important; height: 2.4rem !important; left: 88% !important; top: 76% !important; animation-delay: -4.5s !important; }
    .snap-pink-bubbles span:nth-child(9) { width: 1.25rem !important; height: 1.25rem !important; left: 10% !important; top: 82% !important; animation-delay: -.5s !important; }

    /* Continuous liquid-rise transition with depth and staggered timing. */
    .snap-pink-bubbles span:nth-child(n) {
        --rise-x: 18px;
        animation-name: snap-liquid-rise !important;
        animation-timing-function: linear !important;
        animation-iteration-count: infinite !important;
        will-change: transform, opacity !important;
    }
    .snap-pink-bubbles span:nth-child(1) { animation-duration: 17s !important; animation-delay: -12s !important; --rise-x: 22px; }
    .snap-pink-bubbles span:nth-child(2) { animation-duration: 12s !important; animation-delay: -7s !important; --rise-x: -14px; }
    .snap-pink-bubbles span:nth-child(3) { animation-duration: 21s !important; animation-delay: -18s !important; --rise-x: 30px; }
    .snap-pink-bubbles span:nth-child(4) { animation-duration: 14s !important; animation-delay: -3s !important; --rise-x: -20px; }
    .snap-pink-bubbles span:nth-child(5) { animation-duration: 19s !important; animation-delay: -10s !important; --rise-x: 16px; }
    .snap-pink-bubbles span:nth-child(6) { animation-duration: 11s !important; animation-delay: -5s !important; --rise-x: -11px; }
    .snap-pink-bubbles span:nth-child(7) { animation-duration: 23s !important; animation-delay: -16s !important; --rise-x: 26px; }
    .snap-pink-bubbles span:nth-child(8) { animation-duration: 15s !important; animation-delay: -9s !important; --rise-x: -24px; }
    .snap-pink-bubbles span:nth-child(9) { animation-duration: 10s !important; animation-delay: -2s !important; --rise-x: 10px; }

    @keyframes snap-liquid-rise {
        0% { transform: translate3d(0, 30vh, 0) scale(.72) rotate(-4deg); opacity: 0; }
        8% { opacity: .72; }
        28% { transform: translate3d(var(--rise-x), 2vh, 0) scale(.92) rotate(2deg); opacity: .82; }
        54% { transform: translate3d(-12px, -35vh, 0) scale(1.03) rotate(-2deg); opacity: .78; }
        78% { transform: translate3d(var(--rise-x), -72vh, 0) scale(.95) rotate(3deg); opacity: .58; }
        94% { opacity: .16; }
        100% { transform: translate3d(-6px, -112vh, 0) scale(.76) rotate(0deg); opacity: 0; }
    }
    @keyframes snap-pastel-bob {
        from { transform: translate3d(-5px, 7px, 0) scale(.96) !important; }
        to { transform: translate3d(12px, -17px, 0) scale(1.04) !important; }
    }

    /* Clean layout fixes: prevent decorative layers from covering content */
    .main .block-container {
        max-width: 1120px !important;
        padding-top: 1rem !important;
        padding-bottom: 2.5rem !important;
    }

    [data-testid="stHeader"] {
        background: rgba(255,255,255,.18) !important;
        backdrop-filter: blur(10px) !important;
    }

    [data-testid="stAppViewContainer"]::before,
    [data-testid="stAppViewContainer"]::after {
        content: "" !important;
        display: block !important;
        position: fixed !important;
        z-index: 2 !important;
        pointer-events: none !important;
        width: 11rem !important;
        height: 11rem !important;
        left: 5vw !important;
        bottom: 14vh !important;
        border-radius: 50% !important;
        opacity: .86 !important;
        border: 1px solid rgba(255,255,255,.76) !important;
        background:
            radial-gradient(circle at 28% 20%, rgba(255,255,255,.96) 0 3%, rgba(255,255,255,.42) 4% 10%, transparent 19%),
            radial-gradient(circle at 66% 75%, rgba(255,204,74,.52), transparent 44%),
            radial-gradient(circle at 38% 35%, rgba(255,249,211,.82), rgba(238,174,45,.50) 52%, rgba(139,83,10,.25) 78%, rgba(255,255,255,.44)) !important;
        box-shadow:
            inset -20px -24px 35px rgba(112,38,70,.20),
            inset 14px 16px 28px rgba(255,255,255,.58),
            17vw 18vh 0 -2rem rgba(255,205,91,.76),
            35vw -4vh 0 2rem rgba(255,226,151,.68),
            54vw 25vh 0 -1rem rgba(233,168,41,.66),
            72vw 3vh 0 1rem rgba(255,236,178,.70),
            86vw 31vh 0 -2.5rem rgba(247,188,58,.74),
            0 25px 45px rgba(136,84,16,.20) !important;
        filter: drop-shadow(0 18px 20px rgba(116,44,76,.16)) !important;
        animation: snap-visible-pink-float 9s ease-in-out infinite alternate !important;
        will-change: transform !important;
    }

    [data-testid="stAppViewContainer"]::after {
        width: 7rem !important;
        height: 7rem !important;
        left: 17vw !important;
        bottom: 52vh !important;
        opacity: .72 !important;
        box-shadow:
            inset -14px -18px 28px rgba(112,38,70,.18),
            inset 10px 12px 20px rgba(255,255,255,.62),
            21vw 7vh 0 -1.5rem rgba(255,216,119,.72),
            40vw 24vh 0 .5rem rgba(225,158,34,.62),
            59vw -3vh 0 2rem rgba(255,231,164,.68),
            76vw 18vh 0 -1rem rgba(244,183,49,.70) !important;
        animation-duration: 12s !important;
        animation-delay: -5s !important;
    }

    [data-testid="stAppViewContainer"]::before,
    [data-testid="stAppViewContainer"]::after {
        border-color: rgba(255,190,184,.84) !important;
        background: radial-gradient(circle at 28% 20%,rgba(255,255,255,.98) 0 4%,rgba(255,220,212,.55) 5% 10%,transparent 18%),radial-gradient(circle at 66% 75%,rgba(255,52,45,.42),transparent 44%),radial-gradient(circle at 38% 35%,rgba(255,148,132,.74),rgba(205,14,31,.62) 52%,rgba(82,0,15,.60) 78%,rgba(255,76,63,.48)) !important;
        box-shadow: inset -18px -22px 32px rgba(72,0,13,.38),inset 13px 15px 26px rgba(255,223,216,.52),17vw 18vh 0 -2rem rgba(214,26,38,.68),35vw -4vh 0 2rem rgba(255,109,91,.55),54vw 25vh 0 -1rem rgba(139,0,24,.62),72vw 3vh 0 1rem rgba(255,135,116,.54),86vw 31vh 0 -2.5rem rgba(190,13,34,.66),0 25px 45px rgba(80,0,17,.24) !important;
    }
    @keyframes snap-visible-pink-float {
        0% { transform: translate3d(-1vw, 2vh, 0) scale(.94) rotate(-3deg); }
        45% { transform: translate3d(2vw, -5vh, 0) scale(1.04) rotate(4deg); }
        100% { transform: translate3d(-1.5vw, -10vh, 0) scale(.98) rotate(-2deg); }
    }

    .snap-floating-icons span {
        opacity: .28;
        transform: scale(.78);
    }

    .snap-particles i {
        opacity: .24;
    }

    .snap-counter-card,
    .snap-skeleton-card {
        min-height: unset;
    }

    .snap-home-note {
        text-align: center;
        color: #52607d;
        font-weight: 700;
        margin: -.35rem 0 1rem;
    }

    @keyframes snap-page-enter {
        from { opacity: 0; transform: translateY(14px) scale(.992); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }

    @keyframes snap-soft-rise {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes snap-particle-drift {
        0% { transform: translate3d(0, 0, 0) scale(.75); opacity: 0; }
        15% { opacity: .5; }
        100% { transform: translate3d(3vw, -110vh, 0) scale(1.2); opacity: 0; }
    }

    @keyframes snap-ai-float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }

    @keyframes snap-shimmer {
        0% { transform: translateX(-100%); }
        55%, 100% { transform: translateX(100%); }
    }

    @keyframes snap-counter-pop {
        0% { opacity: 0; transform: translateY(16px) scale(.72); }
        70% { transform: translateY(-2px) scale(1.08); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }

    @keyframes snap-loading-skeleton {
        0% { background-position: 220% 0; }
        100% { background-position: -220% 0; }
    }

    @media (max-width: 768px) {
        .snap-ai-float {
            right: .75rem;
            bottom: .75rem;
            padding: .55rem;
        }

        .snap-ai-float-text {
            display: none;
        }

        .snap-particles i:nth-child(n+4) {
            display: none;
        }
    }
</style>
"""

_UI_ENHANCEMENTS_HTML = """
<div class="snap-pink-bubbles" aria-hidden="true">
    <span></span><span></span><span></span><span></span><span></span>
    <span></span><span></span><span></span><span></span>
</div>
<div class="snap-particles" aria-hidden="true">
    <i></i><i></i><i></i><i></i><i></i><i></i>
</div>
<div class="snap-ai-float" aria-hidden="true">
    <span class="snap-ai-float-bot">AI</span>
    <span class="snap-ai-float-text"><span>Ask SnapClass</span><span>Assistant ready</span></span>
</div>
"""

_FLOATING_ICONS_HTML = """
<div class="snap-floating-icons" aria-hidden="true">
    <span>
        <svg viewBox="0 0 64 64" role="img">
            <defs><linearGradient id="capGrad" x1="0" x2="1"><stop stop-color="#ff2d75"/><stop offset="1" stop-color="#18c7ff"/></linearGradient></defs>
            <path fill="url(#capGrad)" d="M32 10 4 24l28 14 28-14L32 10Z"/>
            <path fill="#7c4dff" d="M15 31v11c0 6 8 11 17 11s17-5 17-11V31L32 40 15 31Z"/>
            <circle cx="53" cy="31" r="3" fill="#ffd000"/>
            <path stroke="#ffd000" stroke-width="4" stroke-linecap="round" d="M53 33v12"/>
        </svg>
    </span>
    <span>
        <svg viewBox="0 0 64 64" role="img">
            <defs><linearGradient id="bookGrad" x1="0" x2="1"><stop stop-color="#18c7ff"/><stop offset="1" stop-color="#7c4dff"/></linearGradient></defs>
            <path fill="url(#bookGrad)" d="M13 10h27a8 8 0 0 1 8 8v36H20a7 7 0 0 1-7-7V10Z"/>
            <path fill="#fff" opacity=".76" d="M22 20h17v4H22zm0 10h17v4H22z"/>
            <path fill="#ff8a00" d="M45 15h6v39l-3-3-3 3V15Z"/>
        </svg>
    </span>
    <span>
        <svg viewBox="0 0 64 64" role="img">
            <defs><linearGradient id="botGrad" x1="0" x2="1"><stop stop-color="#ffffff"/><stop offset="1" stop-color="#8be8ff"/></linearGradient></defs>
            <rect x="13" y="20" width="38" height="30" rx="12" fill="url(#botGrad)"/>
            <path stroke="#7c4dff" stroke-width="4" stroke-linecap="round" d="M32 13v7"/>
            <circle cx="24" cy="34" r="4" fill="#ff2d75"/>
            <circle cx="40" cy="34" r="4" fill="#18c7ff"/>
            <path stroke="#26345d" stroke-width="3" stroke-linecap="round" d="M25 43h14"/>
        </svg>
    </span>
    <span>
        <svg viewBox="0 0 64 64" role="img">
            <defs><linearGradient id="sparkGrad" x1="0" x2="1"><stop stop-color="#ffd000"/><stop offset="1" stop-color="#ff2d75"/></linearGradient></defs>
            <path fill="url(#sparkGrad)" d="M32 5 39 25l20 7-20 7-7 20-7-20-20-7 20-7 7-20Z"/>
            <circle cx="50" cy="14" r="5" fill="#18c7ff"/>
            <circle cx="14" cy="50" r="4" fill="#7c4dff"/>
        </svg>
    </span>
    <span>
        <svg viewBox="0 0 64 64" role="img">
            <defs><linearGradient id="brainGrad" x1="0" x2="1"><stop stop-color="#ff9fc6"/><stop offset="1" stop-color="#7c4dff"/></linearGradient></defs>
            <path fill="url(#brainGrad)" d="M24 12c-7 0-12 5-12 12 0 2 .4 4 1.3 5.6A12 12 0 0 0 16 53h15V12h-7Zm16 0h-7v41h15a12 12 0 0 0 2.7-23.4A12 12 0 0 0 40 12Z"/>
            <path stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".72" d="M24 22c-4 1-6 4-6 8m22-8c4 1 6 4 6 8M25 42h14"/>
        </svg>
    </span>
</div>
"""


def _theme_accents():
    palette = st.session_state.get("theme_palette", "Candy Sky")
    palettes = {
        "Candy Sky": ("#ff2d75", "#18c7ff", "#7c4dff"),
        "Sunset Glow": ("#ff512f", "#f09819", "#ff2d75"),
        "Ocean Mint": ("#00c6ff", "#00d084", "#7c4dff"),
        "Royal Purple": ("#7c4dff", "#b721ff", "#21d4fd"),
    }
    return palettes.get(palette, palettes["Candy Sky"])


def _background_css():
    accent_a, accent_b, accent_c = _theme_accents()

    if st.session_state.get("dark_mode", False):
        css = _BACKGROUND_CSS.replace(
            "linear-gradient(120deg, rgba(255,182,218,.62), rgba(203,239,255,.62), rgba(255,244,172,.45), rgba(221,203,255,.54))",
            "linear-gradient(120deg, rgba(57,8,45,.84), rgba(8,54,86,.82), rgba(91,52,12,.64), rgba(30,19,72,.80))",
        )
        css = css.replace("rgba(255, 255, 255, .42)", "rgba(8, 18, 38, .52)")
        css = css.replace("rgba(255, 255, 255, .58)", "rgba(150, 211, 255, .22)")
        css = css.replace("opacity: .72;", "opacity: .50;")
        css = css.replace("opacity: .60;", "opacity: .42;")
    else:
        css = _BACKGROUND_CSS

    ui_css = (
        _UI_ENHANCEMENTS_CSS
        .replace("__ACCENT_A__", accent_a)
        .replace("__ACCENT_B__", accent_b)
        .replace("__ACCENT_C__", accent_c)
    )
    return (css + ui_css).replace("__CLASSROOM_IMAGE__", BACKGROUND_IMAGE_URL)


def style_background_home():
    st.markdown(_background_css(), unsafe_allow_html=True)
    st.html(_FLOATING_ICONS_HTML)
    st.markdown(_UI_ENHANCEMENTS_HTML, unsafe_allow_html=True)


def style_background_dashboard():
    st.markdown(_background_css(), unsafe_allow_html=True)
    st.html(_FLOATING_ICONS_HTML)
    st.markdown(_UI_ENHANCEMENTS_HTML, unsafe_allow_html=True)


def style_base_layout():
    st.sidebar.toggle("Dark mode", key="dark_mode")
    st.sidebar.selectbox(
        "Theme customizer",
        ["Candy Sky", "Sunset Glow", "Ocean Mint", "Royal Purple"],
        key="theme_palette",
    )

    if not st.session_state.get("ui_welcome_toast_shown"):
        st.toast("SnapClass UI enhancements loaded ?")
        st.session_state.ui_welcome_toast_shown = True




