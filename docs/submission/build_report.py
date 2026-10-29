"""Generate the report PDF from its editable Markdown source.

Requires reportlab (document tooling only, not an application dependency).
Run from any directory: python docs/submission/build_report.py
"""

from pathlib import Path
from html import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak


ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).with_name("development_report.md")
OUTPUT = ROOT / "output" / "pdf" / "hangman-development-report.pdf"


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = {
        "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=19,
                                leading=23, textColor=colors.HexColor("#264b3b"), spaceAfter=9),
        "heading": ParagraphStyle("heading", fontName="Helvetica-Bold", fontSize=11,
                                  leading=14, spaceBefore=10, spaceAfter=5, keepWithNext=True),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9.8,
                               leading=13, spaceAfter=6, alignment=TA_LEFT),
    }
    blocks = SOURCE.read_text(encoding="utf-8").strip().split("\n\n")
    story = []
    for block in blocks:
        if block.startswith("## Testing and debugging"):
            story.append(PageBreak())
        if block.startswith('1. "'):
            for prompt in block.splitlines():
                story.append(Paragraph(escape(prompt), styles["body"]))
            continue
        text = " ".join(block.splitlines())
        kind = "title" if text.startswith("# ") else "heading" if text.startswith("## ") else "body"
        text = text.removeprefix("## ").removeprefix("# ")
        story.append(Paragraph(escape(text), styles[kind]))

    def footer(canvas, document):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#d4ded6"))
        canvas.line(44, 36, 568, 36)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#5d695f"))
        canvas.drawString(44, 24, "Hangman | Development report")
        canvas.drawRightString(568, 24, str(document.page))
        canvas.restoreState()

    SimpleDocTemplate(str(OUTPUT), pagesize=letter, rightMargin=44, leftMargin=44,
                      topMargin=38, bottomMargin=48,
                      title="Web-Based Hangman Development Report",
                      author="").build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    build()
