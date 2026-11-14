// comments.cpp
// Prints a short note. The compiler ignores everything after // on a line.

#include <iostream>

/* A block comment can span
   several lines. */
int main()
{
    std::cout << "Dear reader,\n"; // this comment follows a statement
    // std::cout << "This line is switched off.\n";
    std::cout << "see you in the next lesson.\n";
    return 0;
}
