// expect-fail: an unused variable is an error under -Werror
// passes-without: -Werror
int main()
{
    int unused{1};
    return 0;
}
