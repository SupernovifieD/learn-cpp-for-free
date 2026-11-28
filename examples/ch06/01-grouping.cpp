#include <iostream>

int main()
{
    constexpr int a{2};
    constexpr int b{3};
    constexpr int c{4};

    std::cout << "a + b * c: " << a + b * c << "\n";
    std::cout << "a + (b * c): " << a + (b * c) << "\n";
    std::cout << "(a + b) * c: " << (a + b) * c << "\n";

    constexpr int first{20};
    constexpr int second{6};
    constexpr int third{2};
    std::cout << "first - second - third: " << first - second - third << "\n";
    std::cout << "first - (second - third): " << first - (second - third)
              << "\n";

    int x{9};
    int y{8};
    x = y = 0;
    std::cout << "x and y: " << x << " " << y << "\n";
    return 0;
}
