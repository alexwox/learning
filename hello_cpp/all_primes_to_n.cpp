#include <iostream>

bool isPrime (int number){
    bool result = true;
    
    for(int i = 2; i < number; i++){
        if ( number % i == 0){
            result = false;
        }
    }
    return result;
}

int main () {
    int number;
    
    std::cout << "Give me a positive number: ";
    std::cin >> number; 
    std::cout << "\n";

    if (number == 0 || number == 1){
        return 0;
    }

    else if (number == 2) { 
        std::cout << number;
        std::cout << "\n";  
        return 0;
    }

    for(int i = 3; i < number+1; i++){
        if (isPrime(i) == true){
            std::cout << i;
            std::cout << "\n";
        }
    }  
    return 0;
}