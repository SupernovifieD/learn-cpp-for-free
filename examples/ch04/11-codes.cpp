#include <iostream>

int main()
{
    char letter{'A'};
    int code{letter};
    int nextCode{letter + 1};

    std::cout << "Letter: " << letter << "\n";
    std::cout << "Code: " << code << "\n";
    std::cout << "Code plus one: " << nextCode << "\n";
    std::cout << "Letter plus one: " << letter + 1 << "\n";
    return 0;
}
