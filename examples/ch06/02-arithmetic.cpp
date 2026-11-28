#include <iostream>

int main()
{
    int balance{12};
    std::cout << "Unary plus: " << +balance << "\n";
    std::cout << "Unary minus: " << -balance << "\n";
    std::cout << "Sum: " << balance + 3 << "\n";
    std::cout << "Difference: " << balance - 3 << "\n";
    std::cout << "Product: " << balance * 3 << "\n";
    std::cout << "Quotient: " << balance / 3 << "\n";

    int points{10};
    points += 5;
    std::cout << "After += 5: " << points << "\n";
    points *= 2;
    std::cout << "After *= 2: " << points << "\n";
    points -= 6;
    std::cout << "After -= 6: " << points << "\n";
    points /= 4;
    std::cout << "After /= 4: " << points << "\n";
    return 0;
}
