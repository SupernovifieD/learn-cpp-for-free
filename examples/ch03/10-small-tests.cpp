#include <iostream>

int boxVolume(int length, int width, int height)
{
    return length * width * height;
}

int main()
{
    std::cout << "boxVolume(4, 3, 2): expected 24, got " << boxVolume(4, 3, 2)
              << "\n";
    std::cout << "boxVolume(1, 1, 1): expected 1, got " << boxVolume(1, 1, 1)
              << "\n";
    std::cout << "boxVolume(5, 0, 9): expected 0, got " << boxVolume(5, 0, 9)
              << "\n";
    return 0;
}
