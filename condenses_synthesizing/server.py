from fastapi import FastAPI
from pydantic import BaseModel
from datasets import load_dataset, Dataset
import uvicorn
from .config import CONFIG

NUM_PROC = 16
app = FastAPI()


class SynthesizingResponse(BaseModel):
    user_message: str


class InfinityDataset:
    def __init__(self, config):
        self.config = config
        self.dataset = None
        self.iterator = None
        self._load_dataset()

    def _load_dataset(self):
        # Load and preprocess the dataset
        dataset = load_dataset(
            "BAAI/Infinity-Instruct",
            "0625",
            split="train",
            streaming=True,
        )
        dataset = dataset.map(lambda x: {"text": x["conversations"][0]["value"]})
        dataset = dataset.filter(
            lambda x: len(x["text"]) // 4 > self.config.synthesizing.min_tokens
            and len(x["text"]) // 4 < self.config.synthesizing.max_tokens,
        )

        self.dataset = dataset
        self.iterator = iter(self.dataset)

    def next(self):
        try:
            return next(self.iterator)
        except StopIteration:
            # Reset the iterator when it's exhausted
            self._load_dataset()
            return next(self.iterator)

    def reset(self):
        """Explicitly reset the iterator"""
        self._load_dataset()


# Initialize the dataset
infinity_dataset = InfinityDataset(CONFIG)


@app.get("/api/synthesizing", response_model=SynthesizingResponse)
def api_synthesizing() -> SynthesizingResponse:
    text = infinity_dataset.next()["text"]
    return SynthesizingResponse(
        user_message=text,
    )
