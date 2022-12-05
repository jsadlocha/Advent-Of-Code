#include <iostream>
#include <fstream>
#include <stack>
#include <deque>
#include <stack>
#include <vector>
#include <sstream>

using namespace std;

struct Ops 
{
public:
  int m_reps;
  int m_from;
  int m_to;

  Ops(int reps, int from, int to) 
  {
    m_reps = reps;
    m_from = from;
    m_to = to;
  }
};

void parseStack(ifstream& file, vector<deque<char>>& dque)
{
  string line;
  char pos[] = {1,5,9,13,17,21,25,29,33};

  while(getline(file, line))
  {
    if(line.size() < 1)
      break;
    
    for (auto i=0; i<9; ++i)
    {
      if (line[pos[i]] == ' ')
        continue;
      
      dque[i].push_front(line[pos[i]]);
    }
  }
}

void parseOperations(ifstream& file, vector<Ops>& op)
{
  string trash;
  int reps, from, to;
  while(file>>trash>>reps>>trash>>from>>trash>>to)
  {
    op.push_back(Ops(reps, from, to));
  }
}

void executeOperations1(vector<deque<char>>& dque, vector<Ops>& op)
{
  for(auto &o : op)
  {
    for(auto i=0; i<o.m_reps; ++i)
    {
      dque[o.m_to-1].push_back(dque[o.m_from-1].back());
      dque[o.m_from-1].pop_back();
    }
  }
}

void executeOperations2(vector<deque<char>>& dque, vector<Ops>& op)
{
  stack<char> tmp;
  for(auto &o : op)
  {
    for(auto i=0; i<o.m_reps; ++i)
    {
      tmp.push(dque[o.m_from-1].back());
      dque[o.m_from-1].pop_back();
    }
    for(auto i=0; i<o.m_reps; ++i)
    {
      dque[o.m_to-1].push_back(tmp.top());
      tmp.pop();
    }
  }
}

void printSolution(vector<deque<char>>& dque)
{
  cout<<"Solution: ";
  for(auto &v : dque)
  {
    cout<<v.back();
  }
  cout<<endl;
}

int main()
{
  ifstream file("input.txt");
  vector<Ops> op;
  vector<deque<char>> dque;
  vector<deque<char>> dque2;
  dque.resize(9);

  parseStack(file, dque);
  dque2 = dque;

  parseOperations(file, op);

  executeOperations1(dque, op);
  executeOperations2(dque2, op);

  printSolution(dque);
  printSolution(dque2);

  return 0;
}