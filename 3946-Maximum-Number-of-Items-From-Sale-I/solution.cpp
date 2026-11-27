class Solution {
public:
    int maximumSaleItems(vector<vector<int>>& items, int budget) {
        int n = items.size();

        vector<int> benefit(n, 0);

        for (int i = 0; i < n; i++) {
            int factor = items[i][0];

            for (int j = 0; j < n; j++) {
                if (i != j && items[j][0] % factor == 0) {
                    benefit[i]++;
                }
            }
        }

        const int NEG = -1000000000;

        vector<int> dp(budget + 1, NEG);
        dp[0] = 0;

        int ans = 0;

        for (int p = budget; p >= 1; p--) {
            vector<int> hasPrice(budget + 1, NEG);

            for (int i = 0; i < n; i++) {
                int price = items[i][1];

                if (price != p) continue;

                int value = 1 + benefit[i];

                for (int c = budget; c >= p; c--) {
                    if (dp[c - p] != NEG) {
                        hasPrice[c] = max(
                            hasPrice[c],
                            dp[c - p] + value
                        );
                    }

                    if (hasPrice[c - p] != NEG) {
                        hasPrice[c] = max(
                            hasPrice[c],
                            hasPrice[c - p] + value
                        );
                    }

                    dp[c] = max(dp[c], dp[c - p] + value);
                }
            }

            for (int c = p; c <= budget; c++) {
                if (hasPrice[c] == NEG) continue;

                int extraCopies = (budget - c) / p;

                ans = max(ans, hasPrice[c] + extraCopies);
            }
        }

        return ans;
    }
};
