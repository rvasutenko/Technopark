#include "main.h"

void BFS(const IGraph& graph, int vertex, vector<bool>& visited, const function<void(int)>& func) {
    queue<int> qu;
    qu.push(vertex);
    visited[vertex] = true;

    while (!qu.empty()) {
        int currentVertex = qu.front();
        qu.pop();

        func(currentVertex);

        for (int nextVertex: graph.GetNextVertices(currentVertex)) {
            if (!visited[nextVertex]) {
                visited[nextVertex] = true;
                qu.push(nextVertex);
            }
        }
    }
}

void mainBFS(const IGraph& graph, const function<void(int)>& func) {
    vector<bool> visited(graph.VerticesCount(), false);

    for (int i = 0; i < graph.VerticesCount(); ++i)
        if (!visited[i])
            BFS(graph, i, visited, func);
}

void DFS(const IGraph& graph, int vertex, vector<bool>& visited, const function<void(int)>& func) {
    visited[vertex] = true;
    func(vertex);

    for (int nextVertex: graph.GetNextVertices(vertex))
        if (!visited[nextVertex])
            DFS(graph, nextVertex, visited, func);
}

void mainDFS(const IGraph& graph, const function<void(int)>& func) {
    vector<bool> visited(graph.VerticesCount(), false);

    for (int i = 0; i < graph.VerticesCount(); ++i)
        if (!visited[i])
            DFS(graph, i, visited, func);
}

void topologicalSortInternal(const IGraph& graph, int vertex, vector<bool>& visited, deque<int>& sorted) {
    visited[vertex] = true;

    for (int nextVertex: graph.GetNextVertices(vertex))
        if (!visited[nextVertex])
            topologicalSortInternal(graph, nextVertex, visited, sorted);

    sorted.push_front(vertex);
}

deque<int> topologicalSort(const IGraph& graph) {
    deque<int> sorted;
    vector<bool> visited(graph.VerticesCount(), false);

    for (int i = 0; i < graph.VerticesCount(); ++i)
        if (!visited[i])
            topologicalSortInternal(graph, i, visited, sorted);

    return sorted;
}

int main() {
    ListGraph listGraph(7);
    listGraph.AddEdge(0, 1);
    listGraph.AddEdge(0, 5);
    listGraph.AddEdge(1, 2);
    listGraph.AddEdge(1, 3);
    listGraph.AddEdge(1, 5);
    listGraph.AddEdge(1, 6);
    listGraph.AddEdge(3, 2);
    listGraph.AddEdge(3, 4);
    listGraph.AddEdge(3, 6);
    listGraph.AddEdge(5, 4);
    listGraph.AddEdge(5, 6);
    listGraph.AddEdge(6, 4);

    mainBFS(listGraph, [](int vertex){ cout << vertex << " "; });
    cout << endl;
    mainDFS(listGraph, [](int vertex){ cout << vertex << " "; });
    cout << endl;
    for (int vertex: topologicalSort(listGraph))
        cout << vertex << " ";

    cout << endl;
    cout << endl;

    MatrixGraph matrixGraph(listGraph);
    mainBFS(matrixGraph, [](int vertex){ cout << vertex << " "; });
    cout << endl;
    mainDFS(matrixGraph, [](int vertex){ cout << vertex << " "; });
    cout << endl;
    for (int vertex: topologicalSort(matrixGraph))
        cout << vertex << " ";

    cout << endl;
    cout << endl;

    ArcGraph arcGraph(matrixGraph);
    mainBFS(arcGraph, [](int vertex){ cout << vertex << " "; });
    cout << endl;
    mainDFS(arcGraph, [](int vertex){ cout << vertex << " "; });
    cout << endl;
    for (int vertex: topologicalSort(arcGraph))
        cout << vertex << " ";

    cout << endl;
    cout << endl;

    SetGraph setGraph(arcGraph);
    mainBFS(setGraph, [](int vertex){ cout << vertex << " "; });
    cout << endl;
    mainDFS(setGraph, [](int vertex){ cout << vertex << " "; });
    cout << endl;
    for (int vertex: topologicalSort(setGraph))
        cout << vertex << " ";

    return 0;
}
