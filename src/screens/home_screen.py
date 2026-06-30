import pandas as pd
import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home


def _counter_card(label, value, caption):
    st.html(
        f"""
        <div class="snap-counter-card">
            <div class="snap-counter-number">{value}</div>
            <div style="font-weight:850; color:#17213f; margin-top:.35rem;">{label}</div>
            <div style="font-size:.86rem; color:#52607d; margin-top:.25rem;">{caption}</div>
        </div>
        """
    )



def _feature_strip():
    st.markdown("""
    <style>
    .features-showcase{position:relative;isolation:isolate;overflow:hidden;margin:2rem 0;padding:clamp(1.2rem,4vw,2.7rem);border:1px solid #ffffffcc;border-radius:36px;background:radial-gradient(circle at 5% 0,#ff3cac28,transparent 30%),radial-gradient(circle at 95% 10%,#6048ff32,transparent 32%),#ffffff8f;box-shadow:0 28px 70px #49369e32;backdrop-filter:blur(22px)}
    .bubble-orb{position:absolute;z-index:0;pointer-events:none;border-radius:50%;border:1px solid #ffffffd9;background:radial-gradient(circle at 27% 20%,#fff 0 3%,#ffffff88 4% 10%,transparent 19%),radial-gradient(circle at 68% 74%,#f173a875,transparent 43%),radial-gradient(circle at 40% 36%,#ffe9f3d9,#dc6f9c8c 54%,#792d505e 78%,#ffffff70);box-shadow:inset -16px -20px 30px #74264238,inset 12px 14px 24px #ffffffa6,0 20px 38px #7d31523b;animation:featureBubbleFloat 5.5s ease-in-out infinite alternate}.bubble-orb::after{content:"";position:absolute;inset:9%;border-radius:50%;border-top:2px solid #ffffffc7}.bubble-orb.yellow{background:radial-gradient(circle at 27% 20%,#fff 0 3%,#fffdf0a8 4% 11%,transparent 20%),radial-gradient(circle at 68% 74%,#ffe8a85c,transparent 43%),radial-gradient(circle at 40% 36%,#fffef2f2,#f8e7ad8c 54%,#d5ad5b42 78%,#ffffffa0);box-shadow:inset -12px -15px 24px #bb8d3030,inset 11px 13px 22px #fffffff0,0 18px 34px #c8a45a2e}.bubble-orb.peach{background:radial-gradient(circle at 28% 20%,#fff8f4 0 6%,transparent 18%),radial-gradient(circle at 38% 34%,#ffd8c8,#f2a78f 58%,#b85f655f 86%);box-shadow:inset -13px -16px 24px #9e4f5035,inset 10px 12px 20px #fff9f0c7,0 18px 30px #814f6838}.bubble-orb.blue{background:radial-gradient(circle at 28% 20%,#ffffffd9 0 5%,transparent 18%),radial-gradient(circle at 38% 34%,#d5e8f8,#8fb5d2 58%,#596f9a70 86%);box-shadow:inset -13px -16px 24px #445a7d38,inset 10px 12px 20px #ffffffb8,0 18px 30px #4a52753b}.bubble-orb.lavender{background:radial-gradient(circle at 28% 20%,#ffffffdc 0 5%,transparent 18%),radial-gradient(circle at 38% 34%,#eee4fa,#b7a0d2 58%,#76618f66 86%);box-shadow:inset -13px -16px 24px #59466c36,inset 10px 12px 20px #ffffffc4,0 18px 30px #5e456f38}.bubble-orb.pink-solid{background:radial-gradient(circle at 28% 20%,#fff7fa 0 5%,transparent 18%),radial-gradient(circle at 38% 34%,#ffc9dc,#eb87ad 58%,#a847706b 86%);box-shadow:inset -13px -16px 24px #873a5838,inset 10px 12px 20px #ffffffc7,0 18px 30px #79324f3b}.features-showcase .bubble-orb{border:1px solid #ffc4bde8!important;background:radial-gradient(circle at 28% 20%,#fff 0 5%,transparent 18%),radial-gradient(circle at 68% 74%,#ff3b3b63,transparent 43%),radial-gradient(circle at 40% 36%,#ff9b8edb,#d51629b8 56%,#650014a6 82%,#ff554f8c)!important;box-shadow:inset -12px -15px 24px #57000f70,inset 11px 13px 22px #ffd8d0a8,0 16px 30px #7a00143d!important;filter:saturate(1.18)!important}.bubble-one{width:4rem;height:4rem;left:1%;top:5rem}.bubble-two{width:3.4rem;height:3.4rem;right:5%;top:2.2rem;animation-delay:-2s}.bubble-three{width:3.5rem;height:3.5rem;right:1%;top:43%;animation-delay:-4s}.bubble-four{width:2.5rem;height:2.5rem;left:7%;bottom:9%;animation-delay:-1s}.bubble-five{width:3rem;height:3rem;left:47%;bottom:-1rem;animation-delay:-3s}.bubble-six{width:2.2rem;height:2.2rem;left:28%;top:3%;animation-delay:-4.5s}.bubble-seven{width:3.8rem;height:3.8rem;right:25%;bottom:5%;animation-delay:-2.5s}.bubble-eight{width:2.2rem;height:2.2rem;left:18%;top:48%;animation-delay:-5s}.bubble-nine{width:2rem;height:2rem;left:40%;top:18%;animation-delay:-1.5s;opacity:.75}.bubble-ten{width:3.1rem;height:3.1rem;right:14%;top:27%;animation-delay:-3.5s;opacity:.72}.bubble-eleven{width:2.4rem;height:2.4rem;left:34%;bottom:12%;animation-delay:-4.8s;opacity:.68}.bubble-twelve{width:3.6rem;height:3.6rem;right:7%;bottom:16%;animation-delay:-.8s;opacity:.7}.features-showcase>header,.features-showcase>.features-grid,.features-showcase>.future-banner,.features-showcase>.feature-stats{position:relative;z-index:1}@keyframes featureBubbleFloat{from{transform:translate3d(-5px,8px,0) scale(.96) rotate(-3deg)}to{transform:translate3d(12px,-18px,0) scale(1.05) rotate(4deg)}}
    .features-head{text-align:center;max-width:720px;margin:auto}.features-kicker{display:inline-block;padding:.45rem .85rem;border-radius:99px;background:#ffffffb8;color:#6338db;font-size:.75rem;font-weight:900;letter-spacing:.07em;text-transform:uppercase}.features-head h2{margin:.8rem 0 .45rem;color:#161936;font-size:clamp(2rem,5vw,3.5rem);line-height:1;letter-spacing:-.05em}.features-head h2 span{background:linear-gradient(90deg,#ff2783,#f19a16,#852be6,#3764f4);-webkit-background-clip:text;color:transparent}.features-head p{color:#5d6680;line-height:1.6}.features-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:.9rem;margin-top:1.5rem}.f-card{padding:1.25rem 1rem;text-align:center;border:1px solid #fff;border-radius:25px;background:linear-gradient(145deg,#ffffffe8,#f4f2ff99);box-shadow:0 15px 34px #4c428b20;transition:.25s}.f-card:hover{transform:translateY(-8px);box-shadow:0 23px 44px #523ca936}.f-icon{display:grid;place-items:center;width:4rem;height:4rem;margin:0 auto .8rem;border-radius:20px;color:#fff;font-weight:950;background:var(--c);box-shadow:0 12px 26px var(--s)}.f-card h3{margin:.2rem;color:#171a38;font-size:1rem}.f-card p{color:#69728a;font-size:.82rem;line-height:1.45}.f-card b{display:inline-block;padding:.32rem .62rem;border-radius:99px;color:#5b32ce;background:#eee8ff;font-size:.7rem}.future-banner{display:flex;align-items:center;gap:1rem;margin-top:1rem;padding:1.1rem 1.3rem;border-radius:24px;color:white;background:linear-gradient(110deg,#171b43,#30236d,#6423b3);box-shadow:0 17px 36px #2c1c7040}.future-banner i{display:grid;place-items:center;flex:0 0 3.4rem;height:3.4rem;border-radius:18px;background:linear-gradient(145deg,#df31ff,#4e6cff);font-style:normal;font-weight:900}.future-banner strong{font-size:1.1rem}.future-banner span{color:#ff67cf}.future-banner p{margin:.2rem 0 0;color:#d8dcff;font-size:.82rem}.feature-stats{display:grid;grid-template-columns:repeat(5,1fr);margin-top:1rem;padding:1rem;border-radius:24px;background:#ffffffbd}.feature-stats div{text-align:center;border-right:1px solid #756ca528}.feature-stats div:last-child{border:0}.feature-stats b{display:block;color:#5633da;font-size:1.45rem}.feature-stats small{color:#68718a;font-weight:700}@media(max-width:800px){.features-grid{grid-template-columns:repeat(2,1fr)}.feature-stats{grid-template-columns:repeat(2,1fr);gap:1rem}.feature-stats div{border:0}}@media(max-width:480px){.features-showcase{padding:1rem;border-radius:24px}.features-grid{grid-template-columns:1fr}.future-banner{align-items:flex-start}}
    </style>
    <section class="features-showcase"><div class="bubble-orb peach bubble-one"></div><div class="bubble-orb blue bubble-two"></div><div class="bubble-orb pink-solid bubble-three"></div><div class="bubble-orb lavender bubble-four"></div><div class="bubble-orb peach bubble-five"></div><div class="bubble-orb blue bubble-six"></div><div class="bubble-orb yellow bubble-seven"></div><div class="bubble-orb lavender bubble-eight"></div><div class="bubble-orb pink-solid bubble-nine"></div><div class="bubble-orb peach bubble-ten"></div><div class="bubble-orb blue bubble-eleven"></div><div class="bubble-orb lavender bubble-twelve"></div><header class="features-head"><div class="features-kicker">AI-powered attendance revolution</div><h2>See smarter. <span>Teach better.</span></h2><p>SnapClass sees beyond faces—it understands classroom patterns, turns every session into insight, and gives teachers more time to inspire.</p></header><div class="features-grid">
    <article class="f-card" style="--c:linear-gradient(145deg,#cf5bff,#7a40ef);--s:#9a46df55"><div class="f-icon">AI</div><h3>AI Chatbot</h3><p>Instant help with attendance, timetables and assignments.</p><b>Ask instantly</b></article>
    <article class="f-card" style="--c:linear-gradient(145deg,#52e5ad,#13ae7a);--s:#25bd8655"><div class="f-icon">LIVE</div><h3>Emotion Detection</h3><p>Real-time signals for better classroom understanding.</p><b>Live analysis</b></article>
    <article class="f-card" style="--c:linear-gradient(145deg,#65b5ff,#3769ef);--s:#367ce255"><div class="f-icon">PDF</div><h3>AI Reports</h3><p>Clear trends with one-click PDF and Excel exports.</p><b>View insights</b></article>
    <article class="f-card" style="--c:linear-gradient(145deg,#ffba56,#f36b29);--s:#ed7f3455"><div class="f-icon">DARK</div><h3>Comfortable Themes</h3><p>Beautiful light and dark experiences for every setting.</p><b>Make it yours</b></article></div>
    <div class="future-banner"><i>AI</i><div><strong>The future of attendance is <span>intelligent.</span></strong><p>Less admin work. Better classroom awareness. More meaningful teaching.</p></div></div>
    <div class="feature-stats"><div><b>1M+</b><small>Faces recognized</small></div><div><b>98.7%</b><small>Accuracy rate</small></div><div><b>500+</b><small>Institutions</small></div><div><b>2M+</b><small>Records</small></div><div><b>24/7</b><small>AI assistance</small></div></div></section>
    """, unsafe_allow_html=True)

    with st.expander("Preview Interactive Charts", expanded=True):
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown("##### Attendance Trend")
            trend_df = pd.DataFrame(
                {"Attendance %": [72, 78, 84, 89, 92, 88, 94]},
                index=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            )
            st.line_chart(trend_df)

            st.markdown("##### Weekly Attendance")
            weekly_df = pd.DataFrame(
                {
                    "Present": [38, 42, 45, 41],
                    "Absent": [7, 5, 3, 6],
                },
                index=["Week 1", "Week 2", "Week 3", "Week 4"],
            )
            st.bar_chart(weekly_df)

        with chart_col2:
            st.markdown("##### Emotion Distribution")
            emotion_df = pd.DataFrame(
                {"Students": [18, 7, 5, 20]},
                index=["Happy", "Sad", "Sleepy", "Neutral"],
            )
            st.bar_chart(emotion_df)

            st.markdown("##### Subject-wise Attendance")
            subject_df = pd.DataFrame(
                {"Attendance %": [91, 86, 78, 94, 82]},
                index=["Math", "Science", "English", "AI", "DBMS"],
            )
            st.bar_chart(subject_df)


def _bottom_showcase():
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"]:has(.snap-bottom-showcase) .snap-pink-bubbles{display:none!important}
        [data-testid="stAppViewContainer"]:has(.snap-bottom-showcase)::before,[data-testid="stAppViewContainer"]:has(.snap-bottom-showcase)::after{display:none!important;content:none!important;animation:none!important;box-shadow:none!important}
        .main .block-container:has(.snap-bottom-showcase),section.main>div:has(.snap-bottom-showcase),.block-container:has(.snap-bottom-showcase){padding-bottom:0!important;margin-bottom:0!important}.element-container:has(.snap-bottom-showcase),[data-testid="stElementContainer"]:has(.snap-bottom-showcase),.stMarkdown:has(.snap-bottom-showcase){position:relative!important;z-index:9999!important;isolation:isolate!important;margin-bottom:0!important;padding-bottom:0!important}.snap-bottom-showcase{position:relative;z-index:20;isolation:isolate;left:50%;width:100vw;max-width:none;transform:translateX(-50%);box-sizing:border-box;margin:2rem 0 0!important;padding:0!important;border:0;border-radius:0;background:#111;box-shadow:none;overflow:hidden}
        .snap-bottom-showcase img,.snap-bottom-showcase video{position:relative;z-index:21;display:block;width:100%;height:auto!important;min-height:0!important;margin:0!important;padding:0!important;border-radius:0;transition:transform .5s ease,filter .5s ease;animation:snap-bottom-cinema 12s ease-in-out infinite alternate}.snap-bottom-showcase:hover img,.snap-bottom-showcase:hover video{filter:saturate(1.08) brightness(1.04)}
        .snap-bottom-visuals{position:absolute;inset:0;z-index:23;overflow:hidden;border-radius:0;pointer-events:none}.snap-bottom-visuals::before{content:"";position:absolute;top:-35%;bottom:-35%;left:-25%;width:16%;transform:rotate(15deg);background:linear-gradient(90deg,transparent,#ffffff4f,transparent);filter:blur(5px);animation:snap-bottom-sheen 7s ease-in-out infinite}.snap-bottom-visuals i{position:absolute;width:.5rem;height:.5rem;border-radius:50%;background:radial-gradient(circle,#fff 0 18%,#79e5ff 36%,#985cff 64%,transparent 73%);box-shadow:0 0 13px #70dfff;animation:snap-bottom-particle 5s ease-in-out infinite}.snap-bottom-visuals i:nth-child(1){left:8%;top:72%;animation-delay:-1s}.snap-bottom-visuals i:nth-child(2){left:32%;top:28%;animation-delay:-3.4s;scale:.65}.snap-bottom-visuals i:nth-child(3){left:58%;top:76%;animation-delay:-2s;scale:.8}.snap-bottom-visuals i:nth-child(4){left:78%;top:21%;animation-delay:-4.2s;scale:.55}.snap-bottom-visuals i:nth-child(5){left:92%;top:64%;animation-delay:-.7s;scale:.7}@keyframes snap-bottom-cinema{from{transform:scale(1.005) translate3d(-.25%,.15%,0)}to{transform:scale(1.035) translate3d(.35%,-.25%,0)}}@keyframes snap-bottom-sheen{0%,18%{left:-25%;opacity:0}42%{opacity:.75}68%,100%{left:112%;opacity:0}}@keyframes snap-bottom-particle{0%,100%{opacity:.18;translate:0 10px;scale:.65}48%{opacity:1;translate:8px -15px;scale:1.15}75%{opacity:.45;translate:-5px -24px;scale:.8}}        .snap-bottom-showcase-label{position:absolute;z-index:22;left:50%;bottom:1.4rem;transform:translateX(-50%);padding:.55rem 1rem;border:1px solid #ffffffbd;border-radius:99px;color:white;background:#2a186fb8;box-shadow:0 10px 28px #26136952;backdrop-filter:blur(12px);font-size:.78rem;font-weight:850;white-space:nowrap}
        @media(max-width:600px){.snap-bottom-showcase{width:100vw;margin-top:1.25rem;padding:0;border-radius:0}.snap-bottom-showcase img,.snap-bottom-showcase video{border-radius:0}.snap-bottom-showcase-label{bottom:.75rem;font-size:.64rem;padding:.4rem .7rem}}
        </style>
        <section class="snap-bottom-showcase"><div class="snap-bottom-showcase-label">The complete SnapClass experience</div><video autoplay muted loop playsinline preload="metadata" poster="/app/static/snapclass-classroom-bottom.png?v=1" aria-label="Animated SnapClass teacher, students and AI classroom showcase"><source src="/app/static/snapclass-classroom-animated.mp4?v=1" type="video/mp4"></video><div class="snap-bottom-visuals" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div></section>
        """,
        unsafe_allow_html=True,
    )

def home_screen():
    style_base_layout()
    style_background_home()
    header_home()

    st.markdown(
        """
        <style>
        .portal-role-head{text-align:center;margin:.25rem auto .8rem}.portal-role-head h2{margin:0 0 .7rem;color:#171b3b;font-size:clamp(1.8rem,4vw,2.5rem);font-weight:900}.portal-mascot{display:block;width:min(230px,72%);height:230px;object-fit:contain;margin:0 auto;filter:drop-shadow(0 18px 24px rgba(61,49,135,.22));transition:transform .3s ease}.portal-mascot:hover{transform:translateY(-7px) scale(1.04)}@media(max-width:600px){.portal-mascot{width:min(200px,68%);height:200px}}
        </style>
        """,
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.html('<div class="portal-role-head"><h2>I&apos;m Student</h2><img class="portal-mascot" src="/app/static/student-mascot.png?v=1" alt="Student portal mascot"></div>')
        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.toast("Opening Student Portal")
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.html('<div class="portal-role-head"><h2>I&apos;m Teacher</h2><img class="portal-mascot" src="/app/static/teacher-mascot.png?v=1" alt="Teacher portal mascot"></div>')
        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.toast("Opening Teacher Portal")
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    _feature_strip()
    _bottom_showcase()
    footer_home()
