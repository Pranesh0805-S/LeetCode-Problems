class Solution {
public:
    vector<int> assignTasks(vector<int>& servers, vector<int>& tasks) {
 
        priority_queue<
            pair<int, int>,
            vector<pair<int, int>>,
            greater<pair<int, int>>
        > available;


        using T = tuple<long long, int, int>;
        priority_queue<T, vector<T>, greater<T>> busy;

        int n = servers.size();

        for (int i = 0; i < n; i++) {
            available.push({servers[i], i});
        }

        vector<int> ans(tasks.size());
        long long currentTime = 0;

        for (int i = 0; i < tasks.size(); i++) {


            currentTime = max(currentTime, (long long)i);


            while (!busy.empty() &&
                   get<0>(busy.top()) <= currentTime) {

                auto [finishTime, weight, index] = busy.top();
                busy.pop();

                available.push({weight, index});
            }

            if (available.empty()) {
                currentTime = get<0>(busy.top());

                while (!busy.empty() &&
                       get<0>(busy.top()) <= currentTime) {

                    auto [finishTime, weight, index] = busy.top();
                    busy.pop();

                    available.push({weight, index});
                }
            }

            auto [weight, index] = available.top();
            available.pop();

            ans[i] = index;

 
            busy.push({
                currentTime + tasks[i],
                weight,
                index
            });
        }

        return ans;
    }
};
