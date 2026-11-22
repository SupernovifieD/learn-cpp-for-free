#include <bitset>
#include <iostream>

int main()
{
    int number{77};

    std::cout << "Decimal: " << number << "\n";
    std::cout << std::hex << "Hexadecimal: " << number << "\n";
    std::cout << std::oct << "Octal: " << number << "\n";
    std::cout << "Binary: " << std::bitset<8>{77} << "\n";
    return 0;
}
