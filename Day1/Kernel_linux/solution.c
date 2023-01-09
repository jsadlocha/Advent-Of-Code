#include <linux/module.h>
#include <linux/fs.h>
#include <linux/device.h>
#include <linux/moduleparam.h>
#include <linux/slab.h>
#include <linux/sort.h>

static char *path = "";
module_param(path, charp, 0660);

static int init_func(struct subprocess_info *info, struct cred *new)
{
  int uid = 1000;
  int gid = 1000;
  new->uid = new->euid = new->suid = new->fsuid = KUIDT_INIT(uid);
  new->gid = new->egid = new->sgid = new->fsgid = KGIDT_INIT(gid);
  return 0;
}
static int run_cmd(int s1, int s2)
{
  const char *fmt = "echo \"Advent of Code Day1:\n\";echo \"Solution1: %d\n\";echo \"Solution2: %d\n\n\";bash";
  char buf[128];
	struct subprocess_info *sub_info;
	static char *envp[] = {
    "XDG_RUNTIME_DIR=/run/user/1000",
    "DISPLAY=:0",
		"HOME=/",
		"PATH=/sbin:/bin:/usr/sbin:/usr/bin",
		NULL
	};
  char *argv[] = {"/usr/bin/gnome-terminal", "--", "bash", "-c", NULL, NULL};
	int ret;
	snprintf(buf, 128, fmt, s1, s2);
	argv[4] = buf;
	
	sub_info = call_usermodehelper_setup(argv[0], argv, envp, GFP_ATOMIC,
            init_func, NULL, NULL);
  ret = call_usermodehelper_exec(sub_info, UMH_KILLABLE);
	return ret;
}

static char* strtok(char *buf, char delim)
{
  while (1)
  { 
    if (*buf == '\0')
    {
      buf = 0;
      break;
    }
    
    if (*buf == delim)
    {
      *buf = '\0';
      buf++;
      break;
    }
    buf++;
  }
   
  return buf;
}

static int parse_nums(char p_buf[], int n_buf[])
{
  char *next;
  int sum = 0;
  long res = 0;
  int count = 0;
  while (1)
  {
    next = strtok(p_buf, '\n');
    if (strlen(p_buf) == 0) {
      n_buf[count] = sum;
      count += 1;
      sum = 0;
    } else {
      if (kstrtol(p_buf, 10, &res))
      {
        printk(KERN_ALERT "Parsing number error!");
        return 0;
      }
      sum += res;
    }
    
    if (next == 0)
    {
      n_buf[count] = sum;
      count += 1;
      break;
    }
    
    p_buf = next;
  }
  
  return count;
}

static int cmp_func(const void *num1, const void *num2)
{
  return *(int*)num2 - *(int*)num1;
}

static void swap_func(void *num1, void *num2, int size)
{
  int tmp;
  tmp = *(int*)num1;
  *(int*)num1 = *(int*)num2;
  *(int*)num2 = tmp;
}

static int advent_init(void)
{
  struct file *f;
  int ret = 0;
  int *n_buf;
  int n_count = 0;
  
  char *p_buf;
  loff_t size = 0;
  loff_t pos = 0;
  //int i = 0;
  if (strlen(path) == 0)
  {
  	printk(KERN_ALERT "PATH param is empty!\n");
  	return 0;
  }
  n_buf = (int*)kmalloc(512 * sizeof(int), GFP_KERNEL);
  if (n_buf == 0)
  {
    printk(KERN_ALERT "Memory error!\n");
    return 0;
  }
  printk(KERN_INFO "ADVENT INIT\n");

  printk(KERN_INFO "Module_Param: %s\n", path);
  
  f = filp_open(path, O_RDONLY, 0);
  if (f == NULL)
    printk(KERN_ALERT "Cannot open file!\n");
  else {
    size = i_size_read(file_inode(f));
    p_buf = (char*)kmalloc(size, GFP_KERNEL);
    if (p_buf == 0)
    {
    	printk(KERN_ALERT "Memory error!\n");
    	goto exit;
    }
    printk(KERN_INFO "File size: %lld\n", size);
    kernel_read(f, p_buf, size, &pos);
    
    n_count = parse_nums(p_buf, n_buf);
    kfree(p_buf);
    if(n_count == 0)
    {
      printk(KERN_ALERT "ERROR parsing\n");
      goto exit;
    }

    sort(n_buf, n_count, sizeof(int), cmp_func, swap_func);
    //printk(KERN_INFO "NUMS: \n");    
    //for (i = 0; i < n_count; i++)
    //{
    //  printk("%d\n", n_buf[i]);
    //}
    printk(KERN_INFO "Solution1: %d\n", n_buf[0]);
    printk(KERN_INFO "Solution2: %d\n", n_buf[0]+n_buf[1]+n_buf[2]);
    ret = run_cmd(n_buf[0], n_buf[0]+n_buf[1]+n_buf[2]);
    if (ret != 0)
    {
      printk(KERN_ALERT "Terminal open error!\n");
    }
  }
exit:
  filp_close(f, NULL);
  kfree(n_buf);
  return 0;
}

static void __exit advent_exit(void)
{
  printk(KERN_INFO "Advent Exit\n");
}

module_init(advent_init)
module_exit(advent_exit)

MODULE_LICENSE("GPL");
MODULE_AUTHOR("jsadlocha");
MODULE_DESCRIPTION("Advent Day1");
