#include <iostream>

int main()
{
    double plain{1200.0};
    double scientific{1.2e3};
    double grains{2.5e6};
    double cellLength{4e-6};
    double messages{7.9e9};
    double ordinary{123456.0};

    std::cout << "Plain: " << plain << "\n";
    std::cout << "Scientific: " << scientific << "\n";
    std::cout << "Grains: " << grains << "\n";
    std::cout << "Cell length: " << cellLength << "\n";
    std::cout << "Messages: " << messages << "\n";
    std::cout << "Ordinary: " << ordinary << "\n";
    return 0;
}
