#include "listgraph.h"
#include "kruskalmst.h"
#include <iostream>
#include <vector>
#include <cmath>
#include <random>

using namespace std;

vector<pair<double, double>> GeneratePoints(int n) {
    random_device rd;
    mt19937 gen(rd());
    normal_distribution<> dist(1);

    vector<pair<double, double>> points(n);
    for (int i = 0; i < n; ++i)
        points[i] = {dist(gen), dist(gen)};
    return points;
}

double Distance(const pair<double, double>& a, const pair<double, double>& b) {
    return sqrt((a.first - b.first) * (a.first - b.first) + (a.second - b.second) * (a.second - b.second));
}

ListGraph CreateGraph(const vector<pair<double, double>>& points) {
    int n = points.size();
    ListGraph graph(n);
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            double dist = Distance(points[i], points[j]);
            graph.AddEdge(i, j, dist);
        }
    }
    return graph;
}

int main() {
    for (int n = 2; n <= 10; ++n) {
        vector<double> approximations;

        for (int trial = 0; trial < 100; ++trial) {
            vector<pair<double, double>> points = GeneratePoints(n);
            ListGraph graph = CreateGraph(points);

            vector<tuple<int, int, double>> edges = graph.GetEdges();
            double mstWeight = KruskalMST::FindMSTWeight(edges, graph.VerticesCount());

            double tspEstimate = 2 * mstWeight;
            approximations.push_back(tspEstimate);
        }

        double mean = 0, sqSum = 0;
        for (double value : approximations) {
            mean += value;
            sqSum += value * value;
        }
        mean /= approximations.size();
        double variance = sqSum / approximations.size() - mean * mean;
        double stddev = sqrt(variance);

        cout << "N = " << n << ", Mean: " << mean << ", Stddev: " << stddev << endl;
    }

    return 0;
}
