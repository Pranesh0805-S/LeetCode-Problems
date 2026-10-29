class Solution {
public:
    vector<bool> palindromePath(int n, vector<vector<int>>& edges, string s, vector<string>& queries) {
        int LOG = 1;
        while ((1 << LOG) <= n) LOG++;

        vector<vector<int>> adj(n);
        for (auto& e : edges) {
            adj[e[0]].push_back(e[1]);
            adj[e[1]].push_back(e[0]);
        }

        vector<int> tin(n), tout(n), depth(n);
        vector<vector<int>> up(LOG, vector<int>(n, 0));
        vector<int> bit(n + 1, 0);
        vector<int> mask(n);
        int timer = 0;

        auto add = [&](int idx, int val) {
            for (idx++; idx <= n; idx += idx & -idx)
                bit[idx] ^= val;
        };

        auto prefix = [&](int idx) {
            int res = 0;
            for (idx++; idx > 0; idx -= idx & -idx)
                res ^= bit[idx];
            return res;
        };

        auto rangeXor = [&](int l, int r, int val) {
            if (val == 0) return;
            add(l, val);
            if (r < n) add(r, val);
        };

        vector<tuple<int, int, bool>> st;
        st.push_back({0, 0, false});

        while (!st.empty()) {
            auto [u, p, exit] = st.back();
            st.pop_back();

            if (exit) {
                tout[u] = timer;
                continue;
            }

            tin[u] = timer++;
            up[0][u] = p;

            for (int j = 1; j < LOG; j++)
                up[j][u] = up[j - 1][up[j - 1][u]];

            st.push_back({u, p, true});

            for (int v : adj[u]) {
                if (v == p) continue;
                depth[v] = depth[u] + 1;
                st.push_back({v, u, false});
            }
        }

        for (int u = 0; u < n; u++) {
            mask[u] = 1 << (s[u] - 'a');
            rangeXor(tin[u], tout[u], mask[u]);
        }

        auto lca = [&](int u, int v) {
            if (depth[u] < depth[v]) swap(u, v);

            int diff = depth[u] - depth[v];
            for (int j = 0; j < LOG; j++)
                if (diff & (1 << j))
                    u = up[j][u];

            if (u == v) return u;

            for (int j = LOG - 1; j >= 0; j--) {
                if (up[j][u] != up[j][v]) {
                    u = up[j][u];
                    v = up[j][v];
                }
            }
            return up[0][u];
        };

        vector<bool> ans;

        for (string& q : queries) {
            string type;
            int u;
            stringstream ss(q);
            ss >> type >> u;

            if (type == "update") {
                char c;
                ss >> c;

                int newMask = 1 << (c - 'a');
                int delta = mask[u] ^ newMask;

                rangeXor(tin[u], tout[u], delta);
                mask[u] = newMask;
            } else {
                int v;
                ss >> v;

                int w = lca(u, v);
                int pathMask = prefix(tin[u]) ^ prefix(tin[v]) ^ mask[w];

                ans.push_back((pathMask & (pathMask - 1)) == 0);
            }
        }

        return ans;
    }
};
