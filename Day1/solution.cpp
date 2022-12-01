#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <exception>

int main() {
  std::ifstream file("input.txt");
  std::vector<int> caloriesArray;
  std::string line;
  int calories = 0;
  caloriesArray.reserve(100);

  if (file.is_open())
  {
    while(std::getline(file, line))
    {
      if(line.empty())
      {
        caloriesArray.push_back(calories);
        calories = 0;
        continue;
      }
      try {
        calories += std::stoi(line);
      } 
      catch (const std::exception &e){
        std::cerr<<"Exception error in: "<<e.what()<<std::endl<<"exiting program!"<<std::endl;
        std::exit(EXIT_FAILURE);  
      }
    }
    if (calories > 0)
      caloriesArray.push_back(calories);

    std::sort(begin(caloriesArray), end(caloriesArray), [](int a, int b){
      return a > b;
    });
    
    calories = 0;
    for (auto i = 0; i < 3; ++i)
    {
      calories += caloriesArray[i];
      if (i == 0)
      {
        std::cout<<"Max calories: "<<calories<<std::endl;
      }
    }
    std::cout<<"Sum of best three: "<<calories<<std::endl;
  }
  else
  {
    std::cout<<"Failed to open file!"<<std::endl;
  }

  return 0;
}

// g++ -std=c++17 -Wall -Wextra -Wpedantic solution.cpp -o solution.o