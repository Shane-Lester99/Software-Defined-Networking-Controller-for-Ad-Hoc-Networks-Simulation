import heapq
import random

class PriorityQueue:
    def __init__(self, arr = None):
        arr = arr if arr else []
        heapq.heapify(arr)
        self.heap = arr
    
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
    q = PriorityQueue([(1.1111, 'a'),(1.1112, 'b'),(1.1113, 'c'),(1.1114,'d')])
    # q2 = PriorityQueue()
    # for _ in range(4):
    #     q.add_task((random.randint(1,10), 'z'))
    #     q2.add_task((random.randint(1,10), 'z'))
    print(q)
    while len(q):
        print(q.pop_task())