class Solution {
public:
    string maxSumOfSquares(int num, int sum) {
        if (sum > 9 * num) {
            return "";
        }

        string result = "";

        for (int i = 0; i < num; i++) {
            int digit = min(9, sum);
            result += to_string(digit);
            sum -= digit;
        }

        return result;
    }
};
