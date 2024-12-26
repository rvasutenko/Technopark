#ifndef MATRIXGRAPH_H
#define MATRIXGRAPH_H

#include "igraph.h"

using namespace std;

class MatrixGraph : public IGraph {
public:
    MatrixGraph(size_t size) : adjMatrix(size, vector<int>(size, 0)) {}
    MatrixGraph(const IGraph& graph);
    ~MatrixGraph() {}

    void AddEdge(int from, int to) override;
    int VerticesCount() const override;

    vector<int> GetNextVertices(int vertex) const override;
    vector<int> GetPrevVertices(int vertex) const override;
private:
    vector<vector<int>> adjMatrix;
};

#endif // MATRIXGRAPH_H
