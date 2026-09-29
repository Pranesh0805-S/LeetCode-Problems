class Solution {
public:
    bool hasValidPath(vector<vector<char>>& grid) {

        int m = grid.size();
        int n = grid[0].size();

        int length = m + n - 1;

        if (length % 2 == 1) {
            return false;
        }

        vector<vector<bool>> dp(
            n,
            vector<bool>(length + 1, false)
        );

        if (grid[0][0] == '(') {
            dp[0][1] = true;
        } else {
            return false;
        }

        for (int i = 0; i < m; i++) {

            for (int j = 0; j < n; j++) {

                if (i == 0 && j == 0) {
                    continue;
                }

                vector<bool> current(length + 1, false);

                for (int balance = 0; balance <= length; balance++) {

                    bool reachable = false;

                    if (i > 0) {
                        reachable = reachable || dp[j][balance];
                    }

                    if (j > 0) {
                        reachable = reachable || dp[j - 1][balance];
                    }

                    if (!reachable) {
                        continue;
                    }

                    int newBalance = balance;

                    if (grid[i][j] == '(') {
                        newBalance++;
                    } else {
                        newBalance--;
                    }

                    if (newBalance >= 0) {
                        current[newBalance] = true;
                    }
                }

                dp[j] = current;
            }
        }

        return dp[n - 1][0];
    }
};
