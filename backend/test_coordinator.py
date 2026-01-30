import sys
sys.path.insert(0, '.')

from agents.coordinator import CoordinatorAgent

print("Testing coordinator...")
coordinator = CoordinatorAgent()

print("Testing research...")
import asyncio

async def test():
    try:
        result = await coordinator.research("What is AI")
        print(f"Success! Found {len(result.sources)} sources")
        print(f"Confidence: {result.confidence_score}")
        return result
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test())
