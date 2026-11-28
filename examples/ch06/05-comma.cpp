#include <iostream>

int main()
{
    int left{2};
    int right{5};

    int result{(left += 3, right *= 2)};
    std::cout << "left = " << left << "\n";
    std::cout << "right = " << right << "\n";
    std::cout << "result = " << result << "\n";
    return 0;
}
