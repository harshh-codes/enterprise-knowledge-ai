
from pathlib import Path
import pymupdf

OUTPUT = Path("data/raw/large_hr_handbook.pdf")
TOTAL_PAGES = 100

departments = [
    "Human Resources", "Finance", "Information Technology",
    "Operations", "Customer Support", "Legal and Compliance",
    "Facilities", "Learning and Development", "Procurement",
    "Security", "Research", "Business Administration",
]

topics = [
    "employee onboarding", "workplace conduct", "expense reporting",
    "equipment usage", "business travel", "training requirements",
    "performance reviews", "data protection", "office access",
    "remote work", "meeting procedures", "document retention",
    "workplace safety", "internal communication", "leave administration",
    "payroll processing", "vendor management", "incident reporting",
    "quality assurance", "business continuity",
]

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

document = pymupdf.open()

for page_number in range(1, TOTAL_PAGES + 1):
    page = document.new_page()
    department = departments[(page_number - 1) % len(departments)]

    paragraphs = [
        f"Department: {department}",
        f"Handbook section reference: HR-{page_number:03d}",
        "",
        (
            "Purpose and scope: This section describes standard internal "
            "procedures, employee responsibilities, administrative controls, "
            "documentation requirements, and review practices. Employees "
            "should follow the approved procedures applicable to their roles."
        ),
        "",
    ]

    # Add realistic but synthetic background material and distractors.
    for item in range(1, 7):
        topic = topics[(page_number + item * 3) % len(topics)]
        paragraphs.append(
            f"{item}. {topic.title()}: Employees and managers must follow "
            "the documented workflow, retain relevant records, use approved "
            "systems, and escalate unusual circumstances through the "
            "appropriate departmental channel. Requirements may depend on "
            "the employee's role, location, approval level, and applicable "
            "internal procedures. Supporting records should be accurate, "
            "complete, and available for authorized review."
        )
        paragraphs.append("")

    # Place the key policy in a later page, surrounded by unrelated text.
    if page_number == 73:
        paragraphs.extend([
            "SPECIAL POLICY REFERENCE: ANNUAL LEAVE",
            (
                "The standard annual leave entitlement is 20 working days "
                "per calendar year. Employees must obtain manager approval "
                "before taking annual leave. This statement is part of the "
                "synthetic test handbook and is not an actual company policy."
            ),
            "",
        ])

    paragraphs.extend([
        "Administrative notes",
        (
            "Routine requests should be recorded using the designated "
            "process. Managers should review submissions for completeness "
            "and direct unresolved questions to the responsible team."
        ),
        "",
        f"End of section HR-{page_number:03d}.",
    ])

    text = "\n".join(paragraphs)
    page.insert_textbox(
        pymupdf.Rect(50, 45, 545, 790),
        text,
        fontsize=9,
        lineheight=1.25,
    )

document.save(OUTPUT)
document.close()

print(f"Created: {OUTPUT}")
print(f"Pages requested: {TOTAL_PAGES}")

