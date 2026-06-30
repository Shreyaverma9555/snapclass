import streamlit as st


COLLEGE_ICON_HTML = """
<img class="snap-college-icon" src="/app/static/snapclass-college-icon.png" alt="College icon" />
"""
SNAPCLASS_TITLE_STYLE = """
<style>
    .snap-top-hero-art {
        position: relative;
        left: 50%;
        width: min(900px, calc(100vw - 4rem));
        margin: .55rem 0 1.4rem;
        transform: translateX(-50%);
        isolation: isolate;
        padding: .45rem;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,.86);
        border-radius: 32px;
        background: linear-gradient(145deg,rgba(255,255,255,.78),rgba(226,220,255,.48));
        box-shadow: 0 24px 58px rgba(61,49,135,.22), inset 0 1px 0 rgba(255,255,255,.92);
        backdrop-filter: blur(14px);
    }

    .snap-top-hero-art::before {
        content: "";
        position: absolute;
        inset: 8% 6%;
        z-index: -1;
        border-radius: 48%;
        background: radial-gradient(ellipse, rgba(139,91,255,.22), rgba(255,93,190,.12) 45%, transparent 72%);
        filter: blur(25px);
    }

    .snap-top-hero-art img {
        display: block;
        width: 100%;
        height: auto;
        max-height: none;
        object-fit: contain;
        object-position: center center;
        border-radius: 25px;
        filter: brightness(1.16) saturate(.80) contrast(.90) drop-shadow(0 22px 38px rgba(50,39,126,.16));
        animation: snap-top-art-enter .8s cubic-bezier(.2,.8,.2,1) both, snap-hero-breathe 10s ease-in-out .8s infinite alternate;
    }

    .snap-hero-visuals{position:absolute;inset:0;z-index:3;overflow:hidden;border-radius:28px;pointer-events:none}.snap-hero-spark{position:absolute;width:.65rem;height:.65rem;border-radius:50%;background:radial-gradient(circle,#fff 0 18%,#77ddff 34%,#985bff 62%,transparent 72%);box-shadow:0 0 14px #68cfff,0 0 26px #944fff73;animation:snap-hero-sparkle 4s ease-in-out infinite}.snap-hero-spark:nth-child(1){left:54%;top:16%;animation-delay:-.8s}.snap-hero-spark:nth-child(2){left:68%;top:28%;animation-delay:-2.4s;transform:scale(.65)}.snap-hero-spark:nth-child(3){left:88%;top:13%;animation-delay:-1.6s;transform:scale(.8)}.snap-hero-spark:nth-child(4){left:77%;top:67%;animation-delay:-3.1s;transform:scale(.55)}.snap-hero-spark:nth-child(5){left:47%;top:73%;animation-delay:-2s;transform:scale(.7)}
    .snap-hero-orbit{position:absolute;right:10.5%;top:16%;width:16%;aspect-ratio:1;border:1px solid #635bff47;border-left-color:#ff48c19e;border-radius:50%;box-shadow:0 0 28px #597eff29,inset 0 0 22px #ffffff38;animation:snap-hero-orbit-spin 8s linear infinite}.snap-hero-orbit::after{content:"";position:absolute;width:.7rem;height:.7rem;left:10%;top:12%;border-radius:50%;background:#ff65cb;box-shadow:0 0 15px #ff65cb}.snap-hero-sheen{position:absolute;inset:-30% auto -30% -28%;width:18%;transform:rotate(14deg);background:linear-gradient(90deg,transparent,#ffffff47,transparent);filter:blur(5px);animation:snap-hero-sheen 7s ease-in-out infinite}
    @keyframes snap-hero-sparkle{0%,100%{opacity:.18;translate:0 7px;scale:.65}45%{opacity:1;translate:7px -12px;scale:1.18}65%{opacity:.55;translate:-4px -18px;scale:.82}}@keyframes snap-hero-orbit-spin{to{transform:rotate(360deg)}}@keyframes snap-hero-sheen{0%,18%{left:-28%;opacity:0}42%{opacity:.8}68%,100%{left:112%;opacity:0}}@keyframes snap-hero-breathe{from{transform:scale(1)}to{transform:scale(1.018)}}
    .snap-top-hero-caption {
        display: inline-flex;
        align-items: center;
        gap: .4rem;
        margin-bottom: .65rem;
        padding: .4rem .8rem;
        border: 1px solid rgba(255,255,255,.76);
        border-radius: 999px;
        color: #6540e5;
        background: rgba(255,255,255,.68);
        box-shadow: 0 10px 26px rgba(93,65,187,.14);
        font-size: .72rem;
        font-weight: 900;
        letter-spacing: .06em;
        text-transform: uppercase;
    }

    @keyframes snap-top-art-enter {
        from { opacity: 0; transform: translateY(-18px) scale(.97); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    .snap-home-header {
        text-align: center;
        padding: 0 0 1.5rem;
        transform: translateY(-2.75rem);
        margin-bottom: -2.75rem;
    }
    .snapclass-hero-title {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: .8rem;
        margin: 0;
    }

    .snapclass-title {
        margin: 0;
        font-family: 'Trebuchet MS', 'Segoe UI', cursive, sans-serif;
        font-size: clamp(4.6rem, 10vw, 8.8rem);
        font-weight: 900;
        letter-spacing: .03em;
        line-height: .95;
        background: linear-gradient(90deg, #ff2d75, #ff8a00, #ffd000, #18c7ff, #7c4dff, #ff2d75);
        background-size: 320% 100%;
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        color: transparent !important;
        text-shadow: 0 8px 24px rgba(255, 45, 117, .22);
        animation: snapclass-rainbow 5s ease-in-out infinite alternate;
    }

    .snap-ai-badge {
        position: relative;
        display: inline-grid;
        place-items: center;
        width: clamp(5rem, 8vw, 7rem);
        height: clamp(5rem, 8vw, 7rem);
        border-radius: 1.6rem;
        background: linear-gradient(145deg, rgba(255,255,255,.90), rgba(172,231,255,.60));
        border: 1px solid rgba(255,255,255,.76);
        box-shadow: 0 18px 42px rgba(35,111,190,.26), inset 0 1px 0 rgba(255,255,255,.86);
        animation: ai-bot-float 2.6s ease-in-out infinite;
        overflow: visible;
    }

    .snap-ai-badge::after {
        content: "EDU";
        position: absolute;
        right: -.48rem;
        bottom: -.36rem;
        padding: .18rem .38rem;
        border-radius: 999px;
        color: white;
        background: linear-gradient(90deg, #ff2d75, #7c4dff, #18c7ff);
        font: 900 .56rem/1 'Segoe UI', sans-serif;
        letter-spacing: .04em;
        box-shadow: 0 8px 18px rgba(124,77,255,.30);
    }

    .snap-ai-badge::before {
        content: "";
        position: absolute;
        inset: -.45rem;
        border-radius: 1.9rem;
        background: linear-gradient(90deg, rgba(255,45,117,.30), rgba(24,199,255,.26), rgba(124,77,255,.26));
        filter: blur(12px);
        z-index: -1;
        animation: ai-glow-pulse 2.6s ease-in-out infinite;
    }

    .snap-college-icon {
        width: 100%;
        height: 100%;
        display: block;
        border-radius: 1.35rem;
        object-fit: cover;
        filter: drop-shadow(0 10px 16px rgba(41,76,150,.18));
    }

    .ai-orbit-one { transform-origin: 48px 48px; animation: ai-orbit-spin 3.8s linear infinite; }
    .ai-orbit-two { transform-origin: 48px 48px; animation: ai-orbit-spin 5.5s linear infinite reverse; }
    .ai-eye { animation: ai-eye-blink 3.2s ease-in-out infinite; transform-origin: center; }
    .ai-eye-pink { animation-delay: .1s; }
    .ai-spark { animation: ai-spark-pop 1.9s ease-in-out infinite; transform-origin: center; }
    .ai-spark-two { animation-delay: .5s; }

    .snapclass-subtitle {
        margin: .5rem 0 0;
        color: #8b0000 !important;
        font-weight: 800;
        letter-spacing: .03em;
        text-shadow: 0 2px 10px rgba(255,255,255,.65);
    }

    .snap-top-caption {
        width: min(720px, calc(100% - 1rem));
        margin: 1rem auto 0;
        text-align: center;
        color: #4f536b;
        font-size: clamp(.9rem, 1.8vw, 1.05rem);
        line-height: 1.55;
    }

    .snap-top-caption p { margin: 0; }
    .snap-top-caption strong { color: #5738de; font-weight: 900; }

    .snap-handwritten-line {
        position: relative;
        display: inline-block;
        margin-top: .55rem;
        padding: 0 .4rem .28rem;
        color: #22284c;
        font-family: 'Segoe Print', 'Bradley Hand', 'Comic Sans MS', cursive;
        font-size: clamp(1.05rem, 2.5vw, 1.55rem);
        font-style: italic;
        transform: rotate(-1deg);
    }

    .snap-handwritten-line::after {
        content: "";
        position: absolute;
        left: 3%; right: 3%; bottom: 0;
        height: .22rem;
        border-radius: 999px;
        background: linear-gradient(90deg, #ff4fbd, #ff84cd, #ff4fbd);
        transform: rotate(.7deg);
        box-shadow: 0 3px 9px rgba(255,79,189,.25);
    }

    .snap-caption-spark { color: #d63cff; font-style: normal; }
    .snap-caption-heart { color: #ff54b0; font-style: normal; margin-left: .25rem; }
    .snapclass-dashboard-title-wrap {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: .55rem;
    }

    .snapclass-dashboard-title {
        margin: 0;
        text-align: center;
        font-family: 'Trebuchet MS', 'Segoe UI', cursive, sans-serif;
        font-size: 2.6rem;
        font-weight: 900;
        background: linear-gradient(90deg, #ff2d75, #ff8a00, #18c7ff, #7c4dff);
        background-size: 260% 100%;
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        color: transparent !important;
        animation: snapclass-rainbow 5s ease-in-out infinite alternate;
    }

    .snap-dashboard-ai-badge {
        position: relative;
        display: inline-grid;
        place-items: center;
        width: 2.7rem;
        height: 2.7rem;
        border-radius: 1rem;
        background: rgba(255,255,255,.76);
        box-shadow: 0 12px 26px rgba(24,199,255,.24);
        animation: ai-bot-float 2.6s ease-in-out infinite;
    }

    @media (max-width: 768px) {
        .snap-home-header { transform: translateY(-1.4rem); margin-bottom: -1.4rem; }
        .snap-top-hero-art { width: calc(100vw - 1.5rem); margin-top: .35rem; padding: .25rem; border-radius: 20px; }
        .snap-top-hero-art img { filter: brightness(1.16) saturate(.80) contrast(.90) drop-shadow(0 14px 28px rgba(50,39,126,.15)); }
        .snapclass-hero-title { gap: .45rem; flex-wrap: wrap; }
        .snapclass-title { font-size: clamp(3rem,18vw,4.8rem); line-height:1; letter-spacing:.01em; }
        .snap-ai-badge { width:4rem; height:4rem; border-radius:1.2rem; }
        .snapclass-dashboard-title-wrap { gap:.35rem; flex-wrap:wrap; }
        .snapclass-dashboard-title { font-size:2rem; }
        .snap-dashboard-ai-badge { width:2.25rem; height:2.25rem; }
    }
    @media (max-width: 420px) {
        .snapclass-title {
            font-size: clamp(2.7rem, 17vw, 3.9rem);
        }

        .snap-ai-badge {
            width: 3.35rem;
            height: 3.35rem;
        }

        .snapclass-subtitle {
            font-size: .85rem;
        }
    }

    @keyframes snapclass-rainbow {
        from { background-position: 0% 50%; }
        to { background-position: 100% 50%; }
    }

    @keyframes ai-bot-float {
        0%, 100% { transform: translateY(0) rotate(-4deg) scale(1); }
        50% { transform: translateY(-.45rem) rotate(5deg) scale(1.04); }
    }

    @keyframes ai-glow-pulse {
        0%, 100% { opacity: .45; transform: scale(.92); }
        50% { opacity: .90; transform: scale(1.08); }
    }

    @keyframes ai-orbit-spin {
        to { transform: rotate(360deg); }
    }

    @keyframes ai-eye-blink {
        0%, 44%, 52%, 100% { transform: scaleY(1); }
        48% { transform: scaleY(.16); }
    }

    @keyframes ai-spark-pop {
        0%, 100% { opacity: .45; transform: scale(.75); }
        50% { opacity: 1; transform: scale(1.25); }
    }
</style>
"""


def header_home():
    st.html(
        SNAPCLASS_TITLE_STYLE
        + f"""
        <div class="snap-home-header">
            <div class="snapclass-hero-title">
                <h1 class="snapclass-title">SnapClass</h1>
                <span class="snap-ai-badge">{COLLEGE_ICON_HTML}</span>
            </div>
            <div class="snap-top-hero-art">
                <img src="/app/static/snapclass-generated-top-hero-large.png?v=8" alt="Every Presence Creates Progress - SnapClass AI classroom intelligence" />
                <div class="snap-hero-visuals" aria-hidden="true"><i class="snap-hero-spark"></i><i class="snap-hero-spark"></i><i class="snap-hero-spark"></i><i class="snap-hero-spark"></i><i class="snap-hero-spark"></i><span class="snap-hero-orbit"></span><span class="snap-hero-sheen"></span></div>
            </div>
        </div>
        """,
    )


def header_dashboard():
    st.html(
        SNAPCLASS_TITLE_STYLE
        + f"""
        <div class="snapclass-dashboard-title-wrap">
            <h2 class="snapclass-dashboard-title">SnapClass</h2>
            <span class="snap-dashboard-ai-badge">{COLLEGE_ICON_HTML}</span>
        </div>
        """,
    )
