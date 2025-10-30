import asyncio
import time
import aiohttp # allows us to make non-blocking http requests
import requests
from icecream import ic

# Good moments to use Async functions
# Web requests, file reading, db queries, API calls, any I/O operation (Input Output operation)

# Bad moments to use Async functions
# Math, Image processing, CPU intense work

def sync_requests():
    print("Making slow, blocking requests...")
    
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1"
    ]
    
    start = time.time()
    
    for i, url in enumerate(urls):
        ic(f"Request {i+1}: starting")
        r = requests.get(url)
        ic(f"Request {i+1}: done")
        
    total = time.time() - start
    
    ic(f"Total time: {round(total, 1)} seconds")
    print("")
  
  
async def asynchronous_requests():
    print("Making fast, non-blocking requests...")
    
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1"
    ]
    
    async def get_url(session, url, num):
        ic(f"Request {num} starting.")
        async with session.get(url) as response:
            await response.text()
            ic(f"Request {num} done!")
    
    start = time.time()
    
    async with aiohttp.ClientSession() as session:
        tasks = [get_url(session, url, i + 1) for i, url in enumerate(urls)]
        await asyncio.gather(*tasks)
        
    total = time.time() - start
    
    ic(f"Total time: {round(total, 1)} seconds")
    print("")
    
async def main(): # main function becomes async
    sync_requests()
    
    await asynchronous_requests()
    
    
if __name__ == "__main__":
    asyncio.run(main()) # main function call wrapped around asyncio .run method
    