#include <iostream>
#include <string_view>

int main()
{
    using namespace std::string_view_literals;

    constexpr std::string_view appName{"Trip planner"};
    constexpr std::string_view motto{"pack light"sv};

    std::cout << appName << " has " << appName.length() << " characters\n";
    std::cout << "Motto: " << motto << "\n";
    return 0;
}
