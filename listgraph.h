#include <vector>
#include <cassert>
#include <unordered_map>

using namespace std;

class ListGraph {
public:
    ListGraph(size_t size) : adjLists(size) {}

    ListGraph(const ListGraph& graph) {
        adjLists.resize(graph.VerticesCount());
        for (int i = 0; i < graph.VerticesCount(); ++i)
            adjLists[i] = graph.GetNextVertices(i);
    }

    void AddEdge(int from, int to, double weight) {
        assert(0 <= from && from < adjLists.size());
        assert(0 <= to && to < adjLists.size());
        adjLists[from].push_back(to);
        adjLists[to].push_back(from);
        edgeWeights[{from, to}] = weight;
        edgeWeights[{to, from}] = weight;
    }

    int VerticesCount() const {
        return adjLists.size();
    }

    vector<int> GetNextVertices(int vertex) const {
        assert(0 <= vertex && vertex < adjLists.size());
        return adjLists[vertex];
    }

    vector<int> GetPrevVertices(int vertex) const {
        return GetNextVertices(vertex);
    }

    double GetEdgeWeight(int from, int to) const {
        return edgeWeights.at({from, to});
    }

    vector<tuple<int, int, double>> GetEdges() const {
        vector<tuple<int, int, double>> edges;
        for (int i = 0; i < adjLists.size(); ++i)
            for (int to : adjLists[i])
                if (i < to)
                    edges.emplace_back(i, to, GetEdgeWeight(i, to));
        return edges;
    }

private:
    struct pair_hash {
        template <class T1, class T2>
        std::size_t operator()(const std::pair<T1, T2>& pair) const {
            auto h1 = std::hash<T1>{}(pair.first);
            auto h2 = std::hash<T2>{}(pair.second);
            return h1 ^ h2;
        }
    };
    vector<vector<int>> adjLists;
    unordered_map<pair<int, int>, double, pair_hash> edgeWeights;
};
