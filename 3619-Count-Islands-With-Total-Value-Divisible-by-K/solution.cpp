
class Solution {
public:
    int m, n;

    long long dfs(vector<vector<int>>& grid, int r, int c) {
        if (r < 0 || c < 0 || r >= m || c >= n ||
            grid[r][c] == 0) {
            return 0;
        }

        long long value = grid[r][c];
        grid[r][c] = 0;

        value += dfs(grid, r + 1, c);
        value += dfs(grid, r - 1, c);
        value += dfs(grid, r, c + 1);
        value += dfs(grid, r, c - 1);

        return value;
    }

    int countIslands(vector<vector<int>>& grid, int k) {
        m = grid.size();
        n = grid[0].size();

        int count = 0;

        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (grid[r][c] > 0) {
                    long long sum = dfs(grid, r, c);

                    if (sum % k == 0) {
                        count++;
                    }
                }
            }
        }

        return count;
    }
};
