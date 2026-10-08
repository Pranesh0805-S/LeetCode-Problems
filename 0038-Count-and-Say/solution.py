class Solution:
    def countAndSay(self, n: int) -> str:
        curr = "1"
        
        for _ in range(n - 1):
            next_seq = []
            i = 0
            m = len(curr)
            
            while i < m:
                count = 1
                while i + 1 < m and curr[i] == curr[i + 1]:
                    i += 1
                    count += 1
                
                next_seq.append(str(count))
                next_seq.append(curr[i])
                i += 1
                
            curr = "".join(next_seq)
            
        return curr
