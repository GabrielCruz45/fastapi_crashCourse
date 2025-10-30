# What is a python decorator?
# A decorator is a function that takes another function as an argument.
# It's designed to add new behaviour to that function without modifying its source.

def my_decorator(func):
    def wrapper(): # This is where the new behaviour is defined
        print(f"The beggining game.") # Runs before the wrapped function
        func() # Wrapped function
        print(f"The end game.") # Runs after the wrapped function
    return wrapper # my_decorator function returns the wrapper *function object* itself.



@my_decorator # @ is syntactic sugar (a shortcut) that tells python 
# "take the next function and pass it as an argument to `my_decorator`"
def middle_game():
    print(f"The middle game!")
# Because the @my_decorator line above it, this function is *not just* 
# middle_game anymore. Python has already processed it, 
# so the name middle_fame now actually refers to the wrapper function returned by 
# the my_decorator
   
   
# the following line now points o the wrapper function and executes the wrapper's code
# the function is already "decorated" 
middle_game()

import time


def timer(func):
    def wrapper(*args, **kwargs): 
    # *args, **kwargs -> tells wrapper that it can take any number and type of arguments
    # makes decorator function more reusable
        start = time.time()
        result = func(*args, **kwargs) 
        # pass variable amount of ? type arguments to func(), inside the wrapper
        end = time.time()
        print(f'{func.__name__} took {end-start:.2f} seconds to run!')
        return result
    return wrapper


@timer
def slow_function():
    time.sleep(2)
    print("Function complete!")
    

@timer
def some_math(a, b):
    return (a * b) / 3
    
    
slow_function()
some_math(20, 50)


import random

# this is called the "3-function Decorator Factory Pattern"
def retry_on_failure(max_retries=3): # Runs once at load time, its only job is to receive arguments
    def decorator(func): # Runs once at load time, its only job is to receive the original function
        def wrapper(*args, **kwargs): # Runs everytime unstable_function is called
            retries = 0
            while(retries < max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    print(f'Error: {e} Retrying {retries}/{max_retries}')
            print("Failed after maximum retries.")
        return wrapper # what decorator(func) returns, 
    return decorator # what retry_on_failure(...) returns,

@retry_on_failure(max_retries=5)
def unstable_function():
    if random.choice([True, False]):
        raise ValueError("Random Failure!")
    print("Success!")
    
unstable_function()