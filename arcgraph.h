#ifndef ARCGRAPH_H
#define ARCGRAPH_H

#include "igraph.h"

using namespace std;

class ArcGraph : public IGraph {
public:
    ArcGraph(size_t _size) : verticesCount(_size) {}
    ArcGraph(const IGraph& graph);
    ~ArcGraph() {}

    void AddEdge(int from, int to) override;
    int VerticesCount() const override;

    vector<int> GetNextVertices(int vertex) const override;
    vector<int> GetPrevVertices(int vertex) const override;
private:
    size_t verticesCount;
    vector<pair<int, int>> arcVector;
};

#endif // ARCGRAPH_H
