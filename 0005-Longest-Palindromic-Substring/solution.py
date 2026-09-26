class Solution:
    def longestPalindrome(self, s: str) -> str:
        if not s or len(s) == 1:
            return s

        start, max_len = 0, 0

        def expand(l: int, r: int) -> tuple[int, int]:
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1
                r += 1
            return l + 1, r - l - 1

        for i in range(len(s)):
            l1, len1 = expand(i, i)
            if len1 > max_len:
                start, max_len = l1, len1

            l2, len2 = expand(i, i + 1)
            if len2 > max_len:
                start, max_len = l2, len2

        return s[start : start + max_len]
