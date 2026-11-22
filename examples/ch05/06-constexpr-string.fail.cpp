// expect-fail: a std::string cannot be a constexpr variable
#include <iostream>
#include <string>

int main()
{
    constexpr std::string name{"Noor"};
    std::cout << name << "\n";
    return 0;
}
