from collections import Counter

class Solution:
    def findSubstring(self, s: str, words: list[str]) -> list[int]:
        if not s or not words:
            return []

        word_len = len(words[0])
        word_count = len(words)
        total_len = word_len * word_count
        n = len(s)

        if n < total_len:
            return []

        word_freq = Counter(words)
        result = []

        for offset in range(word_len):
            left = offset
            right = offset
            current_map = Counter()
            matched_words = 0

            while right + word_len <= n:
                w = s[right : right + word_len]
                right += word_len

                if w in word_freq:
                    current_map[w] += 1
                    matched_words += 1

                    while current_map[w] > word_freq[w]:
                        left_word = s[left : left + word_len]
                        current_map[left_word] -= 1
                        matched_words -= 1
                        left += word_len

                    if matched_words == word_count:
                        result.append(left)
                else:
                    current_map.clear()
                    matched_words = 0
                    left = right

        return result
