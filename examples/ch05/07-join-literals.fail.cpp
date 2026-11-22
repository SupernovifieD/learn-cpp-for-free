// expect-fail: two string literals cannot be joined with +
#include <iostream>
#include <string>

int main()
{
    std::string greeting{"Hello, " + "world"};
    std::cout << greeting << "\n";
    return 0;
}
