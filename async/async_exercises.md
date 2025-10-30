# 10 Async Exercises by Gemini

Here are 10 exercises to build your operational knowledge of `asyncio`, `requests`, and `aiohttp`.

-----

### Preparation

You will need to install `requests` and `aiohttp`:

```bash
pip install requests aiohttp
```

For testing, we will use `https://httpbin.org/` (for simulated delays) and `https://jsonplaceholder.typicode.com/` (for realistic API data).

-----

### 1\. The "Hello World" Coroutine 🕵️‍♀️

**Objective:** Understand the basic syntax of an `async` function and how to run it.

**Task:**

1.Import `asyncio`.
2.Define an `async def` function named `greet()` that prints "Signal acquired."
3.Define a main `async def main()` function that `await`s `greet()`.
4.Use `asyncio.run(main())` to execute it.

-----

### 2\. Understanding `await` and `asyncio.sleep()`

**Objective:** See how `await` yields control, allowing other tasks to run.

**Task:**

1.Import `asyncio`.
2.Create an `async def say(message, delay)` function that:
      * `await`s `asyncio.sleep(delay)`.
      * Prints the `message`.
3.In `main()`, `await` two calls to `say()`:
      * `await say("Task 1 complete.", 2)` (2-second delay)
      * `await say("Task 2 complete.", 1)` (1-second delay)
4.Observe the 3-second total execution time.

-----

### 3\. Concurrent Execution with `asyncio.gather()` ⚡

**Objective:** Run multiple coroutines concurrently, not sequentially.

**Task:**

1.Use the `say(message, delay)` function from Exercise 2.
2.In `main()`, create two task objects:
      * `task1 = say("Task 1 complete.", 2)`
      * `task2 = say("Task 2 complete.", 1)`
3.Use `await asyncio.gather(task1, task2)` to run them concurrently.
4.Observe that "Task 2" prints first and the total time is only 2 seconds (the time of the *longest* task).

-----

### 4\. The Problem: Blocking with `requests` 🛑

**Objective:** Establish a baseline by measuring a standard, blocking I/O operation.

**Task:**

1.Import `requests` and `time`.
2.Define a *synchronous* (`def`) function `fetch_blocking()` that:
      * Uses `requests.get("https://jsonplaceholder.typicode.com/posts/1")`.
      * Prints that the request is complete.
3.In your main script (no `asyncio` needed here):
      * Record the `start_time = time.time()`.
      * Call `fetch_blocking()` three times in a row.
      * Print the total `time.time() - start_time`.
      * **Observation:** The total time will be the *sum* of all three requests (e.g., 0.5s + 0.5s + 0.5s = 1.5s).

-----

### 5\. First `aiohttp` Request (Async)

**Objective:** Learn the basic syntax for making a single asynchronous request.

**Task:**

1.Import `aiohttp` and `asyncio`.
2.Define an `async def fetch_async()` function that:
      *Uses `async with aiohttp.ClientSession() as session:`.
      *Inside the block, uses `async with session.get("https://jsonplaceholder.typicode.com/posts/1") as response:`.
      *`await`s `response.json()` to get the data.
      *Prints the title of the post (e.g., `data['title']`).
3.  Use `asyncio.run(fetch_async())` to run it.

-----

### 6\. The Solution: Concurrent `aiohttp` Requests 💡

**Objective:** Re-do Exercise 4 using `aiohttp` to see the performance gain.

**Task:**

1.Import `aiohttp`, `asyncio`, and `time`.
2.Define an `async def fetch_one(session, url)` function that takes a `ClientSession` and URL, and performs a `session.get(url)`.
3.Define an `async def main()` function that:
      *Records the `start_time`.
      *Creates a single `aiohttp.ClientSession()`.
      *Creates a list of tasks (e.g., `tasks = []`).
      *Loops 3 times, creating a task for `fetch_one()` (using the *same* session) and appending it to the list.
      *Uses `await asyncio.gather(*tasks)` to run all fetches concurrently.
      *Prints the total time.
      ***Observation:** The total time will be close to the time of the *single slowest* request (e.g., \~0.5s total).

-----

### 7\. Simulating Slow Work

**Objective:** Use a slow endpoint to make the benefit of `asyncio.gather()` obvious.

**Task:**

1.Modify Exercise 6.
2.Use the URL `https://httpbin.org/delay/2` (which forces a 2-second wait).
3.Run 3 requests to this URL *sequentially* (by `await`ing them one by one). Time it. It will take \~6 seconds.
4.Now, run the same 3 requests *concurrently* using `asyncio.gather()`. Time it. It will take only \~2 seconds.

-----

### 8\. Handling `asyncio.TimeoutError`

**Objective:** Learn to handle requests that take too long.

**Task:**

1.Import `asyncio` and `aiohttp`.
2.Define an `async def fetch_slow()` that:
      *Uses `aiohttp` to request `https://httpbin.org/delay/5` (a 5-second delay).
      *Prints "Request complete."
3.In `main()`, try to run this coroutine using `await asyncio.wait_for(fetch_slow(), timeout=3.0)`.
4.  Wrap this call in a `try...except asyncio.TimeoutError:` block.
5.  In the `except` block, print "Request timed out. 🚩"

-----

### 9\. Mixing Blocking and Async (The Wrong Way ⚠️)

**Objective:** Understand *why* you cannot mix standard `requests` with `asyncio`.

**Task:**

1.Import `asyncio`, `time`, and `requests`.
2.Define a *synchronous* function `blocking_request()` that uses `requests.get("https://httpbin.org/delay/2")` and prints "Blocking request done."
3.Define an `async def` coroutine `async_task()` that `await`s `asyncio.sleep(1)` and prints "Async task done."
4.In `main()`, try to run them concurrently:
      * `await asyncio.gather(async_task(), blocking_request())`
      * This will fail, but if you (unsafely) wrap the blocking call, e.g. `asyncio.to_thread(blocking_request)`, observe what happens. The `requests` call *blocks the entire event loop* if not handled properly. This demonstrates that `requests` has no place inside an `async def` function (unless run in a separate thread pool).

-----

### 10\. Building a Tiny `aiohttp` Server & Client 📡

**Objective:** Use `aiohttp` to build both a client and a server.

**Task (Part A: The Server):**

1.Create a file `server.py`.
2.Import `aiohttp.web`.
3.Define an `async def handle(request):` that `await`s `asyncio.sleep(1)` and returns `web.json_response({"status": "ok"})`.
4.Create an `app = web.Application()`, add the route `app.add_routes([web.get('/', handle)])`.
5.Run the server using `web.run_app(app, port=8080)`.
6.Run this server in a terminal.

**Task (Part B: The Client):**

1.Create a *separate* file `client.py`.
2.Use the concurrent `aiohttp` pattern from Exercise 6.
3.In your client's `main()`, launch 5 concurrent requests to your local server (`http://localhost:8080/`).
4.Time the execution. It should complete in just over 1 second, proving your server handled all 5 "slow" requests concurrently.
