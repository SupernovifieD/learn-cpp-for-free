// expect-fail: units.h is included twice, so its function is defined twice
#include "day.h"
#include "units.h"

#include <iostream>

int main()
{
    std::cout << "minutes per hour: " << minutesPerHour() << "\n";
    std::cout << "minutes per day: " << minutesPerDay() << "\n";
    return 0;
}
