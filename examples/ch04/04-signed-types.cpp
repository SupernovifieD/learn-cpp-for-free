#include <iostream>

int main()
{
    short minutesEarly{-15};
    int balance{-2500};
    long long distance{9000000000};

    std::cout << "Minutes early: " << minutesEarly << "\n";
    std::cout << "Balance: " << balance << "\n";
    std::cout << "Distance: " << distance << "\n";
    std::cout << "Twice the distance: " << distance * 2 << "\n";
    std::cout << "7 / 2 is " << 7 / 2 << "\n";
    std::cout << "-7 / 2 is " << -7 / 2 << "\n";
    return 0;
}
