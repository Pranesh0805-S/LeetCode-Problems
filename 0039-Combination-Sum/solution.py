class Solution:
    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:
        candidates.sort()
        res = []

        def backtrack(remain: int, combo: list[int], start: int):
            if remain == 0:
                res.append(list(combo))
                return

            for i in range(start, len(candidates)):
                val = candidates[i]
                if val > remain:
                    break

                combo.append(val)
                backtrack(remain - val, combo, i)
                combo.pop()

        backtrack(target, [], 0)
        return res
