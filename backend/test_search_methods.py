from duckduckgo_search import DDGS
import time

print("Testing different search approaches...")

# Method 1: Basic search
try:
    print("\n1. Basic search with DDGS:")
    with DDGS() as ddgs:
        results = [r for r in ddgs.text("Python programming", max_results=3)]
        print(f"   Results: {len(results)}")
        if results:
            print(f"   First result: {results[0].get('title', 'N/A')}")
except Exception as e:
    print(f"   Error: {e}")

# Method 2: Without context manager
try:
    print("\n2. Without context manager:")
    ddgs = DDGS()
    results = list(ddgs.text("Python programming", max_results=3))
    print(f"   Results: {len(results)}")
    if results:
        print(f"   First result: {results[0].get('title', 'N/A')}")
except Exception as e:
    print(f"   Error: {e}")

# Method 3: Check if timeout helps
try:
    print("\n3. With timeout and region:")
    ddgs = DDGS(timeout=20)
    results = list(ddgs.text("Python", region='wt-wt', max_results=3))
    print(f"   Results: {len(results)}")
    if results:
        print(f"   First result: {results[0].get('title', 'N/A')}")
except Exception as e:
    print(f"   Error: {e}")

#Method 4: Try news search instead
try:
    print("\n4. News search:")
    ddgs = DDGS()
    results = list(ddgs.news("Python", max_results=3))
    print(f"   Results: {len(results)}")
    if results:
        print(f"   First result: {results[0].get('title', 'N/A')}")
except Exception as e:
    print(f"   Error: {e}")
