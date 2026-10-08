class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n == 0:
            return 1.0
            
        if n < 0:
            x = 1.0 / x
            n = -n
            
        result = 1.0
        curr_product = x
        
        while n > 0:
            if n % 2 == 1:
                result *= curr_product
            
            curr_product *= curr_product
            n //= 2
            
        return result
