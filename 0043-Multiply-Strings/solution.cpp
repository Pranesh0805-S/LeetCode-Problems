class Solution {
public:
    string multiply(string num1, string num2) {
        if (num1 == "0" || num2 == "0") {
            return "0";
        }

        int n = num1.size();
        int m = num2.size();

        vector<int> result(n + m, 0);

        for (int i = n - 1; i >= 0; i--) {
            for (int j = m - 1; j >= 0; j--) {
                int a = num1[i] - '0';
                int b = num2[j] - '0';

                int product = a * b + result[i + j + 1];

                result[i + j + 1] = product % 10;
                result[i + j] += product / 10;
            }
        }

        string answer;

        for (int digit : result) {
            if (!(answer.empty() && digit == 0)) {
                answer += to_string(digit);
            }
        }

        return answer;
    }
};
