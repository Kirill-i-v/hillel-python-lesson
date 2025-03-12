import random
import string
import os
import abc
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

API_KEY = os.getenv("ALPHAVANTAGE_KEY_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def random_string(n: int) -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(n))


class MyGeneratorService(abc.ABC):
    @abc.abstractmethod
    async def generate_random_article_idea(self):
        pass

    @abc.abstractmethod
    async def generate_technical_guide(self):
        pass

    @abc.abstractmethod
    async def generate_fiction(self):
        pass


class ArticleMyGeneratorService(MyGeneratorService):
    async def generate_random_article_idea(self):
        await asyncio.sleep(2)
        return {"title": random_string(10), "idea": random_string(30)}

    async def generate_technical_guide(self):
        await asyncio.sleep(2)
        return {"title": "Tech Guide: " + random_string(8), "idea": random_string(50)}

    async def generate_fiction(self):
        await asyncio.sleep(2)
        return {"title": "Fiction Story: " + random_string(8), "idea": random_string(50)}


article_service = ArticleMyGeneratorService()


@app.get("/article-idea")
async def article_idea():
    return await article_service.generate_random_article_idea()
