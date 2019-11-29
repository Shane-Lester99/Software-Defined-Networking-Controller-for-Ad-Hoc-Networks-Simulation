import heapq
import random
from decorators import validate_key

class PriorityQueue:
    def __init__(self, arr = None):
        arr = arr if arr else []
        heapq.heapify(arr)
        self.heap = arr
    
    @validate_key
    def add_task(self, task):
        """
        Add tasks of form (priority_number<float>, data<Obj>)
        """
        heapq.heappush(self.heap, task)
    
    def pop_task(self):
        return heapq.heappop(self.heap)
    
    def __repr__(self):
        return str(self.heap)
    
    def __len__(self):
        return len(self.heap)
        
if __name__ == "__main__":
    #q = PriorityQueue([(1.1111, 'a'),(1.1112, 'b'),(1.1113, 'c'),(1.1114,'d')])
    q = PriorityQueue()
    q.add_task((1.123, ['a', 'b', 'c']))
   # while len(q):
#        print(q.pop_task())