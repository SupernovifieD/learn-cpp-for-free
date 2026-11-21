#include <iostream>

int boxVolume(int length, int width, int height)
{
    std::cerr << "[debug] boxVolume: length=" << length << " width=" << width
              << " height=" << height << "\n";
    return length * width * width;
}

int main()
{
    int volume{boxVolume(4, 3, 2)};
    std::cout << "Volume: " << volume << "\n";
    return 0;
}
