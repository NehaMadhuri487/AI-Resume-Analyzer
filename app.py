import streamlit as st # type: ignore
import plotly.graph_objects as go # type: ignore
from backend import parser, ai_engine, scorer, utils

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
utils.apply_custom_css()

# ------------------ HEADER ------------------
st.markdown("""
    <div style="text-align: center; margin-bottom: 30px; margin-top: -30px;">
        <h1 style="font-size: 2.8rem; background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🎯 AI Resume Analyzer
        </h1>
        <p style="font-size: 1.1rem; color: #e2e8f0; max-width: 700px; margin: 10px auto; font-weight: 400;">
            Upload your resume and target job description to get ATS insights, keyword analysis, and improvement suggestions.
        </p>
    </div>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
st.sidebar.header("Upload Inputs")

uploaded_resume = st.sidebar.file_uploader(
    "Upload Resume",
    type=["pdf", "docx", "txt"],
    help="Supported formats: PDF, DOCX, TXT"
)

job_desc_input = st.sidebar.text_area(
    "Job Description",
    placeholder="Paste the job description here...",
    height=250
)

analyze_btn = st.sidebar.button(
    "Run Analysis",
    type="primary",
    use_container_width=True,
    disabled=not (uploaded_resume and job_desc_input.strip())
)

# ------------------ MAIN CONTENT ------------------
if analyze_btn:
    with st.spinner("Analyzing your resume against the job description..."):
        try:
            # Step 1: Parse resume
            resume_text = parser.extract_text(uploaded_resume, uploaded_resume.name)
            clean_resume = utils.clean_text(resume_text)
            clean_jd = utils.clean_text(job_desc_input)

            # Step 2: Run Gemini AI analysis
            results = ai_engine.analyze_resume(clean_resume, clean_jd)

            # Step 3: Compute hybrid ATS score
            hybrid_score = scorer.compute_hybrid_score(
                results.get("ats_score", 0),
                results.get("keyword_analysis", {}).get("matched", []),
                results.get("keyword_analysis", {}).get("missing", [])
            )

            st.success("✅ Analysis complete! Results will be displayed below.")

            # ------------------ SCORE DASHBOARD ------------------
            col1, col2 = st.columns([1, 1])
            with col1:
                overall_score = hybrid_score["overall_score"]
                bar_color = "#10b981" if overall_score >= 85 else "#6366f1" if overall_score >= 70 else "#ef4444"

                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=overall_score,
                    title={'text': "Hybrid ATS Score", 'font': {'size': 20, 'color': '#ffffff'}},
                    number={'font': {'color': '#f8fafc', 'size': 50}},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': bar_color},
                        'steps': [
                            {'range': [0, 60], 'color': 'rgba(239, 68, 68, 0.15)'},
                            {'range': [60, 85], 'color': 'rgba(245, 158, 11, 0.15)'},
                            {'range': [85, 100], 'color': 'rgba(16, 185, 129, 0.15)'}
                        ],
                    }
                ))
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=260)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.08); padding: 20px; border-radius: 12px;">
                        <h3 style="color: #ffffff; margin-top: 0;">Matching Status: 
                            <span style="background:#6366f1; color:white; padding:4px 10px; border-radius:6px;">
                                {results.get("match_status", "N/A")}
                            </span>
                        </h3>
                        <p style="color: #e2e8f0; font-size: 0.95rem; font-weight: 400;">
                            {results.get("summary", "No summary available.")}
                        </p>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                            <div>
                                <div style="font-size: 0.85rem; font-weight: 600; color: #f8fafc;">Semantic Match</div>
                                <div style="font-size: 1.4rem; font-weight: 700; color: #a855f7;">{hybrid_score["semantic_score"]}%</div>
                            </div>
                            <div>
                                <div style="font-size: 0.85rem; font-weight: 600; color: #f8fafc;">Keyword Coverage</div>
                                <div style="font-size: 1.4rem; font-weight: 700; color: #3b82f6;">{hybrid_score["keyword_score"]}%</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            # ------------------ TABS ------------------
            #st.subheader("🔍 Raw Gemini Output")
            #st.json(results)

            tab1, tab2, tab3 = st.tabs(["🎯 Match & Analysis", "🏷️ Keyword Insights", "💡 Suggestions"])

            with tab1:
                st.subheader("Strengths")
                for s in results.get("strengths", []):
                    st.success(f"{s['title']}: {s['detail']}")

                st.subheader("Weaknesses")
                for w in results.get("weaknesses", []):
                    st.error(f"{w['title']}: {w['detail']}")

            with tab2:
                st.subheader("Matched Keywords")
                st.write(results.get("keyword_analysis", {}).get("matched", []))

                st.subheader("Missing Keywords")
                st.write(results.get("keyword_analysis", {}).get("missing", []))

            with tab3:
                st.subheader("Suggestions")
                for sug in results.get("suggestions", []):
                    st.info(f"Section: {sug['section']} → {sug['suggestion']}")

        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")

else:
    st.markdown("""
        <div style="text-align: center; padding: 50px 30px; margin-top: 20px;">
            <div style="font-size: 4rem; margin-bottom: 15px;">📄</div>
            <h3 style="margin-bottom: 10px; font-size: 1.6rem; color: #ffffff;">Get Started with AI Analysis</h3>
            <p style="color: #e2e8f0; max-width: 600px; margin: 0 auto 30px auto; font-size: 1rem; line-height: 1.6;">
                Upload your resume and paste the job description using the sidebar. Then click <b>Run Analysis</b> to see ATS insights.
            </p>
        </div>
    """, unsafe_allow_html=True)