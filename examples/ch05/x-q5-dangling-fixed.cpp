#include <iostream>
#include <string>

int main()
{
    std::string note;
    {
        std::string text{"A reminder that is long enough to need the heap"};
        note = text;
    }
    std::cout << note << "\n";
    return 0;
}
