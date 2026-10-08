class Solution:
    def combinationSum2(self, candidates: list[int], target: int) -> list[list[int]]:
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

                if i > start and val == candidates[i - 1]:
                    continue

                combo.append(val)
                backtrack(remain - val, combo, i + 1)
                combo.pop()

        backtrack(target, [], 0)
        return res
