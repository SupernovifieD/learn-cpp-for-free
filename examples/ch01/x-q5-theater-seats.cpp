#include <iostream>

int main()
{
    int rows{8};
    int seatsPerRow{12};
    int seats{rows * seatsPerRow};

    std::cout << "The theater has " << seats << " seats.\n";
    return 0;
}
