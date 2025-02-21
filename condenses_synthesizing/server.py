from fastapi import FastAPI
from pydantic import BaseModel
from datasets import load_dataset
import uvicorn
from .config import CONFIG

NUM_PROC = 16
app = FastAPI()


class SynthesizingResponse(BaseModel):
    user_message: str


# Load dataset once at module level
instruct_dataset = load_dataset(
    "BAAI/Infinity-Instruct",
    "0625",
    split="train",
    streaming=True,
)
instruct_dataset = instruct_dataset.map(
    lambda x: {"text": x["conversations"][0]["value"]}
)
instruct_dataset = instruct_dataset.filter(
    lambda x: len(x["text"]) // 4 > CONFIG.synthesizing.min_tokens
    and len(x["text"]) // 4 < CONFIG.synthesizing.max_tokens,
)

instruct_dataset = iter(instruct_dataset)


@app.get("/api/synthesizing", response_model=SynthesizingResponse)
def api_synthesizing() -> SynthesizingResponse:
    text = next(instruct_dataset)["text"]
    return SynthesizingResponse(
        user_message=text,
    )
