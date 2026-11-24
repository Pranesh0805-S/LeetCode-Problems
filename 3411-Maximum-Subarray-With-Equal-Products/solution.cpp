
class Solution {
public:
    int maxLength(vector<int>& nums) {
        int n = nums.size();
        int ans = 0;

        int primes[4] = {2, 3, 5, 7};

        int factors[11][4] = {};

        for (int v = 1; v <= 10; v++) {
            int x = v;

            for (int p = 0; p < 4; p++) {
                while (x % primes[p] == 0) {
                    factors[v][p]++;
                    x /= primes[p];
                }
            }
        }

        for (int i = 0; i < n; i++) {
            int sum[4] = {};
            int mn[4] = {100, 100, 100, 100};
            int mx[4] = {};

            for (int j = i; j < n; j++) {
                for (int p = 0; p < 4; p++) {
                    int e = factors[nums[j]][p];

                    sum[p] += e;
                    mn[p] = min(mn[p], e);
                    mx[p] = max(mx[p], e);
                }

                bool valid = true;

                for (int p = 0; p < 4; p++) {
                    if (sum[p] != mn[p] + mx[p]) {
                        valid = false;
                        break;
                    }
                }

                if (valid) {
                    ans = max(ans, j - i + 1);
                }
            }
        }

        return ans;
    }
};
