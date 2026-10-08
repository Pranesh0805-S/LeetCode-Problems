class Solution:
    def searchRange(self, nums: list[int], target: int) -> list[int]:
        def find_bound(is_first: bool) -> int:
            left, right = 0, len(nums) - 1
            bound = -1
            
            while left <= right:
                mid = (left + right) // 2
                
                if nums[mid] == target:
                    bound = mid
                    if is_first:
                        right = mid - 1 
                    else:
                        left = mid + 1
                elif nums[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1
                    
            return bound

        left_idx = find_bound(is_first=True)
        if left_idx == -1:
            return [-1, -1]
            
        right_idx = find_bound(is_first=False)
        return [left_idx, right_idx]
