#include <iostream>

int main()
{
    std::cout << "Enter a letter: ";
    char letter{};
    std::cin >> letter;

    char next{static_cast<char>(letter + 1)};
    std::cout << "Code: " << static_cast<int>(letter) << "\n";
    std::cout << "Next letter: " << next << "\n";
    return 0;
}
