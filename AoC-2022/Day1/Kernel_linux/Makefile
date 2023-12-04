KDIR = /lib/modules/`uname -r`/build
obj-m = solution.o

all:
	make -C $(KDIR) M=$(PWD) modules
clean:
	make -C $(KDIR) M=$(PWD) clean
load:
	insmod solution.ko path=$(path)
	rmmod solution.ko
	dmesg
