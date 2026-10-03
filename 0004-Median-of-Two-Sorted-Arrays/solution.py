class Solution:
    def findMedianSortedArrays(self, nums1: list[int], nums2: list[int]) -> float:
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1

        m, n = len(nums1), len(nums2)
        half = (m + n + 1) // 2
        low, high = 0, m

        while low <= high:
            i = (low + high) // 2
            j = half - i

            a_left = nums1[i - 1] if i > 0 else float('-inf')
            a_right = nums1[i] if i < m else float('inf')
            b_left = nums2[j - 1] if j > 0 else float('-inf')
            b_right = nums2[j] if j < n else float('inf')

            if a_left <= b_right and b_left <= a_right:
                if (m + n) % 2 == 1:
                    return float(max(a_left, b_left))
                return (max(a_left, b_left) + min(a_right, b_right)) / 2.0
            
            elif a_left > b_right:
                high = i - 1
            else:
                low = i + 1

        return 0.0
