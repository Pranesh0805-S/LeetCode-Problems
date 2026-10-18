class Solution {
private:
    static const long long MOD = 1'000'000'007;
    vector<vector<long long>> comb;

    long long countWays(vector<int>& nums) {
        int n = nums.size();

        if (n <= 2) {
            return 1;
        }

        int root = nums[0];
        vector<int> left, right;

        for (int i = 1; i < n; i++) {
            if (nums[i] < root) {
                left.push_back(nums[i]);
            } else {
                right.push_back(nums[i]);
            }
        }

        long long leftWays = countWays(left);
        long long rightWays = countWays(right);

        long long ways = comb[n - 1][left.size()];
        ways = ways * leftWays % MOD;
        ways = ways * rightWays % MOD;

        return ways;
    }

public:
    int numOfWays(vector<int>& nums) {
        int n = nums.size();

        comb.assign(n + 1, vector<long long>(n + 1, 0));

        for (int i = 0; i <= n; i++) {
            comb[i][0] = comb[i][i] = 1;

            for (int j = 1; j < i; j++) {
                comb[i][j] =
                    (comb[i - 1][j - 1] + comb[i - 1][j]) % MOD;
            }
        }

        return (countWays(nums) - 1 + MOD) % MOD;
    }
};
