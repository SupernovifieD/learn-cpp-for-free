// expect-fail: a std::string_view does not convert to a std::string by itself
#include <iostream>
#include <string>
#include <string_view>

int main()
{
    std::string_view view{"hello"};
    std::string copy = view;
    std::cout << copy << "\n";
    return 0;
}
