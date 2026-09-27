class Solution:
    def myAtoi(self, s: str) -> int:
        n = len(s)
        i = 0
        
        while i < n and s[i] == ' ':
            i += 1
            
        if i == n:
            return 0
        
        sign = 1
        if s[i] == '-':
            sign = -1
            i += 1
        elif s[i] == '+':
            i += 1
            
        num = 0
        while i < n and s[i].isdigit():
            num = num * 10 + int(s[i])
            i += 1
            
        num *= sign
        
        INT_MIN = -2**31
        INT_MAX = 2**31 - 1
        
        if num < INT_MIN:
            return INT_MIN
        if num > INT_MAX:
            return INT_MAX
            
        return num
