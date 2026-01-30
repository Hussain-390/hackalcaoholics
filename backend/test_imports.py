import sys
sys.path.insert(0, '.')

print("Testing imports...")

try:
    from models.schemas import ResearchRequest
    print("✅ ResearchRequest imported")
except Exception as e:
    print(f"❌ ResearchRequest error: {e}")

try:
    from agents.coordinator import CoordinatorAgent
    print("✅ CoordinatorAgent imported")
except Exception as e:
    print(f"❌ CoordinatorAgent error: {e}")

try:
    coordinator = CoordinatorAgent()
    print("✅ CoordinatorAgent instantiated")
except Exception as e:
    print(f"❌ CoordinatorAgent instantiation error: {e}")

print("\n🧪 Testing simple research...")
try:
    import asyncio
    async def test():
        result = await coordinator.research("test query")
        print(f"✅ Research completed!")
        print(f"Summary: {result.executive_summary[:100]}...")
        return result
    
    report = asyncio.run(test())
    print("✅ ALL TESTS PASSED!")
except Exception as e:
    import traceback
    print(f"❌ Research failed: {e}")
    traceback.print_exc()
