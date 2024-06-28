

def search_cars(query):
    return [f"Car result for {query}"]

def search_numbers(query):
    return [f"Option {i+1} for {query}" for i in range(4)] 
