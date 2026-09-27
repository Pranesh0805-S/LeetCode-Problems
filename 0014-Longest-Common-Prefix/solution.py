class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        if not strs:
            return ""
        
        benchmark = strs[0]
        
        for i, char in enumerate(benchmark):
            for s in strs[1:]:
                if i == len(s) or s[i] != char:
                    return benchmark[:i]
                    
        return benchmark
