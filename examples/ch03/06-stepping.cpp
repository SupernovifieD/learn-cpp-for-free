#include <iostream>

int doubleIt(int value)
{
    return value * 2;
}

int addBonus(int points, int bonus)
{
    int boosted{doubleIt(bonus)};
    return points + boosted;
}

int main()
{
    int score{40};
    int result{addBonus(score, 3)};
    std::cout << "Result: " << result << "\n";
    return 0;
}
