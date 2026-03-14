import streamlit as st
from analyzer import ResumeAnalyzer
import os

# Page Configuration for a modern, high-end feel
st.set_page_config(
    page_title="AI Resume Intelligence", 
    page_icon="📄", 
    layout="wide"
)

# Custom CSS for Professional Branding
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        height: 3.5em; 
        background-color: #2e7d32; 
        color: white;
        font-weight: bold;
    }
    .metric-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("🚀 AI Resume Intelligence: Code the Future")
    st.markdown("Transform your resume from a simple document into a **high-impact career asset** using Gemini 1.5 Flash.")

    # Sidebar for Settings and JD
    with st.sidebar:
        st.header("⚙️ Configuration")
        api_key = st.text_input("Gemini API Key", type="password", help="Enter your Google AI Studio API key.")
        
        st.divider()
        st.header("🎯 Target Alignment")
        target_jd = st.text_area(
            "Target Job Description", 
            placeholder="Paste the job requirements here to identify skill gaps...",
            height=250
        )
        st.caption("Including a JD allows the AI to find missing keywords specifically for that role.")

    # Main Dashboard
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.header("📤 Upload Resume")
        uploaded_file = st.file_uploader("Upload your Resume (PDF format)", type="pdf")
        
        if st.button("Analyze Impact"):
            if not api_key:
                st.error("Please enter your Gemini API Key in the sidebar.")
            elif not uploaded_file:
                st.warning("Please upload a PDF file first.")
            else:
                analyzer = ResumeAnalyzer(api_key)
                with st.spinner("Analyzing project impact and action-verbs..."):
                    # Extract and Analyze
                    resume_text = analyzer.extract_text(uploaded_file)
                    analysis = analyzer.analyze_resume(resume_text, target_jd)
                    
                    if "error" in analysis:
                        st.error(analysis["error"])
                    else:
                        st.session_state['analysis_data'] = analysis
                        st.success("Analysis Complete!")

    with col2:
        st.header("📊 Results Dashboard")
        if 'analysis_data' in st.session_state:
            data = st.session_state['analysis_data']
            
            # 1. Rating Metric (Core Requirement)
            score = data.get('rating', 0)
            st.metric(label="Resume Impact Score", value=f"{score}/10")
            st.progress(score / 10)
            
            if score < 8:
                st.warning(f"Your score is {score}/10. Follow the tasks below to reach at least 8/10!")
            else:
                st.balloons()
                st.success("Great job! Your resume has a strong impact score.")

            # 2. AI-Generated Summary (Core Requirement)
            st.subheader("✨ Professional Summary")
            st.info(data.get('summary', "Summary could not be generated."))

    # Bottom Sections for Detailed Breakdown
    if 'analysis_data' in st.session_state:
        st.divider()
        data = st.session_state['analysis_data']
        
        tab1, tab2, tab3 = st.tabs(["💡 Improvement Tasks", "🔍 JD Alignment", "🛠️ Extracted Highlights"])
        
        with tab1:
            st.subheader("Actionable Tasks to Improve Your Score")
            # Addressing the core requirement of tasks to improve score to 8/10
            tasks = data.get('action_tasks', [])
            for task in tasks:
                st.checkbox(task)
            
            with st.expander("Section-Specific Suggestions"):
                for section, advice in data.get('suggestions', {}).items():
                    st.write(f"**{section}:** {advice}")

        with tab2:
            st.subheader("Gap Analysis")
            if target_jd:
                gaps = data.get('alignment_gaps', [])
                if gaps:
                    st.write("The following skills/experiences are missing or weak compared to the JD:")
                    for gap in gaps:
                        st.error(f"Missing: {gap}")
                else:
                    st.success("Your resume aligns perfectly with this Job Description!")
            else:
                st.info("Paste a Job Description in the sidebar to see alignment gaps.")

        with tab3:
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Extracted Skills**")
                st.write(data.get('skills', []))
            with c2:
                st.write("**Industry Keywords**")
                st.write(data.get('keywords', []))

if __name__ == "__main__":
    main()
