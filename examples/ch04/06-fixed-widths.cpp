#include <cstddef>
#include <cstdint>
#include <iostream>

int main()
{
    std::int16_t shelves{1200};
    std::int32_t visitors{2000000000};
    std::int64_t downloads{9000000000};
    std::size_t intSize{sizeof(int)};

    std::cout << "Shelves: " << shelves << "\n";
    std::cout << "Visitors: " << visitors << "\n";
    std::cout << "Downloads: " << downloads << "\n";
    std::cout << "int has " << intSize << " bytes\n";
    std::cout << "std::int16_t has " << sizeof(std::int16_t) << " bytes\n";
    std::cout << "std::int32_t has " << sizeof(std::int32_t) << " bytes\n";
    std::cout << "std::int64_t has " << sizeof(std::int64_t) << " bytes\n";
    std::cout << "std::size_t has " << sizeof(std::size_t) << " bytes\n";
    return 0;
}
