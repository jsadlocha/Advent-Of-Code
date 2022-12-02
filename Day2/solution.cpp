#include <iostream>
#include <fstream>
#include <map>

void strategy()
{
  std::map<char, int> players = {{'X', 1},{'Y', 2},{'Z', 3},{'A', 1},{'B', 2},{'C', 3}};
  std::map<int, int> lose = {{1, 2}, {2, 3}, {3, 1}};
  std::map<int, int> win = {{1, 3}, {2, 1}, {3, 2}};

  std::ifstream file("input.txt");

  int total_score1 = 0;
  int total_score2 = 0;
  char player_move = 0;
  char enemy_move = 0;

  auto strategy1 = [](int e, int p) -> int {
    if (p == e) // draw
      return 3+p; 
    
    if ((p - e == -2) || (p - e == 1)) // win
      return 6+p; 

    if ((p - e == 2) || (p - e == -1)) // lose
      return p; 
    
    return 0;
  };

  auto strategy2 = [&lose, &win](int e, int p) -> int {
    if (p == 1) //lose
      return win[e];
    
    if (p == 2) //remis
      return e+3;

    if (p == 3) //win
      return lose[e]+6;

    return 0;
  };
  
  while(file >> enemy_move && file>>player_move)
  {
    total_score1 += strategy1(players[enemy_move], players[player_move]);
    total_score2 += strategy2(players[enemy_move], players[player_move]);
  }
  
  std::cout<<"Strategy1: "<<total_score1<<std::endl;
  std::cout<<"Strategy2: "<<total_score2<<std::endl;
}

int main()
{
  strategy();

  return 0;
}