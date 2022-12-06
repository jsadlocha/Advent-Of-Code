#include <iostream>
#include <fstream>
#include <sstream>
#include <deque>
#include <set>

using namespace std;

void find_message(string& msg, int mark_len)
{
  deque<char> deq;
  set<char> cset;

  for(auto i = 0; i<mark_len; ++i)
    deq.push_back(msg[i]);
    
  for(auto i = mark_len; i < msg.size(); ++i)
  {
    for(auto i : deq)
      cset.insert(i);

    if(cset.size() == mark_len)
    {
      cout<<"Solution: "<<i<<endl;
      break;
    }
    cset.clear();
    deq.pop_front();
    deq.push_back(msg[i]);
  }
}

int main()
{
  ifstream file("input.txt");
  stringstream stream;
  stream << file.rdbuf();
  string message = stream.str();
  
  find_message(message, 4);
  find_message(message, 14);

  return 0;
}