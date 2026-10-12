class Solution {
public:
    int maxSum(vector<int>& nums, int k) {
        const long long MOD = 1e9 + 7;
        vector<int> bits(32, 0);

        for (int num : nums) {
            for (int b = 0; b < 32; b++) {
                if (num & (1LL << b)) {
                    bits[b]++;
                }
            }
        }

        long long answer = 0;

        for (int i = 0; i < k; i++) {
            long long value = 0;

            for (int b = 0; b < 32; b++) {
                if (bits[b] > 0) {
                    value |= (1LL << b);
                    bits[b]--;
                }
            }

            answer = (answer + value * value) % MOD;
        }

        return answer;
    }
};
