class Solution {
public:
    string countAndSay(int n) {

        string result = "1";

        for (int step = 2; step <= n; step++) {

            string next = "";

            int i = 0;

            while (i < result.size()) {

                char digit = result[i];
                int count = 0;

                while (i < result.size() && result[i] == digit) {
                    count++;
                    i++;
                }

                next += to_string(count);
                next += digit;
            }

            result = next;
        }

        return result;
    }
};
