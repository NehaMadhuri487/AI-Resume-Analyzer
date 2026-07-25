import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* Global background and text */
        body, .stApp {
            background-color: #0f172a; /* dark navy */
            color: #f9fafb; /* bright text */
            font-family: 'Inter', sans-serif;
        }

        /* Sidebar styling */
        .stSidebar {
            background-color: #1e293b !important; /* slate */
            color: #f9fafb !important;
        }
        .stSidebar textarea, .stSidebar input {
            background-color: #f1f5f9 !important; /* light background for contrast */
            color: #111827 !important; /* dark text for readability */
            border-radius: 6px !important;
            border: 1px solid #d1d5db !important;
        }

        /* Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #6366f1, #a855f7);
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            transition: 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #4f46e5, #9333ea);
            transform: scale(1.02);
        }

        /* Headings */
        h1, h2, h3, h4 {
            color: #ffffff !important;
        }

        /* Paragraphs and labels */
        p, label {
            color: #f9fafb !important; /* bright text */
        }

        /* Tabs */
        .stTabs [role="tablist"] {
            gap: 12px;
        }
        .stTabs [role="tab"] {
            background-color: #1e293b;
            color: #f9fafb;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 500;
        }
        .stTabs [role="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, #6366f1, #a855f7);
            color: #ffffff;
        }

        /* Cards */
        .analysis-card {
            background: rgba(255,255,255,0.15); /* lighter overlay */
            border: 1px solid rgba(255,255,255,0.25);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            color: #f9fafb;
        }
        </style>
    """, unsafe_allow_html=True)

def clean_text(text: str) -> str:
    """
    Normalize whitespace and remove empty lines from extracted text.
    """
    if not text:
        return ""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)
