#include <iostream>
#include <vector>
#include <string>

//using namespace std;

int main() 
{
    std::vector<std::string> msg {"hello", "c++", "world", "from", "VS code", "and the c++ extension"};
    int slices = 5;
    slices = slices + 5;
    std::cout << slices << "\n" ;
    for (const std::string& word : msg){
        std::cout << word  << " ";
    }
    std::cout << std::endl;
}  
