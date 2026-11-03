"""Live integration checks using six natural ways members may ask questions.

Run: python test_assistant.py
These checks make six Gemini API requests and require a working GEMINI_API_KEY.
"""
from main import answer_question

TEST_CASES = [
    ("Nataka kujua balance yangu.", ["3,500", "THK-014"]),
    ("How much do I owe the sacco?", ["3,500"]),
    ("When are we having our next chama meeting?", ["13", "November", "Friday"]),
    ("Is there a members meeting coming up and what time?", ["10:00", "13", "November"]),
    ("How much does a new member pay to join?", ["2,000", "500"]),
    ("What are the monthly charges and registration costs?", ["1,000", "500"]),
]


def main() -> None:
    passed = 0
    print("Running member-question tests...\n")

    for number, (question, expected_any) in enumerate(TEST_CASES, start=1):
        print(f"Test {number}: {question}")
        try:
            answer = answer_question(question)
            print(f"Answer: {answer}")
            normalized = answer.lower().replace(",", "")
            # Each test passes if at least one expected detail appears.
            matched = any(
                item.lower().replace(",", "") in normalized
                for item in expected_any
            )
            if matched:
                print("Result: PASS\n")
                passed += 1
            else:
                print(f"Result: REVIEW — expected one of: {expected_any}\n")
        except Exception as error:
            print(f"Result: ERROR — {error}\n")

    print(f"Summary: {passed}/{len(TEST_CASES)} checks passed.")
    if passed != len(TEST_CASES):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
