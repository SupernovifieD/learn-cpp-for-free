#include <iostream>

void addBonus(int points)
{
    points = points + 10;
    std::cout << "inside addBonus: " << points << "\n";
}

int main()
{
    int score{50};
    addBonus(score);
    std::cout << "back in main: " << score << "\n";
    return 0;
}
