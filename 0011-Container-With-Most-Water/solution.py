class Solution:
    def maxArea(self, height: list[int]) -> int:
        left, right = 0, len(height) - 1
        max_water = 0
        
        while left < right:
            width = right - left
            h = min(height[left], height[right])
            current_area = width * h
            max_water = max(max_water, current_area)
            
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
                
        return max_water
