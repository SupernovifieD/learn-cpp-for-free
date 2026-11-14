#include <iostream>

int main()
{
    int eggs{};
    std::cout << "How many eggs? ";
    std::cin >> eggs;

    int boxes{eggs / 12};
    int leftOver{eggs - boxes * 12};

    std::cout << "Full boxes: " << boxes << "\n";
    std::cout << "Left over: " << leftOver << "\n";
    return 0;
}
