#include <iostream>
#include <fstream>
#include <algorithm>
#include <vector>

int convert_to_points(char el)
{
  int sum = 0;
  if (el > 96 && el < 123)
  {
    sum += el - 96;
  }
  else if (el > 64 && el < 91)
  {
    sum += el - 38;
  }
  return sum;
}

char first_problem(std::string rucksack)
{
  int mid_point = rucksack.size()/2;
  std::vector<char> left(rucksack.begin(), rucksack.begin()+mid_point);
  std::vector<char> right(rucksack.begin()+mid_point, rucksack.end());
  std::sort(left.begin(), left.end());
  std::sort(right.begin(), right.end());
  std::vector<char> intersection;

  std::set_intersection(left.begin(), left.end(), right.begin(), right.end(), std::back_inserter(intersection));
  auto el = *intersection.begin();
  return el;
}

auto second_problem(std::string one, std::string two, std::string three)
{
  std::vector<char> first(one.begin(), one.end());
  std::vector<char> second(two.begin(), two.end());
  std::vector<char> third(three.begin(), three.end());
  std::sort(first.begin(), first.end());
  std::sort(second.begin(), second.end());
  std::sort(third.begin(), third.end());
  std::vector<char> intersection;
  std::vector<char> inter;
  std::set_intersection(first.begin(), first.end(), second.begin(), second.end(), std::back_inserter(intersection));

  std::set_intersection(intersection.begin(), intersection.end(), third.begin(), third.end(), std::back_inserter(inter));
  
  char res = ' ';
  if (inter.size() > 0)
    res = *inter.begin();

  return res;
}

int main()
{
  std::ifstream file("input.txt");
  std::string rucksack;
  std::string rucksack2;
  std::string rucksack3;

  int first_sum = 0;
  int second_sum = 0;

  while(std::getline(file, rucksack) &&
      std::getline(file, rucksack2) &&
      std::getline(file, rucksack3))
  {
    auto el = first_problem(rucksack);
    first_sum += convert_to_points(el);
    el = first_problem(rucksack2);
    first_sum += convert_to_points(el);
    el = first_problem(rucksack3);
    first_sum += convert_to_points(el);
    
    std::vector<std::string> rucksacks{rucksack, rucksack2, rucksack3};
    el = second_problem(rucksack, rucksack2, rucksack3);
    second_sum += convert_to_points(el);
  }

  std::cout<<"Sum: "<<first_sum<<std::endl;
  std::cout<<"Second Sum: "<<second_sum<<std::endl;
  return 0;
}