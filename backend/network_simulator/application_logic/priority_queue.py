import heapq
import random
from decorators import validate_key

class PriorityQueue:
    def __init__(self, arr = None):
        self.heap = []
        arr = arr if arr else []
        for heap_input in arr:
            self.add_task(heap_input)
    
    @validate_key
    def add_task(self, task):
        """
        Add tasks of form (priority_number<float>, data<Obj>) else ValueError
        """
        heapq.heappush(self.heap, task)
    
    def pop_task(self):
        return heapq.heappop(self.heap)
    
    def __repr__(self):
        return str(self.heap)
    
    def __len__(self):
        return len(self.heap)