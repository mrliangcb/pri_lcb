from typing import List

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap_size = len(nums)
        self.build_max_heap(nums, heap_size)

        for i in range(len(nums)-1, len(nums)-k, -1):
            nums[0], nums[i] = nums[i], nums[0]
            heap_size -= 1
            self.max_heapify(nums, 0, heap_size)
        return nums[0]

    def build_max_heap(self, nums, heap_size):
        for i in range(heap_size // 2, -1, -1):
            self.max_heapify(nums, i, heap_size)


    def max_heapify(self, nums, i, heap_size):
        left = i * 2 + 1
        right = i * 2 + 2
        largest = i
        if left < heap_size and nums[left] > nums[largest]:
            largest = left
        if right < heap_size and nums[right] > nums[largest]:
            largest = right
        if (largest != i):
            nums[i], nums[largest] = nums[largest], nums[i]
            self.max_heapify(nums, largest, heap_size)

# top k算法
class Solution2:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap_size = len(nums)
        self.build_max_heap(nums, heap_size)

        for i in range(len(nums)-1, len(nums)-k, -1):
            nums[0], nums[i] = nums[i], nums[0]
            heap_size -= 1
            self.max_heapify(nums, 0, heap_size)
        return nums[0]

    def build_max_heap(self, nums, heap_size):
        for i in range(heap_size // 2, -1, -1):
            self.max_heapify(nums, i, heap_size)


    def max_heapify(self, nums, i, heap_size):
        left = i * 2 + 1
        right = i * 2 + 2
        largest = i
        if left < heap_size and nums[left] > nums[largest]:
            largest = left
        if right < heap_size and nums[right] > nums[largest]:
            largest = right
        if (largest != i):
            nums[i], nums[largest] = nums[largest], nums[i]
            self.max_heapify(nums, largest, heap_size)

examm=Solution2()

result=examm.findKthLargest([10,5,298,34,50,18,38,47,58,100,0.1,0.5],0)
print(result)







