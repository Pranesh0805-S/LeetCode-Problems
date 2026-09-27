class Solution {
public:
    vector<string> letterCombinations(string digits) {

        if (digits.empty()) {
            return {};
        }

        vector<string> phone = {
            "",     
            "",     
            "abc",  
            "def",  
            "ghi",  
            "jkl",  
            "mno",  
            "pqrs", 
            "tuv",  
            "wxyz"  
        };

        vector<string> result;
        string current;

        backtrack(0, digits, phone, current, result);

        return result;
    }

private:
    void backtrack(
        int index,
        string& digits,
        vector<string>& phone,
        string& current,
        vector<string>& result
    ) {

        if (index == digits.length()) {
            result.push_back(current);
            return;
        }

        string letters = phone[digits[index] - '0'];

        for (char ch : letters) {

            current.push_back(ch);

            backtrack(
                index + 1,
                digits,
                phone,
                current,
                result
            );

            current.pop_back();
        }
    }
};
