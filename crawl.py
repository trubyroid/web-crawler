import aiohttp
import asyncio
import sys
import json
import time


async def client(urls):

    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:8888/api/v1/tasks/',
                                json=urls) as response_post:
            resp_header = dict(response_post._headers)
            resp_text = json.loads(await response_post.text())

            print("\nPOST response:")
            print("HTTP/1.1", response_post.status)
            for i in resp_header:
                print(f"{i} : {resp_header[i]}")
            print("\nTask object: ")
            for i in resp_text:
                print(f"{i} : {resp_text[i]}")

    async with aiohttp.ClientSession() as session:
        while 1:
            await asyncio.sleep(1)
            async with session.get('http://127.0.0.1:8888/api/v1/tasks/' +
                                   resp_text["id"]) as response_get:
                resp_header = dict(response_get._headers)
                resp_text = json.loads(await response_get.text())
    
                print("\nGET response:")
                print("HTTP/1.1", response_get.status)
                for i in resp_header:
                    print(f"{i} : {resp_header[i]}")
                print("\nTask object: ")
                for i in resp_text:
                    print(f"{i} : {resp_text[i]}")
                print("\n")
                if resp_text["status"] == "Ready":
                    break


if __name__ == "__main__":
    urls = sys.argv[1:]
    if not urls:
        print("Please, insert urls.")
    else:
        asyncio.run(client(urls))
