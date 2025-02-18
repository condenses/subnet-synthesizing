from fastapi import FastAPI
from pydantic import BaseModel
from datasets import load_dataset
import uvicorn
from .config import CONFIG

NUM_PROC = 16


class SynthesizingResponse(BaseModel):
    user_message: str


class App:
    def __init__(self):
        self.app = FastAPI()
        self.dataset = self._load_dataset()
        self.app.add_api_route(
            "/api/synthesizing",
            self.api_synthesizing,
            methods=["GET"],
            response_model=SynthesizingResponse,
        )

    def _load_dataset(self):
        instruct_dataset = load_dataset(
            "BAAI/Infinity-Instruct", "0625", split="train", num_proc=NUM_PROC
        )
        instruct_dataset = instruct_dataset.map(
            lambda x: {"text": x["conversations"][0]["value"]}, num_proc=NUM_PROC
        )
        instruct_dataset = instruct_dataset.filter(
            lambda x: len(x["text"]) // 4 > CONFIG.synthesizing.min_tokens
            and len(x["text"]) // 4 < CONFIG.synthesizing.max_tokens,
            num_proc=NUM_PROC,
        )
        return iter(instruct_dataset)

    def api_synthesizing(self) -> SynthesizingResponse:
        text = next(self.dataset)["text"]
        return SynthesizingResponse(
            user_message=text,
        )


def start_server():
    app = App()
    uvicorn.run(app.app, host=CONFIG.server.host, port=CONFIG.server.port)


if __name__ == "__main__":
    start_server()
