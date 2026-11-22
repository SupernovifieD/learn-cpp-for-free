// expect-fail: a const variable that is set from input is not a constant
// expression
#include <bitset>
#include <cstddef>
#include <iostream>

int main()
{
    std::size_t typed{};
    std::cin >> typed;
    const std::size_t bits{typed};
    std::bitset<bits> row{};
    std::cout << row << "\n";
    return 0;
}
