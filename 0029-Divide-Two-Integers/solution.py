class Solution:
    def divide(self, dividend: int, divisor: int) -> int:
        MAX_INT = 2**31 - 1
        MIN_INT = -2**31

        if dividend == MIN_INT and divisor == -1:
            return MAX_INT

        negative = (dividend < 0) ^ (divisor < 0)

        a, b = abs(dividend), abs(divisor)
        quotient = 0

        while a >= b:
            temp_b = b
            multiple = 1
            
            while a >= (temp_b << 1):
                temp_b <<= 1
                multiple <<= 1

            a -= temp_b
            quotient += multiple

        if negative:
            quotient = -quotient

        return min(max(quotient, MIN_INT), MAX_INT)
