#include <bitset>
#include <iostream>

int main()
{
    int value{200};

    std::cout << "Decimal: " << value << "\n";
    std::cout << std::hex << "Hexadecimal: " << value << "\n";
    std::cout << std::oct << "Octal: " << value << "\n";
    std::cout << std::dec << "Decimal again: " << value << "\n";
    std::cout << "Binary: " << std::bitset<8>{200} << "\n";
    return 0;
}
