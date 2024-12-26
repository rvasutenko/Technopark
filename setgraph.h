#ifndef SETGRAPH_H
#define SETGRAPH_H

#include "igraph.h"

class SetGraph : public IGraph {
public:
    SetGraph(size_t size) : adjMap(size) {}
    SetGraph(const IGraph& graph);
    ~SetGraph() {}

    void AddEdge(int from, int to) override;
    int VerticesCount() const override;

    vector<int> GetNextVertices(int vertex) const override;
    vector<int> GetPrevVertices(int vertex) const override;

private:
    vector<unordered_map<int, int>> adjMap;
};

#endif // SETGRAPH_H
