// expect-fail: a const double cannot be used in a constant expression
#include <bitset>
#include <cstddef>
#include <iostream>

int main()
{
    const double width{8.0};
    std::bitset<static_cast<std::size_t>(width)> row{5};
    std::cout << row << "\n";
    return 0;
}
