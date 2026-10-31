class Solution {
public:
    int uniquePaths(vector<vector<int>>& grid) {
        const int MOD = 1'000'000'007;
        int m = grid.size();
        int n = grid[0].size();

        vector<vector<int>> dp(m, vector<int>(n, 0));
        dp[0][0] = 1;

        auto moveTo = [&](int r, int c, int dir) -> pair<int, int> {
            while (true) {
                if (dir == 0) {
                    c++;
                } else {
                    r++;
                }

                if (r >= m || c >= n) {
                    return {-1, -1};
                }

                if (grid[r][c] == 0) {
                    return {r, c};
                }

                dir ^= 1;
            }
        };

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 1 || dp[i][j] == 0) {
                    continue;
                }

                auto [r1, c1] = moveTo(i, j, 0);
                if (r1 != -1) {
                    dp[r1][c1] = (dp[r1][c1] + dp[i][j]) % MOD;
                }

                auto [r2, c2] = moveTo(i, j, 1);
                if (r2 != -1) {
                    dp[r2][c2] = (dp[r2][c2] + dp[i][j]) % MOD;
                }
            }
        }

        return dp[m - 1][n - 1];
    }
};
