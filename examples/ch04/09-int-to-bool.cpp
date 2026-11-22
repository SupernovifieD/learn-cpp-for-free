#include <iostream>

int main()
{
    int cartItems{3};
    int returns{0};
    bool hasItems{false};
    bool hasReturns{true};

    hasItems = cartItems;
    hasReturns = returns;

    std::cout << std::boolalpha;
    std::cout << "Has items: " << hasItems << "\n";
    std::cout << "Has returns: " << hasReturns << "\n";
    return 0;
}
