#include <iostream>

int main()
{
    std::cout << "5: " << sizeof(5) << "\n";
    std::cout << "5u: " << sizeof(5u) << "\n";
    std::cout << "5LL: " << sizeof(5LL) << "\n";
    std::cout << "5.0f: " << sizeof(5.0f) << "\n";
    std::cout << "5.0: " << sizeof(5.0) << "\n";
    std::cout << "'a': " << sizeof('a') << "\n";
    std::cout << "\"hello\": " << sizeof("hello") << "\n";
    std::cout << "true: " << sizeof(true) << "\n";
    return 0;
}
