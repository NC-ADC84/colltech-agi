import asyncio

def pytest_pyfunc_call(pyfuncitem):
    """Run coroutine test functions using asyncio.run when pytest-asyncio isn't installed."""
    testfn = pyfuncitem.obj
    if asyncio.iscoroutinefunction(testfn):
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(testfn())
        finally:
            try:
                loop.close()
            except Exception:
                pass
    # If not coroutine, let pytest handle
    return None
