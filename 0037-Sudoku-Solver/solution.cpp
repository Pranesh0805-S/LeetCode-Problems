class Solution {
public:
    bool solveSudoku(vector<vector<char>>& board) {

        for (int i = 0; i < 9; i++) {
            for (int j = 0; j < 9; j++) {

                if (board[i][j] != '.')
                    continue;

                for (char digit = '1'; digit <= '9'; digit++) {

                    if (isValid(board, i, j, digit)) {

                        board[i][j] = digit;

                        if (solveSudoku(board))
                            return true;

                        board[i][j] = '.';
                    }
                }

                return false;
            }
        }

        return true;
    }

private:
    bool isValid(vector<vector<char>>& board,
                 int row, int col, char digit) {

        for (int i = 0; i < 9; i++) {

            if (board[row][i] == digit ||
                board[i][col] == digit) {
                return false;
            }

            int boxRow = 3 * (row / 3) + i / 3;
            int boxCol = 3 * (col / 3) + i % 3;

            if (board[boxRow][boxCol] == digit)
                return false;
        }

        return true;
    }
};
