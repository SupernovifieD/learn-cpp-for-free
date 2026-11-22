#include <iostream>
#include <string>
#include <string_view>

int main()
{
    std::string line{"[note] remember the milk;"};
    std::string_view view{line};

    view.remove_prefix(7);
    view.remove_suffix(1);

    std::cout << "View: " << view << "\n";
    std::cout << "String: " << line << "\n";
    std::cout << "Lengths: " << view.length() << " " << line.length() << "\n";
    return 0;
}
