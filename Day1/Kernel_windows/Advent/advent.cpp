#include "advent.h"
#include "ioctl.h"
#include "solution.h"

PDEVICE_OBJECT pDeviceObject;
UNICODE_STRING dev, dos;


NTSTATUS DriverEntry(PDRIVER_OBJECT pDriverObject, PUNICODE_STRING pRegistryPath)
{
	UNREFERENCED_PARAMETER(pDriverObject);
	UNREFERENCED_PARAMETER(pRegistryPath);
	pDriverObject->DriverUnload = DriverUnload;
	DbgPrintEx(0, 0, "Driver loaded\n");

	RtlInitUnicodeString(&dev, L"\\Device\\Advent");
	RtlInitUnicodeString(&dos, L"\\DosDevices\\Advent");

	IoCreateDevice(pDriverObject, 0, &dev, FILE_DEVICE_UNKNOWN, FILE_DEVICE_SECURE_OPEN, false, &pDeviceObject);
	IoCreateSymbolicLink(&dos, &dev);

	pDriverObject->MajorFunction[IRP_MJ_CREATE] = CreateCall;
	pDriverObject->MajorFunction[IRP_MJ_CLOSE] = CloseCall;
	pDriverObject->MajorFunction[IRP_MJ_DEVICE_CONTROL] = IoControl;

	pDeviceObject->Flags |= DO_DIRECT_IO;
	pDeviceObject->Flags &= ~DO_DEVICE_INITIALIZING;

	return STATUS_SUCCESS;
}

void DriverUnload(PDRIVER_OBJECT pDriverObject)
{
	UNREFERENCED_PARAMETER(pDriverObject);

	IoDeleteSymbolicLink(&dos);
	IoDeleteDevice(pDriverObject->DeviceObject);

	DbgPrintEx(0, 0, "Driver unloaded\n");
}

//sc create Advent binPath="C:\Users\Jaras\source\repos\Advent\x64\Release\Advent.sys" type=kernel
//sc start Advent
//sc stop Advent
//sc delete Advent
