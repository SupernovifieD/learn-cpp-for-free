#include <iostream>
#include <string>

int main()
{
    using namespace std::string_literals;

    std::string greeting{"Hello, "s + "world"};
    std::cout << greeting << "\n";
    return 0;
}
