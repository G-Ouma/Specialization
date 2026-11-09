
from backend.proposal_generator import generate_proposal

test_brief = """
We need a Python script that reads a single Excel sales
spreadsheet, calculates total sales by product, and generates
a weekly summary report in Excel. No database integration
or dashboard is required.
"""

test_analysis = {
    "problem": "Weekly sales reports are prepared manually.",
    "deliverable": "A Python script that generates weekly Excel reports.",
    "deadline": "Two weeks",
    "what_is_unclear": [],
    "red_flags": [],
    "effort_estimate": {
        "working_days": 5,
        "confidence": "medium",
        "reason": "A single spreadsheet and a clearly defined Excel output.",
        "needs_scoping": False
    }
}

proposal = generate_proposal(test_brief, test_analysis)

print("\nPRICING INTEGRATION TEST")
print("=" * 50)
print(proposal)
print("=" * 50)
print("WORD COUNT:", len(proposal.split()))
