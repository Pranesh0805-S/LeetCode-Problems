class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        if num1 == "0" or num2 == "0":
            return "0"

        m, n = len(num1), len(num2)
        result = [0] * (m + n)

        for i in range(m - 1, -1, -1):
            d1 = ord(num1[i]) - ord('0')
            for j in range(n - 1, -1, -1):
                d2 = ord(num2[j]) - ord('0')
                
                total = d1 * d2 + result[i + j + 1]
                result[i + j + 1] = total % 10
                result[i + j] += total // 10

        start_idx = 0
        while start_idx < len(result) and result[start_idx] == 0:
            start_idx += 1

        return "".join(str(d) for d in result[start_idx:])
