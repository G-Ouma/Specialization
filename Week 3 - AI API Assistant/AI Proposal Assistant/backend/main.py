from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.brief_analyzer import analyze_brief
from backend.proposal_generator import generate_proposal


app = FastAPI(title="AI Proposal Assistant")

# Allow requests from our frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProposalRequest(BaseModel):
    mode: str
    text: str


@app.get("/")
def home():
    return {
        "message": "AI Proposal Assistant API is running"
    }


@app.post("/process")
def process_proposal(request: ProposalRequest):

    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Please provide some text."
        )

    if request.mode == "generate":

        try:
            # Step 1: Analyse the client's brief
            analysis = analyze_brief(request.text)

            # Step 2: Generate the proposal using the analysis
            proposal = generate_proposal(
                request.text,
                analysis
            )

            # Step 3: Return both results to the frontend
            return {
                "mode": "generate",
                "analysis": analysis,
                "proposal": proposal
            }

        except Exception as error:
            raise HTTPException(
                status_code=502,
                detail=f"Proposal generation failed: {error}"
            )

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid mode selected."
        )