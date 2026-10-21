
from pathlib import Path
import pymupdf

output = Path("data/raw/annual_leave_revision_test.pdf")
output.parent.mkdir(parents=True, exist_ok=True)

doc = pymupdf.open()
page = doc.new_page()

page.insert_textbox(
    pymupdf.Rect(60, 60, 540, 740),
    """Synthetic HR Policy Revision Test

Annual Leave Policy

For this conflict-handling test only, this document states that
employees receive 25 working days of annual leave per calendar year.

Employees must obtain manager approval before taking annual leave.

IMPORTANT: This is fictional test content. It has not been approved
by any real organization. No effective date or supersession status
is specified in this test document.
""",
    fontsize=12,
)

doc.save(output)
doc.close()

print(f"Created synthetic conflict document: {output}")

