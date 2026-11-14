#include <iostream>

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
    // Fixed values for now: the calculations come first, then the input.
    int length{5};
    int width{4};

    std::cout << "Floor area: " << floorArea(length, width)
              << " square meters\n";
    std::cout << "Skirting board: " << skirtingLength(length, width)
              << " meters\n";
    return 0;
}
