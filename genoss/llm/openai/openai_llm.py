from __future__ import annotations

from typing import Any

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from pydantic import Field

from genoss.entities.chat.chat_completion import ChatCompletion
from genoss.llm.base_genoss import BaseGenossLLM
from genoss.prompts.prompt_template import prompt_template


class OpenAILLM(BaseGenossLLM):
    name: str = "openai"
    description: str = "OpenAI LLM"
    model_name: str = Field("gpt-3.5-turbo", description="OpenAI model name")
    api_key: str

    def generate_answer(self, question: str) -> dict[str, Any]:
        llm = ChatOpenAI(model_name=self.model_name, openai_api_key=self.api_key)

        llm_chain = LLMChain(llm=llm, prompt=prompt_template)
        response_text = llm_chain(question)

        answer = response_text["text"]
        chat_completion = ChatCompletion(
            model=self.name, answer=answer, question=question
        )

        return chat_completion.to_dict()

    def generate_embedding(self, text: str) -> list[float]:
        model = OpenAIEmbeddings()
        return model.embed_query(text)
