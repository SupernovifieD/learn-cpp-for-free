// expect-fail: a function parameter cannot be constexpr
#include <iostream>

void showFee(constexpr int fee)
{
    std::cout << fee << "\n";
}

int main()
{
    showFee(25);
    return 0;
}
