// Plan:
// 1. Ask for a number of hours.
// 2. Read the number.
// 3. Calculate the minutes and the seconds.
// 4. Print the results.

#include <iostream>

int main()
{
    int hours{};
    std::cout << "How many hours? ";
    std::cin >> hours;

    int minutes{hours * 60};
    int seconds{minutes * 60};

    std::cout << hours << " hours are " << minutes << " minutes and " << seconds
              << " seconds.\n";
    return 0;
}
