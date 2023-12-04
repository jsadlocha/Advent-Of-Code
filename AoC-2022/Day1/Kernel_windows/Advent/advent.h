#pragma once
#include <ntifs.h>
#include <ntddk.h>

extern "C" NTSTATUS DriverEntry(PDRIVER_OBJECT pDriverObject, PUNICODE_STRING pRegisterPath);

void DriverUnload(PDRIVER_OBJECT pDriverObject);
