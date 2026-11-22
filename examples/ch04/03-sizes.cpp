#include <iostream>

int main()
{
    int count{7};

    std::cout << "char: " << sizeof(char) << "\n";
    std::cout << "short: " << sizeof(short) << "\n";
    std::cout << "int: " << sizeof(int) << "\n";
    std::cout << "long long: " << sizeof(long long) << "\n";
    std::cout << "float: " << sizeof(float) << "\n";
    std::cout << "double: " << sizeof(double) << "\n";
    std::cout << "bool: " << sizeof(bool) << "\n";
    std::cout << "count: " << sizeof(count) << "\n";
    return 0;
}
