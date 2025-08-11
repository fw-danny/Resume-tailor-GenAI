import base64
import pathlib
from io import BytesIO

import streamlit as st
from openai import OpenAI

from prompts import resume_tailor_prompt, cover_letter_prompt
from utils import read_resume, text_to_pdf_bytes

# -------------------- Config --------------------
MODEL_NAME = "gpt-5-mini"
APP_TITLE = "GenAI Resume & Cover Letter Tailor"
APP_SUBTITLE = "Upload your resume, paste the job description, and get a tidy tailored resume + cover letter. Or use sample data to see how it works."
PRIVACY_NOTE = "Files and text are processed in-memory — nothing is stored."

# Prefer secrets in production; for local dev you can temporarily hardcode
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -------------------- Page Setup --------------------
st.set_page_config(page_title=APP_TITLE, layout="wide")
st.markdown("""
<style>
.step-strip { display:flex; gap:.5rem; font-size:.95rem; margin:.25rem 0 1rem 0; }
.step { display:flex; align-items:center; gap:.4rem; padding:.35rem .6rem; border-radius:.6rem;
        background:#f2f4f8; border:1px solid #e5e7eb; color:#1E1E1E; font-weight:500; }
.step .icon { width:18px; height:18px; display:inline-flex; align-items:center; justify-content:center;
             filter: contrast(1.1) saturate(0.9); }
.step small { color:#475569; font-weight:600; } /* the 1/2/3 numbers */
@media (prefers-color-scheme: dark) {
  .step     { background:#1f2937; border-color:#374151; color:#f3f4f6; }
  .step small { color:#cbd5e1; }
}
/* Outputs a bit roomier */
textarea, .stMarkdown { font-size: 1rem; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

# -------------------- Header --------------------
st.title(APP_TITLE)
st.write(APP_SUBTITLE)
st.caption(PRIVACY_NOTE)
st.markdown(
    '''
    <div class="step-strip">
      <div class="step">
        <span class="icon">📄</span><small>1</small>&nbsp;Upload Resume
      </div>
      <div class="step">
        <span class="icon">🧾</span><small>2</small>&nbsp;Paste JD
      </div>
      <div class="step">
        <span class="icon">✨</span><small>3</small>&nbsp;Generate
      </div>
    </div>
    ''',
    unsafe_allow_html=True
)

# -------------------- Sample Loader (set state BEFORE widgets) --------------------
sample_resume_path = pathlib.Path("sample_data/sample_resume.pdf")
sample_jd_path = pathlib.Path("sample_data/sample_jd.txt")

# Ensure keys exist
if "uploaded_resume" not in st.session_state:
    st.session_state["uploaded_resume"] = None
if "jd_input" not in st.session_state:
    st.session_state["jd_input"] = ""

load_cols = st.columns([1, 3])
with load_cols[0]:
    if st.button("Load Sample Data"):
        if not sample_resume_path.exists() or not sample_jd_path.exists():
            st.error("Sample files not found in sample_data/. Please add sample_resume.pdf and sample_jd.txt.")
        else:
            # Load JD text
            with open(sample_jd_path, "r", encoding="utf-8") as f:
                st.session_state["jd_input"] = f.read()
            # Load resume as a BytesIO so it behaves like an uploaded file
            with open(sample_resume_path, "rb") as f:
                b = f.read()
            bio = BytesIO(b)
            bio.name = sample_resume_path.name
            st.session_state["uploaded_resume"] = bio
            st.success("Loaded sample resume and JD. Click Generate.")

# -------------------- Inputs --------------------
left, right = st.columns(2)
with left:
    # Always render the uploader so it never disappears
    uploader_value = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"], key="resume_uploader")

    # If a sample is loaded, tell the user and let them clear it
    if st.session_state.get("uploaded_resume") is not None:
        st.info("Using sample resume")
        if st.button("Clear sample resume"):
            st.session_state["uploaded_resume"] = None
            st.rerun()

with right:
    # JD textarea is keyed; when we load the sample JD, this will auto-fill
    job_description = st.text_area("Paste the job description", height=220, key="jd_input")

# Effective resume to use for generation: prefer sample if present, else the uploader
effective_resume = st.session_state.get("uploaded_resume") or uploader_value

# -------------------- Session State Defaults for Outputs --------------------
for key, default in [
    ("tailored_resume", ""),
    ("cover_letter", ""),
    ("resume_pdf_bytes", b""),
    ("cover_pdf_bytes", b""),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# -------------------- Generate Button --------------------
can_generate = (effective_resume is not None) and bool(job_description.strip())
generate_disabled_reason = None
if effective_resume is None:
    generate_disabled_reason = "Upload a resume or click Load Sample Data"
elif not job_description.strip():
    generate_disabled_reason = "Paste the job description first"

btn = st.button(
    "Generate",
    type="primary",
    disabled=not can_generate,
    help=None if can_generate else generate_disabled_reason,
)

# -------------------- Generation --------------------
if btn and can_generate:
    try:
        resume_text = read_resume(effective_resume)
        with st.spinner("Tailoring resume…"):
            tailored = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{
                    "role": "user",
                    "content": resume_tailor_prompt.format(
                        resume_text=resume_text,
                        job_description=job_description
                    )
                }],
            ).choices[0].message.content.strip()

        with st.spinner("Drafting cover letter…"):
            letter = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{
                    "role": "user",
                    "content": cover_letter_prompt.format(
                        tailored_resume=tailored,
                        job_description=job_description
                    )
                }],
            ).choices[0].message.content.strip()

        # Persist outputs
        st.session_state["tailored_resume"] = tailored
        st.session_state["cover_letter"] = letter

        # Build PDFs (your compact, block-aware rules are inside text_to_pdf_bytes)
        with st.spinner("Formatting PDFs…"):
            st.session_state["resume_pdf_bytes"] = text_to_pdf_bytes(tailored, title="Tailored Resume")
            st.session_state["cover_pdf_bytes"] = text_to_pdf_bytes(letter, title="Cover Letter")

        st.success("Done! Scroll down to preview and download.")
    except Exception as e:
        st.error(f"Something went wrong: {e}")

st.divider()

# -------------------- Results Tabs --------------------
tabs = st.tabs(["Tailored Resume", "Cover Letter"])

with tabs[0]:
    st.subheader("Tailored Resume")
    st.text_area(
        label="",
        value=st.session_state["tailored_resume"],
        height=420,
        key="resume_out_area"
    )
    c1, c2 = st.columns([1, 2])
    with c1:
        st.download_button(
            "Download Resume (PDF)",
            data=st.session_state["resume_pdf_bytes"],
            file_name="tailored_resume.pdf",
            mime="application/pdf",
            disabled=not st.session_state["resume_pdf_bytes"]
        )

with tabs[1]:
    st.subheader("Cover Letter")
    st.text_area(
        label="",
        value=st.session_state["cover_letter"],
        height=420,
        key="cover_out_area"
    )
    c1, c2 = st.columns([1, 2])
    with c1:
        st.download_button(
            "Download Cover Letter (PDF)",
            data=st.session_state["cover_pdf_bytes"],
            file_name="cover_letter.pdf",
            mime="application/pdf",
            disabled=not st.session_state["cover_pdf_bytes"]
        )

# -------------------- Inline PDF Preview (Resume) --------------------
if st.session_state["resume_pdf_bytes"]:
    with st.expander("Preview Resume PDF (beta)"):
        b64 = base64.b64encode(st.session_state["resume_pdf_bytes"]).decode("utf-8")
        pdf_iframe = f"""
        <iframe
            src="data:application/pdf;base64,{b64}"
            width="100%" height="600" style="border:1px solid #e5e7eb; border-radius:8px;">
        </iframe>
        """
        st.markdown(pdf_iframe, unsafe_allow_html=True)