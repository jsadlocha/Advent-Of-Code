#include "ioctl.h"
#include "solution.h"

NTSTATUS CreateCall(PDEVICE_OBJECT pDeviceObject, PIRP pIrp)
{
	UNREFERENCED_PARAMETER(pDeviceObject);
	pIrp->IoStatus.Status = STATUS_SUCCESS;
	pIrp->IoStatus.Information = 0;

	IoCompleteRequest(pIrp, IO_NO_INCREMENT);

	DbgPrintEx(0, 0, "Open Device kerneldriver!\n");

	return STATUS_SUCCESS;
}

NTSTATUS CloseCall(PDEVICE_OBJECT pDeviceObject, PIRP pIrp)
{
	UNREFERENCED_PARAMETER(pDeviceObject);
	pIrp->IoStatus.Status = STATUS_SUCCESS;
	pIrp->IoStatus.Information = 0;

	IoCompleteRequest(pIrp, IO_NO_INCREMENT);

	DbgPrintEx(0, 0, "Close Device kerneldriver!\n");

	return STATUS_SUCCESS;
}

NTSTATUS IoControl(PDEVICE_OBJECT pDeviceObject, PIRP pIrp)
{
	UNREFERENCED_PARAMETER(pDeviceObject);
	NTSTATUS Status = STATUS_UNSUCCESSFUL;
	SIZE_T ByteIO = 0;
	ANSI_STRING asPath;
	UNICODE_STRING usPath;
	Advent_Solution Advent = { 0 };
	UNICODE_STRING usResponse = { 0 };
	ANSI_STRING asResponse = { 0 };

	usResponse.Buffer = (PWCH)ExAllocatePool2(POOL_FLAG_PAGED, 128, 'dead');
	if (usResponse.Buffer == NULL)
	{
		DbgPrintEx(0, 0, "Memory allocation error!\n");
		goto ERROR;
	}
	usResponse.Length = 0;
	usResponse.MaximumLength = 128;
	

	PIO_STACK_LOCATION stack = IoGetCurrentIrpStackLocation(pIrp);

	ULONG ControlCode = stack->Parameters.DeviceIoControl.IoControlCode;
	DbgPrintEx(0, 0, "IoControl kerneldriver\n");

	if (ControlCode == IO_GET_CLIENTADDRESS)
	{
		//DbgPrintEx(0, 0, "Output Buffer: %u\n", stack->Parameters.DeviceIoControl.OutputBufferLength);
		DbgPrintEx(0, 0, "Data From Userpace: %s\n", (LPCSTR)pIrp->AssociatedIrp.SystemBuffer);

		RtlInitAnsiString(&asPath, (LPCSTR)pIrp->AssociatedIrp.SystemBuffer);
		RtlAnsiStringToUnicodeString(&usPath, &asPath, TRUE);

		Main(&usPath, &Advent);
		//DbgPrintEx(0, 0, "Unicode: %wZ\n", usPath);
		RtlFreeUnicodeString(&usPath);

		//DbgPrintEx(0, 0, "Advent1: %d", Advent.solution1);
		//DbgPrintEx(0, 0, "Advent2: %d", Advent.solution2);

		RtlUnicodeStringPrintf(&usResponse, L"Solution1: %d\nSolution2: %d\n", Advent.solution1, Advent.solution2);
		//DbgPrintEx(0, 0, "Sol\n%wZ\n", &usResponse);
		
		//ByteIO = nMsgLength > (*stack).Parameters.DeviceIoControl.OutputBufferLength ? (*stack).Parameters.DeviceIoControl.OutputBufferLength : nMsgLength;

		RtlUnicodeStringToAnsiString(&asResponse, &usResponse, TRUE);
		ByteIO = asResponse.Length > (*stack).Parameters.DeviceIoControl.OutputBufferLength ? (*stack).Parameters.DeviceIoControl.OutputBufferLength : asResponse.Length;
		RtlCopyMemory(pIrp->AssociatedIrp.SystemBuffer, asResponse.Buffer, ByteIO);

		RtlFreeAnsiString(&asResponse);

		Status = STATUS_SUCCESS;
	}

	ERROR:
	ExFreePoolWithTag(usResponse.Buffer, 'dead');
	pIrp->IoStatus.Status = Status;
	pIrp->IoStatus.Information = ByteIO;
	IoCompleteRequest(pIrp, IO_NO_INCREMENT);

	return Status;
}
