#include <iostream>

int main()
{
    int width{6};
    int height{4};

    int area{width * height};
    int perimeter{2 * (width + height)};

    std::cout << "area: " << area << "\n";
    std::cout << "perimeter: " << perimeter << "\n";
    std::cout << "half the area: " << area / 2 << "\n";

    width = width + 1;
    std::cout << "area after widening: " << width * height << "\n";
    return 0;
}
