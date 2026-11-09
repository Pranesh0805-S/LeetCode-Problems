class Solution {
public:
    vector<int> busiestServers(int k, vector<int>& arrival, vector<int>& load) {
        set<int> available;

        priority_queue<
            pair<long long, int>,
            vector<pair<long long, int>>,
            greater<pair<long long, int>>
        > busy;

        vector<int> count(k, 0);

        for (int i = 0; i < k; i++) {
            available.insert(i);
        }

        for (int i = 0; i < arrival.size(); i++) {
            long long time = arrival[i];

            while (!busy.empty() && busy.top().first <= time) {
                int server = busy.top().second;
                busy.pop();

                available.insert(server);
            }

            if (available.empty()) {
                continue;
            }

            int target = i % k;

            auto it = available.lower_bound(target);

            if (it == available.end()) {
                it = available.begin();
            }

            int server = *it;

            available.erase(it);

            count[server]++;

            busy.push({
                time + load[i],
                server
            });
        }

        int maxCount = *max_element(count.begin(), count.end());

        vector<int> ans;

        for (int i = 0; i < k; i++) {
            if (count[i] == maxCount) {
                ans.push_back(i);
            }
        }

        return ans;
    }
};
