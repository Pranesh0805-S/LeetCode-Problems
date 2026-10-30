class Solution {
public:
    int shortestPath(int n, vector<vector<int>>& edges,
                     string labels, int k) {

        vector<vector<pair<int, int>>> adj(n);

        for (auto& e : edges) {
            adj[e[0]].push_back({e[1], e[2]});
        }

        const long long INF = LLONG_MAX;

        vector<vector<long long>> dist(
            n, vector<long long>(k + 1, INF)
        );

        using State = tuple<long long, int, int>;

        priority_queue<State, vector<State>, greater<State>> pq;

        dist[0][1] = 0;
        pq.push({0, 0, 1});

        while (!pq.empty()) {
            auto [cost, u, run] = pq.top();
            pq.pop();

            if (cost != dist[u][run]) {
                continue;
            }

            if (u == n - 1) {
                return (int)cost;
            }

            for (auto [v, w] : adj[u]) {

                int nextRun;

                if (labels[u] == labels[v]) {
                    nextRun = run + 1;
                } else {
                    nextRun = 1;
                }

                if (nextRun > k) {
                    continue;
                }

                long long newCost = cost + w;

                if (newCost < dist[v][nextRun]) {
                    dist[v][nextRun] = newCost;

                    pq.push({
                        newCost,
                        v,
                        nextRun
                    });
                }
            }
        }

        return -1;
    }
};
