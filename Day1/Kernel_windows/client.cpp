#include <iostream>
#include <windows.h>
#include <string>
#include <cstdint>

#define IO_GET_CLIENTADDRESS CTL_CODE(FILE_DEVICE_UNKNOWN, 0x2222, METHOD_BUFFERED, FILE_SPECIAL_ACCESS)

class Device
{
private:
	HANDLE hDevice;

public:
	Device(LPCSTR RegistryPath)
	{
		hDevice = CreateFileA(RegistryPath, GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE, 0, OPEN_EXISTING, 0, 0);
		if (hDevice == INVALID_HANDLE_VALUE)
			throw std::exception("Cannot open device!");
	}

	~Device()
	{
		if (hDevice)
			CloseHandle(hDevice);
	}

	std::uint64_t make_ioctl(std::string cmd)
	{
		CHAR Buf[256] = { 0 };
		DWORD Bytes;
		
		DeviceIoControl(hDevice, IO_GET_CLIENTADDRESS, (LPVOID)cmd.c_str(), (DWORD)cmd.size(), Buf, sizeof(Buf), &Bytes, NULL);
		std::cout << "Advent of Code\n\n" << Buf << std::endl;
		return 0x0;
	}

};

int main()
{
	try
	{
		Device device = Device("\\\\.\\Advent");
		device.make_ioctl("\\DosDevices\\C:\\Users\\Jaras\\Desktop\\input.txt");
	}
	catch (std::exception& e)
	{
		std::cout << e.what() << std::endl;
	}

	return 0;
}