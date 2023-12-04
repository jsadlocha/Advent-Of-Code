#pragma once
#include <ntifs.h>
#include <ntstrsafe.h>
#include <wdm.h>

struct Advent_Solution
{
	UINT32 solution1;
	UINT32 solution2;
};

typedef Advent_Solution* PAdvent_Solution;

void Main(PUNICODE_STRING usPath, PAdvent_Solution Advent);
