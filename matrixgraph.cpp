#include "matrixgraph.h"

MatrixGraph::MatrixGraph(const IGraph& graph) : adjMatrix(graph.VerticesCount(), vector<int>(graph.VerticesCount(), 0)) {
    for (int from = 0; from < graph.VerticesCount(); ++from)
        for (int to : graph.GetNextVertices(from))
            adjMatrix[from][to] = 1;
}

void MatrixGraph::AddEdge(int from, int to) {
    assert(0 <= from && from < adjMatrix.size());
    assert(0 <= to && to < adjMatrix.size());
    adjMatrix[from][to] = 1;
}

int MatrixGraph::VerticesCount() const {
    return (int)adjMatrix.size();
}

vector<int> MatrixGraph::GetNextVertices(int vertex) const {
    assert(0 <= vertex && vertex < adjMatrix.size());
    vector<int> nextVertices;

    for (int to = 0; to < adjMatrix.size(); ++to)
        if (adjMatrix[vertex][to])
            nextVertices.push_back(to);

    return nextVertices;
}

vector<int> MatrixGraph::GetPrevVertices(int vertex) const {
    assert(0 <= vertex && vertex < adjMatrix.size());
    vector<int> prevVertices;

    for (int from = 0; from < adjMatrix.size(); ++from)
        if (adjMatrix[from][vertex])
            prevVertices.push_back(from);

    return prevVertices;
}
