from .consts import READY_MEM_NAME, READY_MEM_SIZE

from typing import List
from multiprocessing import Process, Queue
from multiprocessing.shared_memory import SharedMemory

class ProcessManager:
    def __init__(self):
        self._process_pool: List[Process] = []
        self._ready_mem = SharedMemory(name=READY_MEM_NAME, create=True, size=READY_MEM_SIZE)
        self._ready_mem.buf[0] = 0
        self.results_queue = Queue()
    
    def add_process(self, target, args):
        self._process_pool.append(
            Process(target=target, args=args)
        )
    
    def start_processes(self):
        for proc in self._process_pool:
            proc.start()
    
    def wait_until_ready(self):
        for _ in self._process_pool:
            self.results_queue.get()
    
    def trigger_ready(self):
        self._ready_mem.buf[0] = 1
    
    def results(self):
        for _ in self._process_pool:
            yield self.results_queue.get()
    
    def close(self):
        for proc in self._process_pool:
            proc.terminate()
        self._ready_mem.unlink()
        self._ready_mem.buf[0] = 0
        self._ready_mem.close()
        self.results_queue.close()
