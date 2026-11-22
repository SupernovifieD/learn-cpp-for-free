// undefined-behavior: the view outlives the string it refers to
#include <iostream>
#include <string>
#include <string_view>

int main()
{
    std::string_view note;
    {
        std::string text{"A reminder that is long enough to need the heap"};
        note = text;
    }
    std::cout << note << "\n";
    return 0;
}
