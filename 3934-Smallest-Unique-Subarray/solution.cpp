class Solution {
public:
    int smallestUniqueSubarray(vector<int>& nums) {
        int n = nums.size();

        vector<int> sa(n), rank(n), newRank(n);

        vector<int> vals = nums;
        sort(vals.begin(), vals.end());
        vals.erase(unique(vals.begin(), vals.end()), vals.end());

        for (int i = 0; i < n; i++) {
            sa[i] = i;
            rank[i] = lower_bound(vals.begin(), vals.end(), nums[i])
                      - vals.begin();
        }

        for (int len = 1; len < n; len *= 2) {
            sort(sa.begin(), sa.end(), [&](int a, int b) {
                if (rank[a] != rank[b])
                    return rank[a] < rank[b];

                int ra = (a + len < n) ? rank[a + len] : -1;
                int rb = (b + len < n) ? rank[b + len] : -1;

                return ra < rb;
            });

            newRank[sa[0]] = 0;

            for (int i = 1; i < n; i++) {
                int a = sa[i - 1];
                int b = sa[i];

                int a2 = (a + len < n) ? rank[a + len] : -1;
                int b2 = (b + len < n) ? rank[b + len] : -1;

                newRank[b] = newRank[a] +
                    (rank[a] != rank[b] || a2 != b2);
            }

            rank = newRank;

            if (rank[sa[n - 1]] == n - 1)
                break;
        }

        vector<int> pos(n);

        for (int i = 0; i < n; i++) {
            pos[sa[i]] = i;
        }

        vector<int> lcp(n, 0);
        int h = 0;

        for (int i = 0; i < n; i++) {
            int p = pos[i];

            if (p == 0) continue;

            int j = sa[p - 1];

            while (i + h < n && j + h < n &&
                   nums[i + h] == nums[j + h]) {
                h++;
            }

            lcp[p] = h;

            if (h > 0) h--;
        }

        int ans = n;

        for (int i = 0; i < n; i++) {
            int common = 0;

            if (i > 0)
                common = max(common, lcp[i]);

            if (i + 1 < n)
                common = max(common, lcp[i + 1]);

            int shortestUnique = common + 1;

            if (shortestUnique <= n - sa[i]) {
                ans = min(ans, shortestUnique);
            }
        }

        return ans;
    }
};
