#ifndef LISTGRAPH_H
#define LISTGRAPH_H

#include "igraph.h"

class ListGraph : public IGraph {
public:
    ListGraph(size_t size) : adjacencyLists(size) {}
    ListGraph(const IGraph& graph);
    ~ListGraph() {}

    void AddEdge(int from, int to) override;
    int VerticesCount() const override;

    vector<int> GetNextVertices(int vertex) const override;
    vector<int> GetPrevVertices(int vertex) const override;
private:
    vector<vector<int>> adjacencyLists;
};

#endif // LISTGRAPH_H
