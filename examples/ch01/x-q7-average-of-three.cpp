#include <iostream>

int main()
{
    int first{};
    int second{};
    int third{};

    std::cout << "Enter three numbers: ";
    std::cin >> first >> second >> third;

    int average{(first + second + third) / 3};
    std::cout << "Average (rounded down): " << average << "\n";
    return 0;
}
