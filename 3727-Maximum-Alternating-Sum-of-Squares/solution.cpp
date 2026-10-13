class Solution {
public:
    long long maxAlternatingSum(vector<int>& nums) {
        vector<long long> squares;

        for (int num : nums) {
            squares.push_back(1LL * num * num);
        }

        sort(squares.begin(), squares.end());

        int n = squares.size();
        int positive = (n + 1) / 2;
        long long score = 0;

        for (int i = n - 1; i >= n - positive; i--) {
            score += squares[i];
        }

        for (int i = 0; i < n - positive; i++) {
            score -= squares[i];
        }

        return score;
    }
};
