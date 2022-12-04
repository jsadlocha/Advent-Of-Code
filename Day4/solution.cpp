#include <iostream>
#include <fstream>

struct Elf
{
public:
  int lower_bound;
  int upper_bound;

  Elf(std::string &&elf)
  {
    auto delim = elf.find('-');
    lower_bound = std::atoi(elf.substr(0, delim).c_str());
    upper_bound = std::atoi(elf.substr(delim+1, elf.size()).c_str());
  }
};

bool compareElfContainsItself(Elf e1, Elf e2)
{
  bool isContained = false;
  if(e1.lower_bound <= e2.lower_bound && e1.upper_bound >= e2.upper_bound)
    isContained = true;

  if(e2.lower_bound <= e1.lower_bound && e2.upper_bound >= e1.upper_bound)
    isContained = true;

  return isContained;
}

bool compareElfOverlaps(Elf e1, Elf e2)
{ 
  if (e2.upper_bound < e1.lower_bound || e1.upper_bound < e2.lower_bound)
    return false;

  return true;
}

int main()
{
  std::ifstream file("input.txt");
  std::string line;
  auto sum = 0;
  auto sum2 = 0;
  
  auto debug = 0;
  while(std::getline(file, line))
  {
    Elf elf1(line.substr(0, line.find(',')));
    Elf elf2(line.substr(line.find(',')+1, line.size()));
    auto contains = compareElfContainsItself(elf1, elf2);
    auto overlaps = compareElfOverlaps(elf1, elf2);
    if (contains)
      sum++;

    if (overlaps)
      sum2++;
  }

  std::cout<<"Sum: "<<sum<<std::endl;
  std::cout<<"Sum2: "<<sum2<<std::endl;

  return 0;
}