class Solution {
public:
    vector<vector<string>> solveNQueens(int n) {
        vector<vector<string>> ans;
        vector<string> board(n, string(n, '.'));

        vector<bool> col(n, false);
        vector<bool> diag1(2 * n - 1, false);
        vector<bool> diag2(2 * n - 1, false);

        function<void(int)> backtrack = [&](int row) {
            if (row == n) {
                ans.push_back(board);
                return;
            }

            for (int c = 0; c < n; c++) {
                int d1 = row - c + n - 1;
                int d2 = row + c;

                if (col[c] || diag1[d1] || diag2[d2]) {
                    continue;
                }

                board[row][c] = 'Q';
                col[c] = diag1[d1] = diag2[d2] = true;

                backtrack(row + 1);

                board[row][c] = '.';
                col[c] = diag1[d1] = diag2[d2] = false;
            }
        };

        backtrack(0);
        return ans;
    }
};
