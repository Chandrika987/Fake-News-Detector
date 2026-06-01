from pathlib import Path
import time

import requests
import streamlit as st


BACKEND_URL = "http://localhost:8000"


st.set_page_config(
    page_title="The Daily Truth Checker",
    page_icon="DTC",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def load_css() -> None:
    project_root = Path(__file__).resolve().parent.parent
    for css_path in (
        project_root / "assets" / "styles.css",
        project_root / "assests" / "styles.css",
    ):
        if css_path.exists():
            st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
            break


def render_confidence(fake_probability: float, real_probability: float) -> None:
    fake_score = fake_probability * 100
    real_score = real_probability * 100
    leading_label = "Real News" if real_score >= fake_score else "Fake News"
    leading_score = max(real_score, fake_score)

    st.markdown(
        f"""
        <section class="confidence-card">
          <div>
            <p class="eyebrow">Confidence analysis</p>
            <h3>{leading_score:.2f}% {leading_label}</h3>
          </div>
          <div class="meter-group" aria-label="Prediction probability visualization">
            <div class="meter-row">
              <div class="meter-label">
                <span>Fake News</span>
                <strong>{fake_score:.2f}%</strong>
              </div>
              <div class="meter-track">
                <div class="meter-fill fake-fill" style="width: {fake_score:.2f}%"></div>
              </div>
            </div>
            <div class="meter-row">
              <div class="meter-label">
                <span>Real News</span>
                <strong>{real_score:.2f}%</strong>
              </div>
              <div class="meter-track">
                <div class="meter-fill real-fill" style="width: {real_score:.2f}%"></div>
              </div>
            </div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


load_css()

st.markdown(
    """
    <nav class="top-nav">
      <div class="brand-mark">
        <span class="brand-orb"></span>
        <span>The Daily Truth Checker</span>
      </div>
      <div class="nav-links">
        <span>AI Detection</span>
        <span>Live Analysis</span>
        <span>Dark Mode</span>
      </div>
    </nav>

    <main class="page-shell">
      <section class="hero-section">
        <div class="hero-copy">
          <p class="eyebrow">AI-powered media integrity dashboard</p>
          <h1>Verify news authenticity with a modern intelligence layer.</h1>
          <p class="hero-text">
            Paste a headline or article and receive a clear fake-versus-real assessment,
            confidence visualization, and polished decision summary.
          </p>
          <div class="hero-actions">
            <a href="#analysis-panel" class="primary-link">Start analysis</a>
            <span class="system-status"><span></span>Backend endpoint unchanged</span>
          </div>
        </div>
        <div class="hero-visual glass-card">
          <div class="signal-header">
            <span>Truth Signal</span>
            <strong>Realtime</strong>
          </div>
          <div class="signal-chart">
            <span class="bar bar-one"></span>
            <span class="bar bar-two"></span>
            <span class="bar bar-three"></span>
            <span class="bar bar-four"></span>
          </div>
          <div class="signal-row">
            <span>Source consistency</span>
            <strong>High</strong>
          </div>
          <div class="signal-row">
            <span>Manipulation risk</span>
            <strong>Scanning</strong>
          </div>
        </div>
      </section>

      <section class="stats-grid" aria-label="Dashboard statistics">
        <div class="stat-card glass-card">
          <span>Model Task</span>
          <strong>Binary Detection</strong>
        </div>
        <div class="stat-card glass-card">
          <span>Output</span>
          <strong>Fake / Real</strong>
        </div>
        <div class="stat-card glass-card">
          <span>Confidence</span>
          <strong>Probability View</strong>
        </div>
      </section>
    """,
    unsafe_allow_html=True,
)

st.markdown('<section id="analysis-panel" class="analysis-panel glass-card">', unsafe_allow_html=True)
st.markdown(
    """
    <div class="section-heading">
      <p class="eyebrow">Detection workspace</p>
      <h2>Analyze a news article</h2>
      <p>Enter the content below. The existing backend prediction API handles the classification.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

user_input = st.text_area(
    "News article or headline",
    height=220,
    placeholder="Paste a headline, article excerpt, or full news story here...",
)

analyze = st.button("Check Authenticity", type="primary", use_container_width=True)
st.markdown("</section>", unsafe_allow_html=True)

if analyze:
    if not user_input.strip():
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing credibility signals..."):
            time.sleep(0.3)
            try:
                resp = requests.post(f"{BACKEND_URL}/predict", json={"text": user_input}, timeout=20)
                resp.raise_for_status()
                data = resp.json()

                prediction = data.get("prediction")
                fake_p = data.get("fake_probability")
                real_p = data.get("real_probability")

                if not prediction:
                    st.error("The backend response did not include a prediction.")
                    st.stop()

                if fake_p is not None and real_p is not None:
                    fake_p = float(fake_p)
                    real_p = float(real_p)

                if prediction.lower() == "real":
                    st.markdown(
                        """
                        <section class="result-card result-real">
                          <span class="result-badge">REAL NEWS</span>
                          <h2>Likely authentic reporting</h2>
                          <p>The article patterns align more strongly with real news in the current model output.</p>
                        </section>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        """
                        <section class="result-card result-fake">
                          <span class="result-badge">FAKE NEWS</span>
                          <h2>Potential misinformation detected</h2>
                          <p>The article patterns align more strongly with fake news in the current model output.</p>
                        </section>
                        """,
                        unsafe_allow_html=True,
                    )

                if fake_p is not None and real_p is not None:
                    render_confidence(fake_p, real_p)

            except Exception as ex:
                st.error(f"Error: {ex}")

st.markdown(
    """
      <footer class="footer-section">
        <span>The Daily Truth Checker</span>
        <span>Frontend refresh only. Backend behavior and prediction logic remain unchanged.</span>
      </footer>
    </main>
    """,
    unsafe_allow_html=True,
)
