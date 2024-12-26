#include "listgraph.h"

ListGraph::ListGraph(const IGraph& graph) {
    for (int i = 0; i < graph.VerticesCount(); ++i)
        adjacencyLists[i] = graph.GetNextVertices(i);
}

void ListGraph::AddEdge(int from, int to) {
    assert(0 <= from && from < adjacencyLists.size());
    assert(0 <= to && to < adjacencyLists.size());
    adjacencyLists[from].push_back(to);
}

int ListGraph::VerticesCount() const {
    return (int)adjacencyLists.size();
}

vector<int> ListGraph::GetNextVertices(int vertex) const {
    assert(0 <= vertex && vertex < adjacencyLists.size());
    return adjacencyLists[vertex];
}

vector<int> ListGraph::GetPrevVertices(int vertex) const {
    assert(0 <= vertex && vertex < adjacencyLists.size());
    vector<int> prevVertices;

    for (int from = 0; from < adjacencyLists.size(); ++from)
        for (int to: adjacencyLists[from])
            if (to == vertex)
                prevVertices.push_back(from);

    return prevVertices;
}
