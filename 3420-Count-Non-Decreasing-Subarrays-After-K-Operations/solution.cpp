class Solution {
public:
    long long countNonDecreasingSubarrays(vector<int>& nums, int k) {
        int n = nums.size();

        deque<pair<int, int>> dq;
        long long cost = 0;
        long long ans = 0;

        int j = n - 1;

        for (int i = n - 1; i >= 0; i--) {
            int num = nums[i];
            int count = 1;

            while (!dq.empty() && dq.back().first < num) {
                auto [nextNum, nextCount] = dq.back();
                dq.pop_back();

                count += nextCount;

                cost += 1LL * (num - nextNum) * nextCount;
            }

            dq.push_back({num, count});

            while (cost > k) {
                auto [rightmostNum, rightmostCount] = dq.front();
                dq.pop_front();

                cost -= rightmostNum - nums[j];
                j--;

                if (rightmostCount > 1) {
                    dq.push_front({
                        rightmostNum,
                        rightmostCount - 1
                    });
                }
            }

            ans += j - i + 1;
        }

        return ans;
    }
};
