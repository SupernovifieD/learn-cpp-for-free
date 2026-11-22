#include <cstdint>
#include <iostream>

int main()
{
    std::int8_t level{65};
    std::uint8_t spare{66};

    std::cout << "Level: " << level << "\n";
    std::cout << "Spare: " << spare << "\n";
    return 0;
}
