#include <iostream>

int main()
{
    int left{3};
    int right{8};
    std::cout << "before: " << left << " " << right << "\n";

    int spare{left};
    left = right;
    right = spare;
    std::cout << "after: " << left << " " << right << "\n";
    return 0;
}
