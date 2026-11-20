from backend.brief_analyzer import analyze_brief

brief = """
I need a Python script to automate our weekly sales reports.

Currently, my team manually collects sales data from
multiple spreadsheets and prepares reports.

We need this completed ASAP.

Our previous developer stopped responding halfway
through the project.
"""

result = analyze_brief(brief)

print("\nCLIENT BRIEF ANALYSIS")
print("=====================")

for key, value in result.items():
    print(f"\n{key.upper()}:")
    print(value)