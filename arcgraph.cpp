#include "arcgraph.h"

ArcGraph::ArcGraph(const IGraph& graph) : verticesCount(graph.VerticesCount()) {
    for (int from = 0; from < graph.VerticesCount(); ++from)
        for (int to : graph.GetNextVertices(from))
            arcVector.push_back(pair<int, int>(from, to));
}

void ArcGraph::AddEdge(int from, int to) {
    assert(0 <= from && from < verticesCount);
    assert(0 <= to && to < verticesCount);
    arcVector.push_back(pair<int, int>(from, to));
}

int ArcGraph::VerticesCount() const {
    return (int)verticesCount;
}

vector<int> ArcGraph::GetNextVertices(int vertex) const {
    assert(0 <= vertex && vertex < verticesCount);
    vector<int> nextVertices;

    for (pair<int, int> edge : arcVector)
        if (edge.first == vertex)
            nextVertices.push_back(edge.second);

    return nextVertices;
}

vector<int> ArcGraph::GetPrevVertices(int vertex) const {
    assert(0 <= vertex && vertex < verticesCount);
    vector<int> prevVertices;

    for (pair<int, int> edge : arcVector)
        if (edge.second == vertex)
            prevVertices.push_back(edge.first);

    return prevVertices;
}
