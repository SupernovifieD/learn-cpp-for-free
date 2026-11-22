#include <iostream>

int ticketPrice(int age)
{
    if (age < 13)
    {
        return 5;
    }
    if (age < 65)
    {
        return 12;
    }
    return 8;
}

int main()
{
    std::cout << "Age 10: " << ticketPrice(10) << "\n";
    std::cout << "Age 30: " << ticketPrice(30) << "\n";
    std::cout << "Age 70: " << ticketPrice(70) << "\n";
    return 0;
}
