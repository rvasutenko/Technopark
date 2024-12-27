#ifndef KRUSKALMST_H
#define KRUSKALMST_H

#include <vector>
#include <tuple>

class KruskalMST {
public:
    static double FindMSTWeight(const std::vector<std::tuple<int, int, double>>& edges, int verticesCount);
};

#endif // KRUSKALMST_H
