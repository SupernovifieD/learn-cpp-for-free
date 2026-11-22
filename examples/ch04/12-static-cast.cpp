#include <cstdint>
#include <iostream>

int main()
{
    double price{4.75};
    int whole{static_cast<int>(price)};
    std::cout << "Whole part: " << whole << "\n";

    int total{7};
    int groups{2};
    double average{static_cast<double>(total) / groups};
    std::cout << "Average: " << average << "\n";

    char letter{'A'};
    char next{static_cast<char>(letter + 1)};
    std::cout << "Next letter: " << next << "\n";
    std::cout << "Code of the letter: " << static_cast<int>(letter) << "\n";

    std::int8_t level{65};
    std::cout << "Level as a number: " << static_cast<int>(level) << "\n";
    return 0;
}
