from fpdf import FPDF
import PyPDF2
from pathlib import Path
import docx
import io
import os
import re

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def read_resume(file):
    if file.name.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif file.name.endswith(".docx"):
        return extract_text_from_docx(file)
    else:
        return None
    
def text_to_pdf_bytes(text: str, title: str = "Document") -> bytes:
    """
    Compact, resilient PDF renderer:
    - Loads DejaVu fonts via OS-safe paths relative to this file
    - Falls back to Helvetica if fonts are missing
    - Keeps headings/subheadings/bullets formatting tight and readable
    """

    # -------- Compact defaults --------
    MARGINS_MM = (16, 16, 16)   # left, top, right
    BODY_SIZE = 10.5
    HEAD_SIZE = 11.5
    SUBHEAD_SIZE = 11
    LINE_H_BODY = 5.5
    LINE_H_HEAD = 6.0
    GAP_AFTER_PARA = 1.0
    GAP_AFTER_SUBHEAD = 2.0
    GAP_AFTER_HEADING = 2.0
    CONTACT_SIZE = 13

    # Normalize some characters
    text = text.replace("\t", "    ").replace("—", "–")

    # -------- OS-safe font paths relative to this file --------
    BASE_DIR = Path(__file__).resolve().parent
    FONT_REG = (BASE_DIR / "fonts" / "DejaVuSans.ttf").as_posix()
    FONT_BOLD = (BASE_DIR / "fonts" / "DejaVuSans-Bold.ttf").as_posix()
    FONT_OBLQ = (BASE_DIR / "fonts" / "DejaVuSans-Oblique.ttf").as_posix()

    have_fonts = all(Path(p).is_file() for p in (FONT_REG, FONT_BOLD, FONT_OBLQ))

    pdf = FPDF()
    l, t, r = MARGINS_MM
    pdf.set_margins(l, t, r)
    pdf.add_page()

    # -------- Register fonts or fall back --------
    if have_fonts:
        pdf.add_font("DejaVu",  "", FONT_REG,  uni=True)
        pdf.add_font("DejaVu",  "B", FONT_BOLD, uni=True)
        pdf.add_font("DejaVuI", "", FONT_OBLQ, uni=True)
        pdf.set_font("DejaVu", size=BODY_SIZE)
        use_core_font = False
    else:
        # Fallback: core Helvetica (Latin-1 only) + sanitize text
        text = (text.replace("•", "-")
                    .replace("–", "-")
                    .replace("—", "-")
                    .replace("’", "'")
                    .replace("“", '"')
                    .replace("”", '"'))
        pdf.set_font("Helvetica", size=BODY_SIZE)
        use_core_font = True

    page_w = pdf.w - pdf.l_margin - pdf.r_margin
    bullet_re = re.compile(r"^(\s*)([●•\-\*])\s+(.*)$")

    def string_w(s: str) -> float:
        return pdf.get_string_width(s)

    def is_section_heading(s: str) -> bool:
        s = s.strip()
        return (s.isupper() and 3 <= len(s) <= 40) or (s.endswith(":") and len(s) <= 40)

    def is_subheading(s: str) -> bool:
        s = s.strip()
        if not s or s.isupper() or bullet_re.match(s) or is_section_heading(s):
            return False
        if " | " in s or "," in s:
            return True
        if re.search(r"\b(19|20)\d{2}\b", s):
            return True
        if re.search(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b", s, re.I):
            return True
        words = s.split()
        return 5 <= len(words) <= 16 and sum(w[:1].isupper() for w in words)/len(words) > 0.5

    # -------- Render --------
    lines = text.splitlines()
    first_non_empty_done = False

    for raw in lines:
        if raw.strip() == "":
            pdf.ln(LINE_H_BODY)
            continue

        # Contact line (first non-empty)
        if not first_non_empty_done:
            if not use_core_font:
                pdf.set_font("DejaVu", "B", CONTACT_SIZE)
            else:
                pdf.set_font("Helvetica", "B", CONTACT_SIZE)
            pdf.multi_cell(page_w, LINE_H_BODY + 1, raw.strip(), align="C")
            pdf.ln(LINE_H_BODY)
            pdf.set_font("DejaVu" if not use_core_font else "Helvetica", size=BODY_SIZE)
            first_non_empty_done = True
            continue

        # Bullets
        m = bullet_re.match(raw)
        if m:
            leading_spaces, symbol, rest = m.groups()
            if use_core_font and symbol not in "-*":
                symbol = "-"
            indent_px = string_w(leading_spaces)
            y0 = pdf.get_y()
            x_bullet = pdf.l_margin + indent_px
            pdf.set_xy(x_bullet, y0)
            pdf.set_font("DejaVu" if not use_core_font else "Helvetica", "", BODY_SIZE - 1)
            bullet_token = f"{symbol} "
            pdf.cell(string_w(bullet_token), LINE_H_BODY, bullet_token, ln=0)
            pdf.set_font("DejaVu" if not use_core_font else "Helvetica", "", BODY_SIZE)
            x_text = pdf.get_x() + string_w(" ")
            pdf.set_xy(x_text, y0)
            avail = pdf.w - pdf.r_margin - x_text
            pdf.multi_cell(avail, LINE_H_BODY, rest, align="J")
            pdf.ln(GAP_AFTER_PARA)
            continue

        # Subheading
        if is_subheading(raw):
            if not use_core_font:
                pdf.set_font("DejaVuI", "", SUBHEAD_SIZE)
            else:
                pdf.set_font("Helvetica", "I", SUBHEAD_SIZE)
            pdf.multi_cell(page_w, LINE_H_HEAD, raw.strip(), align="L")
            pdf.ln(GAP_AFTER_SUBHEAD)
            pdf.set_font("DejaVu" if not use_core_font else "Helvetica", "", BODY_SIZE)
            continue

        # Section heading
        if is_section_heading(raw):
            if not use_core_font:
                pdf.set_font("DejaVu", "B", HEAD_SIZE)
            else:
                pdf.set_font("Helvetica", "B", HEAD_SIZE)
            pdf.multi_cell(page_w, LINE_H_HEAD, raw.strip(), align="L")
            pdf.ln(GAP_AFTER_HEADING)
            pdf.set_font("DejaVu" if not use_core_font else "Helvetica", "", BODY_SIZE)
            continue

        # Normal text
        leading_spaces = len(raw) - len(raw.lstrip(" "))
        indent_w = string_w(" " * leading_spaces)
        pdf.set_x(pdf.l_margin + indent_w)
        pdf.multi_cell(page_w - indent_w, LINE_H_BODY, raw.strip(), align="J")
        pdf.ln(GAP_AFTER_PARA)

        # --- Final output ---
    pdf_bytes = pdf.output(dest="S")

    # fpdf2 >= 2.7 returns bytearray; older versions may return str
    if isinstance(pdf_bytes, bytearray):
        return bytes(pdf_bytes)
    elif isinstance(pdf_bytes, str):
        return pdf_bytes.encode("latin1", "ignore")
    else:
        raise TypeError(f"Unexpected PDF output type: {type(pdf_bytes)}")

    return pdf.output(dest="S").encode("latin1")