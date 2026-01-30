from duckduckgo_search import DDGS

print("Testing DuckDuckGo Search...")

try:
    ddgs = DDGS()
    print("DDGS object created successfully")
    
    query = "electric vehicles India 2024"
    print(f"\nSearching for: {query}")
    
    results = ddgs.text(query, max_results=5)
    print(f"\nFound {len(list(results))} results")
    
    # Try again with list conversion
    ddgs2 = DDGS()
    results2 = list(ddgs2.text(query, max_results=5))
    print(f"Second attempt: {len(results2)} results")
    
    for i, r in enumerate(results2[:3]):
        print(f"\n{i+1}. {r.get('title', 'No title')}")
        print(f"   URL: {r.get('href', 'No URL')}")
        print(f"   Snippet: {r.get('body', 'No snippet')[:100]}...")
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
