// undefined-behavior: the string moves its characters while a view uses them
#include <iostream>
#include <string>
#include <string_view>

int main()
{
    std::string text{"first text, long enough to need its own memory"};
    std::string_view view{text};
    text = "a second text that is much longer than the first one, for sure";
    std::cout << view << "\n";
    return 0;
}
