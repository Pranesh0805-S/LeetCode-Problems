class Solution:
    def solveSudoku(self, board: list[list[str]]) -> None:
        rows = [0] * 9
        cols = [0] * 9
        boxes = [0] * 9
        empty_cells = []

        for r in range(9):
            for c in range(9):
                if board[r][c] != '.':
                    d = int(board[r][c]) - 1
                    mask = 1 << d
                    rows[r] |= mask
                    cols[c] |= mask
                    boxes[(r // 3) * 3 + (c // 3)] |= mask
                else:
                    empty_cells.append((r, c))

        def get_candidates(r: int, c: int) -> int:
            b = (r // 3) * 3 + (c // 3)
            used = rows[r] | cols[c] | boxes[b]
            return (~used) & 0x1FF

        def backtrack(remaining: list[tuple[int, int]]) -> bool:
            if not remaining:
                return True

            min_idx = -1
            min_count = 10
            best_mask = 0

            for i, (r, c) in enumerate(remaining):
                mask = get_candidates(r, c)
                count = bin(mask).count('1')
                if count < min_count:
                    min_count = count
                    min_idx = i
                    best_mask = mask
                if min_count == 1:
                    break

            if min_count == 0:
                return False

            r, c = remaining[min_idx]
            box_idx = (r // 3) * 3 + (c // 3)
            next_remaining = remaining[:min_idx] + remaining[min_idx + 1:]

            cand = best_mask
            while cand:
                bit = cand & -cand
                cand -= bit
                d = bit.bit_length()

                board[r][c] = str(d)
                rows[r] |= bit
                cols[c] |= bit
                boxes[box_idx] |= bit

                if backtrack(next_remaining):
                    return True

                board[r][c] = '.'
                rows[r] ^= bit
                cols[c] ^= bit
                boxes[box_idx] ^= bit

            return False

        backtrack(empty_cells)
