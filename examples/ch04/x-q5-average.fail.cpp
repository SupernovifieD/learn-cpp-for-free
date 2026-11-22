// expect-fail: a brace initializer does not accept an int division for a double
#include <iostream>

int main()
{
    int total{7};
    int count{2};
    double average{total / count};
    std::cout << "Average: " << average << "\n";
    return 0;
}
