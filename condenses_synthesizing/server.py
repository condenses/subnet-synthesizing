from fastapi import FastAPI
from pydantic import BaseModel
import tiktoken
from datasets import load_dataset
import uvicorn
from argparse import ArgumentParser

NUM_PROC = 10


class SynthesizingResponse(BaseModel):
    text: str
    token_count: int


class CountTokensRequest(BaseModel):
    text: str


class CountTokensResponse(BaseModel):
    token_count: int


class App:
    def __init__(self):
        self.app = FastAPI()
        self.tokenizer = tiktoken.encoding_for_model("gpt-4o")
        self.dataset = self._load_dataset()
        self.app.add_api_route(
            "/api/count_tokens",
            self.api_count_tokens,
            methods=["POST"],
            response_model=CountTokensResponse,
        )
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
            lambda x: len(x["text"]) > 200, num_proc=NUM_PROC
        )
        return iter(instruct_dataset)

    def api_count_tokens(self, request: CountTokensRequest) -> CountTokensResponse:
        tokens = self.tokenizer.encode(request.text)
        return CountTokensResponse(token_count=len(tokens))

    def api_synthesizing(self) -> SynthesizingResponse:
        text = next(self.dataset)["text"]
        return SynthesizingResponse(
            text=text, token_count=len(self.tokenizer.encode(text))
        )


def start_server():
    parser = ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    app = App()
    uvicorn.run(app.app, host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    start_server()
