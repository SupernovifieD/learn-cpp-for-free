// undefined-behavior: this claims to overflow, but it does not
#include <iostream>

int main()
{
    int number{};
    std::cin >> number;
    std::cout << number + 1 << "\n";
    return 0;
}
