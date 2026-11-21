#include <iostream>

int addPoints(int current, int bonus)
{
    return current + bonus;
}

int main()
{
    int score{40};
    score = addPoints(score, 2);
    std::cout << "score " << score << "\n";
    return 0;
}
