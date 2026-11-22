// expect-fail: one bitset size is a const variable that is set at run time
#include <bitset>
#include <cstddef>
#include <iostream>

int main()
{
    constexpr std::size_t rows{3};
    const std::size_t cells{rows * 4};

    std::size_t typed{5};
    const std::size_t copy{typed};

    std::bitset<cells> first{};
    std::bitset<copy> second{};
    std::cout << first << " " << second << "\n";
    return 0;
}
