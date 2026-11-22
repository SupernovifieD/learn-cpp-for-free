#include <iostream>

int main()
{
    int weightKg{12};

    if (weightKg > 20)
    {
        std::cout << "Freight\n";
    }
    else if (weightKg > 10)
    {
        std::cout << "Parcel\n";
    }
    else if (weightKg > 2)
    {
        std::cout << "Small parcel\n";
    }
    else
    {
        std::cout << "Letter\n";
    }
    return 0;
}
