#include "KruskalMST.h"
#include <algorithm>

using namespace std;

class DSU {
public:
    DSU(int n) : parent(n), rank(n, 0) {
        for (int i = 0; i < n; ++i)
            parent[i] = i;
    }

    int find(int v) {
        if (v == parent[v])
            return v;
        return parent[v] = find(parent[v]);
    }

    bool unite(int u, int v) {
        int rootU = find(u);
        int rootV = find(v);
        if (rootU != rootV) {
            if (rank[rootU] < rank[rootV])
                swap(rootU, rootV);
            parent[rootV] = rootU;
            if (rank[rootU] == rank[rootV])
                ++rank[rootU];
            return true;
        }
        return false;
    }

private:
    vector<int> parent, rank;
};

double KruskalMST::FindMSTWeight(const vector<tuple<int, int, double>>& edges, int verticesCount) {
    DSU dsu(verticesCount);
    double mstWeight = 0;

    auto sortedEdges = edges;
    sort(sortedEdges.begin(), sortedEdges.end(), [](const auto& a, const auto& b) {
        return get<2>(a) < get<2>(b);
    });

    for (const auto& edge : sortedEdges) {
        int from = get<0>(edge);
        int to = get<1>(edge);
        double weight = get<2>(edge);

        if (dsu.unite(from, to))
            mstWeight += weight;
    }

    return mstWeight;
}
