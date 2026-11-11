class Solution {
public:
    long long minimumCost(int cost1, int cost2, int costBoth,
                          int need1, int need2) {

        int common = min(need1, need2);

        long long ans = 1LL * common * min(costBoth, cost1 + cost2);

        ans += 1LL * (need1 - common) * min(cost1, costBoth);

        ans += 1LL * (need2 - common) * min(cost2, costBoth);

        return ans;
    }
};
