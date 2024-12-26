#ifndef IGRAPH_H
#define IGRAPH_H

#include <iostream>

using namespace std;

struct IGraph {
    virtual ~IGraph() {}

    virtual void AddEdge(int from, int to) = 0;
    virtual int VerticesCount() const = 0;

    virtual vector<int> GetNextVertices(int vertex) const = 0;
    virtual vector<int> GetPrevVertices(int vertex) const = 0;
};

#endif // IGRAPH_H
