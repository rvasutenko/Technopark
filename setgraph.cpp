#include "setgraph.h"

SetGraph::SetGraph(const IGraph& graph) : adjMap(graph.VerticesCount()) {
    for (int from = 0; from < graph.VerticesCount(); ++from)
        for (int to : graph.GetNextVertices(from))
            adjMap[from][to] = 1;
}

void SetGraph::AddEdge(int from, int to) {
    assert(0 <= from && from < adjMap.size());
    assert(0 <= to && to < adjMap.size());
    adjMap[from][to] = 1;
}

int SetGraph::VerticesCount() const {
    return (int)adjMap.size();
}

vector<int> SetGraph::GetNextVertices(int vertex) const {
    assert(0 <= vertex && vertex < adjMap.size());
    vector<int> nextVertices;

    for (pair<int, int> to_pair : adjMap[vertex])
        if (to_pair.second)
            nextVertices.push_back(to_pair.first);

    return nextVertices;
}

vector<int> SetGraph::GetPrevVertices(int vertex) const {
    assert(0 <= vertex && vertex < adjMap.size());
    vector<int> prevVertices;

    for (size_t from = 0; from < adjMap.size(); ++from)
        if (adjMap[from].find(vertex)->second)
            prevVertices.push_back(from);

    return prevVertices;
}
