#include <iostream>

int readNumber()
{
    int value{};
    std::cin >> value;
    return value;
}

int floorArea(int length, int width)
{
    return length * width;
}

int skirtingLength(int length, int width)
{
    return 2 * (length + width);
}

int main()
{
    std::cout << "Length of the room in meters: ";
    int length{readNumber()};

    std::cout << "Width of the room in meters: ";
    int width{readNumber()};

    std::cout << "Floor area: " << floorArea(length, width)
              << " square meters\n";
    std::cout << "Skirting board: " << skirtingLength(length, width)
              << " meters\n";
    return 0;
}
