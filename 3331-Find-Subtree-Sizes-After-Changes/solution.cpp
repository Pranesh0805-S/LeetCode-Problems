class Solution {
public:
    vector<int> findSubtreeSizes(vector<int>& parent, string s) {
        int n = parent.size();

        vector<vector<int>> children(n);


        for (int i = 1; i < n; i++) {
            children[parent[i]].push_back(i);
        }

        vector<int> newParent(n, -1);
        vector<int> last(26, -1);
        vector<int> previous(n, -1);

 
        stack<pair<int, bool>> st;
        st.push({0, true});

        while (!st.empty()) {
            auto [u, entering] = st.top();
            st.pop();

            int c = s[u] - 'a';

            if (entering) {
                previous[u] = last[c];

  
                newParent[u] = (last[c] != -1) ? last[c] : parent[u];

                last[c] = u;

                st.push({u, false});

                for (int v : children[u]) {
                    st.push({v, true});
                }
            } 
            else {

                last[c] = previous[u];
            }
        }


        vector<vector<int>> newChildren(n);

        for (int i = 1; i < n; i++) {
            newChildren[newParent[i]].push_back(i);
        }


        vector<int> order;
        stack<int> nodes;
        nodes.push(0);

        while (!nodes.empty()) {
            int u = nodes.top();
            nodes.pop();

            order.push_back(u);

            for (int v : newChildren[u]) {
                nodes.push(v);
            }
        }

        vector<int> ans(n, 1);


        for (int i = n - 1; i >= 0; i--) {
            int u = order[i];

            if (newParent[u] != -1) {
                ans[newParent[u]] += ans[u];
            }
        }

        return ans;
    }
};
