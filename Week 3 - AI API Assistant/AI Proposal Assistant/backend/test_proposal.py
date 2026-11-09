
from backend.brief_analyzer import analyze_brief
from backend.proposal_generator import generate_proposal


client_brief = """
Hello, I need someone to build me a bot that can reply to
customer messages automatically. We sell agricultural inputs
in Kenya and get a lot of WhatsApp messages asking about prices
and stock. Budget is flexible. I need it ASAP.
"""


def test_proposal_generation():
    print("\nANALYSING CLIENT BRIEF...")
    analysis = analyze_brief(client_brief)
    
    print("\nBRIEF ANALYSIS")
    print("=" * 50)
    print(analysis)
    print("=" * 50)

    print("\nGENERATING PROPOSAL...")
    proposal = generate_proposal(client_brief, analysis)

    print("\n" + "=" * 50)
    print("GENERATED FREELANCE PROPOSAL")
    print("=" * 50)

    print(proposal)

    print("\n" + "=" * 50)
    print("WORD COUNT:", len(proposal.split()))
    print("=" * 50)


if __name__ == "__main__":
    test_proposal_generation()
