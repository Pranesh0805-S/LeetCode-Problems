class Solution {
public:
    long long minSumSquareDiff(vector<int>& nums1,
                               vector<int>& nums2,
                               int k1, int k2) {

        int n = nums1.size();
        long long k = (long long)k1 + k2;

        vector<int> diff(n);
        int maxDiff = 0;

        long long total = 0;

        for (int i = 0; i < n; i++) {
            diff[i] = abs(nums1[i] - nums2[i]);
            maxDiff = max(maxDiff, diff[i]);
            total += 1LL * diff[i] * diff[i];
        }

        if (k >= accumulate(diff.begin(), diff.end(), 0LL))
            return 0;

        int left = 0, right = maxDiff;

        while (left < right) {
            int mid = left + (right - left) / 2;
            long long needed = 0;

            for (int d : diff) {
                if (d > mid)
                    needed += d - mid;
            }

            if (needed <= k)
                right = mid;
            else
                left = mid + 1;
        }

        int limit = left;
        long long needed = 0;
        long long answer = 0;

        for (int d : diff) {
            if (d > limit) {
                needed += d - limit;
                d = limit;
            }

            answer += 1LL * d * d;
        }

        long long remaining = k - needed;

        if (limit > 0) {
            for (int d : diff) {
                if (remaining == 0)
                    break;

                if (d >= limit) {
                    answer -= 1LL * limit * limit;
                    answer += 1LL * (limit - 1) * (limit - 1);
                    remaining--;
                }
            }
        }

        return answer;
    }
};
