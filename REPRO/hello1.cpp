// clang-format off
// for /L %I in (1,1,5) do cl /Bt+ /EHsc /nologo /W4 /std:c++latest /Zc:preprocessor /MD /Od /D_SILENCE_ALL_CXX17_DEPRECATION_WARNINGS hello1.cpp
// clang-format on
#include <iostream>
using namespace std;

int main() {
    cout << "Hello, world!" << endl;
}
