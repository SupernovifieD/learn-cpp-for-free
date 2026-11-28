// undefined-behavior: divides an integer by a zero value read at run time
#include <iostream>

int main()
{
    int divisor{};
    std::cin >> divisor;

    int result{24 / divisor};
    std::cout << result << "\n";
    return 0;
}
