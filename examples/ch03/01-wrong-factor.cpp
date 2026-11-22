#include <iostream>

int toTimerSeconds(int minutes)
{
    return minutes * 6;
}

int main()
{
    int bakingTime{7};
    std::cout << bakingTime << " minutes are " << toTimerSeconds(bakingTime)
              << " seconds\n";
    return 0;
}
