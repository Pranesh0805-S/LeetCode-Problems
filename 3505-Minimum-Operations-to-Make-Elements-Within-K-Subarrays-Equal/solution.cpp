class Solution {
public:
    long long minOperations(vector<int>& nums, int x, int k) {
        int n = nums.size();

        vector<long long> cost(n - x + 1);

        multiset<int> low, high;
        long long sumLow = 0, sumHigh = 0;

        auto rebalance = [&]() {
            while (low.size() > high.size() + 1) {
                int v = *low.rbegin();
                low.erase(prev(low.end()));
                sumLow -= v;
                high.insert(v);
                sumHigh += v;
            }
            while (low.size() < high.size()) {
                int v = *high.begin();
                high.erase(high.begin());
                sumHigh -= v;
                low.insert(v);
                sumLow += v;
            }
        };

        auto add = [&](int v) {
            if (low.empty() || v <= *low.rbegin()) {
                low.insert(v);
                sumLow += v;
            } else {
                high.insert(v);
                sumHigh += v;
            }
            rebalance();
        };

        auto remove = [&](int v) {
            auto it = low.find(v);
            if (it != low.end()) {
                low.erase(it);
                sumLow -= v;
            } else {
                it = high.find(v);
                high.erase(it);
                sumHigh -= v;
            }
            rebalance();
        };

        auto getCost = [&]() -> long long {
            long long med = *low.rbegin();
            return med * (long long)low.size() - sumLow
                 + sumHigh - med * (long long)high.size();
        };

        for (int i = 0; i < x; ++i) add(nums[i]);
        cost[0] = getCost();

        for (int i = x; i < n; ++i) {
            remove(nums[i - x]);
            add(nums[i]);
            cost[i - x + 1] = getCost();
        }

        const long long INF = LLONG_MAX / 4;
        vector<long long> dp(k + 1, INF);
        dp[0] = 0;

        for (int i = 0; i < n; ++i) {
            for (int j = k; j >= 1; --j) {
                if (i + 1 >= x && dp[j - 1] != INF) {
                    dp[j] = min(dp[j], dp[j - 1] + cost[i - x + 1]);
                }
            }
        }

        vector<vector<long long>> best(n + 1, vector<long long>(k + 1, INF));
        best[0][0] = 0;

        for (int i = 1; i <= n; ++i) {
            for (int j = 0; j <= k; ++j) {
                best[i][j] = best[i - 1][j];

                if (j > 0 && i >= x && best[i - x][j - 1] != INF) {
                    best[i][j] = min(
                        best[i][j],
                        best[i - x][j - 1] + cost[i - x]
                    );
                }
            }
        }

        return best[n][k];
    }
};
