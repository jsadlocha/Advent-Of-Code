#include "solution.h"

void ProcessFile(PVOID pBuffer, SIZE_T nSize, PAdvent_Solution Advent)
{
	NTSTATUS NtStatus = { 0 };
	UINT32 i = 0;
	UINT32 k = 0;
	CHAR* pPos = (CHAR*)pBuffer;
	CHAR* pLine = (CHAR*)pBuffer;
	UINT32 nSum = 0;
	UINT32 nLastSum = 0;
	ULONG value = 0;
	UINT32 pBestOfTree[3] = { 0 };

	for (i = 0; i < nSize; i++)
	{
		if (*(pPos + i) == '\n')
		{
			*(pPos + i) = '\0';
			i++;
			
			NtStatus = RtlCharToInteger(pLine, 10, &value);
			if (NTSTATUS(NtStatus) != STATUS_SUCCESS)
			{
				DbgPrintEx(0, 0, "Error in converting string to number!\n");
				return;
			}

			nSum += value;
			pLine = (pPos + i);

			if (*(pPos + i) == '\n' || *(pPos + i) == '\0')
			{
				for (k = 0; k < 3; k++)
				{
					if (nSum > pBestOfTree[k])
					{
						nLastSum = pBestOfTree[k];
						pBestOfTree[k] = nSum;
						nSum = nLastSum;
					}

				}
				nSum = 0;
				pLine++;
				i++;
			}
		}
	}

	Advent->solution1 = pBestOfTree[0];

	for (k = 0; k < 3; k++)
	{
		Advent->solution2 += pBestOfTree[k];
		//DbgPrintEx(0, 0, "BestOfTree(%d): %d\n", k, pBestOfTree[k]);
	}

}

void Main(PUNICODE_STRING usPath, PAdvent_Solution Advent)
{
	HANDLE hFile = NULL;
	UNICODE_STRING strPath = { 0 };
	OBJECT_ATTRIBUTES objAttr = { 0 };

	NTSTATUS NtStatus = 0;
	IO_STATUS_BLOCK ioStatusBlock = { 0 };
	LARGE_INTEGER byteOffset = { 0 };
	ULONG nBufSize = 0;
	PVOID pBuffer = { 0 };
	FILE_STANDARD_INFORMATION fileInfo = { 0 };

	InitializeObjectAttributes(&objAttr, usPath,
		OBJ_CASE_INSENSITIVE | OBJ_INHERIT,
		NULL, NULL);

	if (KeGetCurrentIrql() != PASSIVE_LEVEL)
	{
		DbgPrintEx(0, 0, "High IRQL Level!\n");
		goto ERROR_HANDLING;
	}

	NtStatus = ZwCreateFile(&hFile,
		GENERIC_READ,
		&objAttr,
		&ioStatusBlock,
		NULL,
		FILE_ATTRIBUTE_NORMAL,
		FILE_SHARE_READ,
		FILE_OPEN,
		FILE_RANDOM_ACCESS | FILE_SYNCHRONOUS_IO_NONALERT | FILE_NON_DIRECTORY_FILE,
		NULL,
		0);

	if (!NT_SUCCESS(NtStatus))
	{
		DbgPrintEx(0, 0, "Cannot Open File!\n");
		goto ERROR_HANDLING;
	}

	NtStatus = ZwQueryInformationFile(hFile,
		&ioStatusBlock,
		&fileInfo,
		sizeof(fileInfo),
		FileStandardInformation);

	if (!NT_SUCCESS(NtStatus))
	{
		DbgPrintEx(0, 0, "Cannot read file information!\n");
		goto ERROR_HANDLING;
	}

	//DbgPrintEx(0, 0, "File size: %d\n", fileInfo.EndOfFile.LowPart);
	pBuffer = ExAllocatePool2(POOL_FLAG_PAGED, (SIZE_T)fileInfo.EndOfFile.LowPart, 'c0de');
	nBufSize = fileInfo.EndOfFile.LowPart;

	if (pBuffer == nullptr)
	{
		DbgPrintEx(0, 0, "Cannot allocate memory!\n");
		goto ERROR_HANDLING;
	}

	byteOffset.LowPart = byteOffset.HighPart = 0;
	NtStatus = ZwReadFile(hFile,
		NULL,
		NULL,
		NULL,
		&ioStatusBlock,
		pBuffer,
		nBufSize,
		&byteOffset,
		NULL);

	if (!NT_SUCCESS(NtStatus))
	{
		DbgPrintEx(0, 0, "Cannot Read File!\n");
		goto ERROR_HANDLING;
	}

	//DbgPrintEx(0, 0, "%s\n", pBuffer);	
	ProcessFile(pBuffer, nBufSize, Advent);

ERROR_HANDLING:
	if (pBuffer != nullptr)
		ExFreePoolWithTag(pBuffer, 'c0de');
	/*if (hFile != NULL)
		ZwClose(&hFile);*/ // Trigger BSOD even with currect handle
}
