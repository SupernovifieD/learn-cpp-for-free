#include <iostream>

int main()
{
    int binaryValue{0b1101};
    int hexValue{0x1F};
    int octalValue{017};
    int octalTrap{010};
    int million{1'000'000};
    int grouped{0b1101'0010};

    std::cout << "0b1101: " << binaryValue << "\n";
    std::cout << "0x1F: " << hexValue << "\n";
    std::cout << "017: " << octalValue << "\n";
    std::cout << "010: " << octalTrap << "\n";
    std::cout << "1'000'000: " << million << "\n";
    std::cout << "0b1101'0010: " << grouped << "\n";
    return 0;
}
