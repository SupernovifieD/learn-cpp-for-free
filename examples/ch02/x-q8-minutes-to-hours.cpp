#include <iostream>

int hoursPart(int totalMinutes)
{
    return totalMinutes / 60;
}

int minutesPart(int totalMinutes)
{
    return totalMinutes - hoursPart(totalMinutes) * 60;
}

int main()
{
    int totalMinutes{};
    std::cout << "Minutes: ";
    std::cin >> totalMinutes;

    std::cout << hoursPart(totalMinutes) << " hours and "
              << minutesPart(totalMinutes) << " minutes\n";
    return 0;
}
