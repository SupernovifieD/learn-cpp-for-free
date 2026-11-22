#include <iostream>

int main()
{
    int total{7};
    int count{2};
    double average{static_cast<double>(total) / count};
    std::cout << "Average: " << average << "\n";
    return 0;
}
