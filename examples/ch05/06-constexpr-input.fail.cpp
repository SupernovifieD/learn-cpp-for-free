// expect-fail: a constexpr variable cannot be set from a value read at run time
#include <iostream>

int main()
{
    int typed{};
    std::cin >> typed;
    constexpr int limit{typed};
    std::cout << limit << "\n";
    return 0;
}
