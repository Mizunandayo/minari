"""Demo flaky tests for Minari"""


import threading
import time
import uuid
import pytest






# Category 1 async/timing
class _AsyncJob:
    def __init__(self) -> None:
        self.done = False
    
    def start(self) -> None:
        def _work() -> None:
            time.sleep(0.05)
            self.done = True
        
        threading.Thread(target=_work, daemon=True).start()



def test_checkout_flow_async_completion():
    job = _AsyncJob()
    job.start()
    time.sleep(0.04)          
    assert job.done is True  







# Category 5 data isolation
_SHARED_TABLE: list[str] = []

def _seed(rows: int) -> None:
    for _ in range(rows):
        _SHARED_TABLE.append("item")




def test_checkout_items_count_isolation():
    _SHARED_TABLE.clear()
    _seed(3)
    assert len(_SHARED_TABLE) == 3







