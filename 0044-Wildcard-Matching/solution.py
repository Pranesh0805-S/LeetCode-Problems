class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        s_ptr = 0
        p_ptr = 0
        match_idx = 0
        star_idx = -1

        s_len, p_len = len(s), len(p)

        while s_ptr < s_len:
            if p_ptr < p_len and (p[p_ptr] == '?' or p[p_ptr] == s[s_ptr]):
                s_ptr += 1
                p_ptr += 1
            elif p_ptr < p_len and p[p_ptr] == '*':
                star_idx = p_ptr
                match_idx = s_ptr
                p_ptr += 1
            elif star_idx != -1:
                p_ptr = star_idx + 1
                match_idx += 1
                s_ptr = match_idx
            else:
                return False

        while p_ptr < p_len and p[p_ptr] == '*':
            p_ptr += 1

        return p_ptr == p_len
