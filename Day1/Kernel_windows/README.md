# Windows kernel driver solution!

### How to run
- Required Microsoft Visual studio with wdk
- Virtual machine with windows 10
- Prepare test mode and reboot
- Load and start driver
- Compile client and specify file path with input data for solve(first day task)
- And just run client who connect to kernel driver using ioctl

### Test mode
- `bcdedit /debug on`
- `bcdedit /dbgsettings net hostip:192.168.100.100 port:53000` - optionally debug ip/port for virtual machine
- `bcdedit /set testsigning on`

### Load and start Driver
- `sc create KernelDriver binPath="C:\Users\\...\source\repos\KernelDriver\x64\Release\KernelDriver.sys" type=kernel`
- `sc start KernelDriver`

### Stop and delete
- `sc stop KernelDriver`
- `sc delete KernelDriver`

### Client 
- Set file path `"\\DosDevices\\C:\\Users\\Desktop\\input.txt"` where is input.txt file located with `\\DosDevice\\` prefix
- compile `g++ client.cpp -o client.exe`
- run