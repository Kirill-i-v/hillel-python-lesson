import asyncio
import random
import time
import argparse
import requests
import httpx

BASE_URL = "https://pokeapi.co/api/v2/pokemon/{pokemon_id}"


def http_request(url: str) -> str:
    print(f"Requesting {url} (requests)")
    response = requests.get(url)
    return response.json()["name"]


async def ahttp_request(client: httpx.AsyncClient, url: str) -> str:
    print(f"Requesting {url} (httpx)")
    response = await client.get(url)
    return response.json()["name"]


def get_urls(n: int) -> list[str]:
    return [BASE_URL.format(pokemon_id=random.randint(1, 500)) for _ in range(n)]


def sync_pokemons():
    urls = get_urls(n=50)
    results = [http_request(url) for url in urls]
    return results


async def async_pokemons():
    urls = get_urls(n=50)
    async with httpx.AsyncClient() as client:
        tasks = [ahttp_request(client, url) for url in urls]
        results = await asyncio.gather(*tasks)
    return results


def main(client_type: str):
    start = time.perf_counter()

    if client_type == "httpx":
        data = asyncio.run(async_pokemons())
    elif client_type == "requests":
        data = sync_pokemons()
    else:
        raise ValueError("Invalid client type. Use 'httpx' or 'requests'.")

    end = time.perf_counter()
    print(data)
    print(f"The length of the collection: {len(data)}")
    print(f"Execution time: {end - start:.2f} seconds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Pokémon names using requests or httpx.")
    parser.add_argument("client", choices=["httpx", "requests"], help="HTTP client to use")
    args = parser.parse_args()
    main(args.client)