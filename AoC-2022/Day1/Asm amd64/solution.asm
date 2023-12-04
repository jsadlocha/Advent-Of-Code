[bits 64]
section .text
global _start
; syscalls args
; syscall rax, rdi, rsi, rdx, r10, r8, r9

; int open(const char *pathname, int flags, mode_t mode);
; sys_open rax: 2
%macro sys_open 3
mov rdx, %3
mov rsi, %2
mov rdi, %1
mov rax, 2
syscall
%endmacro

; ssize_t read(int fd, void *buf, size_t count);
; sys_read rax: 0
%macro sys_read 3
mov rdx, %3
mov rsi, %2
mov rdi, %1
mov rax, 0
syscall
%endmacro

; ssize_t write(int fd, const void *buf, size_t count);
; sys_write rax: 1
%macro sys_write 3
mov rdx, %3
mov rsi, %2
mov rdi, %1
mov rax, 1
syscall
%endmacro

; int close(int fd);
; sys_close rax: 3
%macro sys_close 1
mov rdi, %1
mov rax, 3
syscall
%endmacro

; int fstat(int fd, struct stat *buf);
; fstat rax: 0x5
%macro sys_fstat 2
mov rsi, %2
mov rdi, %1
mov rax, 0x5
syscall 
%endmacro

; void exit(int status);
; sys_exit rax: 0x3c
%macro sys_exit 1
mov rdi, %1
mov rax, 0x3c
syscall
%endmacro

; char* strtok(char *str, const char del)
_strtok:
pop rdx; return val
pop rdi ;str
pop rbx ; del
push rdx

mov rax, 0
mov rcx, 0
.loop:
  mov byte al, [rdi+rcx]
  cmp al, 0
  je .end
  inc rcx
  cmp al, bl
  jne .loop

dec rcx
mov bl, 0
mov byte [rdi+rcx], bl
inc rcx
mov rax, rdi
add rax, rcx
ret

.end:
mov rax, 0
ret

; size_t strlen(const char *str)
_strlen:
pop rdx
pop rdi
push rdx

mov rcx, 0
.loop:
mov al, [rdi+rcx]
inc rcx
cmp al, 0
jne .loop

dec rcx
mov rax, rcx
ret

; char* reverse_string(char *str)
_reverse_string:
pop rsi
pop rdi
push rsi

push rdi
push rdi
call _strlen
mov rbx, rax ; len
pop rdi

mov rsi, rbx
shr rsi, 1
dec rbx
mov rcx, 0
mov rdx, 0
mov rax, 0

.loop:
  cmp rcx, rsi
  jge .end

  mov al, [rdi+rcx]
  mov r15, rbx
  sub r15, rcx
  mov dl, [rdi+r15]
  mov [rdi+rcx], dl
  mov [rdi+r15], al

  inc rcx
  jmp .loop

.end:
mov rax, rdi
ret

; int atoi(const char *str)
_atoi:
pop rdx
pop rdi
push rdx

push rdi
call _strlen
mov r15, rax ; str_len
sub r15, 1

mov r14, 0xa
mov rax, 0
mov rbx, 0
mov rdx, 0
mov rcx, 0

.loop:
  mov bl, [rdi+rcx]
  cmp bl, 0x30
  jl .end
  cmp bl, 0x39
  jg .end

  sub bl, 0x30
  add rax, rbx

  cmp rcx, r15
  jge .end

  inc rcx
  mul r14
  jmp .loop

.end:

ret

; char* itoa(int value, char *buf)//, int base)
_itoa:
pop rdx
pop rsi
pop rdi
push rdx
push rdi

mov rax, rsi
mov rbx, 0xa
mov rdx, 0

.loop:
  test rax, rax
  jz .end
  div rbx
  mov cl, [_ascii_number+rdx]
  mov rdx, 0
  mov [rdi], cl
  inc rdi
  jmp .loop

.end:
mov rax, 0
mov [rdi], al
pop rax

push rax
call _reverse_string
ret

; memset(void& addr, uint_8 value, int size)
_memset:
pop rbx
pop rdi
pop rax
pop rcx
push rbx

rep stosb

ret

; memcpy(void& src, void& dst, int size)
_memcpy:
pop rbx
pop rsi
pop rdi
pop rcx
push rbx

rep movsb

ret

; void std::endl()
_endl:
call .newline
db 0xa,0
.newline:
pop rax
sys_write 1, rax, 1
ret

; void qsort(int buf[], int low_boundary, int upper_boundary)
;;; local
; [rbp-0x8] buf
; [rbp-0x10] l_b
; [rbp-0x18] u_b
; [rbp-0x20] p - pivot idx
; [rbp-0x28] i - iterator
; [rbp-0x30] cmp value idx
_qsort:
pop rdi
pop rsi
pop rax
pop rdx
push rdi

push rbp
mov rbp, rsp
sub rsp, 40

mov [rbp-0x8], rsi
mov [rbp-0x10], rax
mov [rbp-0x18], rdx
mov [rbp-0x20], rax
mov [rbp-0x28], rax



;if up-lo < 2 return
mov rbx, [rbp-0x10]
mov rax, [rbp-0x18]
sub rax, rbx
mov rcx, 2
cmp rax, rcx
jl .end
; initialize local variable end


mov rdi, [rbp-0x8]
mov rax, [rbp-0x10]
mov rbx, [rdi+rax*8]
mov rcx, [rbp-0x18]
dec rcx
mov rax, [rdi+rcx*8]
add rax, rbx
shr rax, 1
mov [rbp-0x30], rax

.loop:
  ; mov rax, [rbp-0x30]
  mov rbx, [rbp-0x8]
  ; mov rcx, [rbx+rax*8] ; value to compare
  mov rcx, [rbp-0x30]
  mov rax, [rbp-0x28]
  mov rdx, [rbx+rax*8]
  cmp rdx, rcx
  jg .swap

  .inc:
  mov rax, [rbp-0x28]
  add rax, 1
  mov [rbp-0x28], rax
  mov rbx, [rbp-0x18]
  cmp rax, rbx
  jge .recursion
  jmp .loop
  .swap:
  mov rax, [rbp-0x8]
  mov rbx, [rbp-0x20]
  mov rdi, [rbp-0x28]
  mov rdx, [rax+rbx*8]
  mov rsi, [rax+rdi*8]
  mov [rax+rbx*8], rsi
  mov [rax+rdi*8], rdx

  mov rbx, [rbp-0x20]
  inc rbx
  mov [rbp-0x20], rbx
  jmp .inc

.recursion:
.left:
mov rax, [rbp-0x20]
push rax
mov rax, [rbp-0x10]
push rax
mov rax, [rbp-0x8]
push rax
call _qsort
.right:
mov rax, [rbp-0x18]
push rax
mov rax, [rbp-0x20]
push rax
mov rax, [rbp-0x8]
push rax
call _qsort

.end:
mov rsp, rbp
pop rbp
ret

; Main
; local variable
; [rbp - 0x8] uint64_t - sum
; [rbp - 0x10] uint64_t - counter
; [rbp - 0x18] uint64_t
; [rbp - 0x20] uint64_t
_start:
mov rbp, rsp
sub rsp, 32

sys_open _file_name, 0, 0
mov [_fd], rax

sys_fstat rax, _stat
mov rbx, [_st_size_offset]
mov rax, [_stat+rbx]
mov [_file_size], rax ; file size

; alloc file_buffer
sub rsp, rax
mov [_file_buf], rsp

mov rax, [_fd]
mov rcx, [_file_size]
sys_read rax, rsp, rcx ; read file

mov rax, [_fd]
sys_close rax

; mov rax, [_file_size]
; sys_write 1, rsp, rax ; print whole file

mov rax, [_file_buf]
mov [_iter], rax

mov rax, 0
mov [rbp-8], rax

.loop:
  ; debug exit
  ; mov rax, [_sum_buf_idx]
  ; cmp rax, 10
  ; jge .end
  ; debug exit
  mov rax, 0xa
  push rax
  mov rax, [_iter]
  push rax
  call _strtok

  test rax, rax
  jz .end ; if end of file

  mov [_iter_next], rax

  mov rax, [_iter]
  push rax
  call _strlen

  test rax, rax ; if new line
  jz .next

  mov rax, [_iter]
  push rax
  call _atoi

  mov rbx, [rbp-8]
  add rbx, rax
  mov [rbp-8], rbx

  mov rax, [_iter_next]
  mov [_iter], rax

  jmp .loop
  .next:
  mov rax, [rbp-8]
  mov rbx, [_sum_buf_idx]
  mov [_sum_buf+rbx*8], rax
  inc rbx
  mov [_sum_buf_idx], rbx
  mov rax, 0
  mov [rbp-8], rax

  mov rax, [_iter_next]
  mov [_iter], rax
  jmp .loop
.end:

mov rax, [_sum_buf_idx]
push rax
mov rax, 0
push rax
mov rax, _sum_buf
push rax
call _qsort

; printa all numbers for testing
; mov rax, 0
; mov [rbp-0x10], rax
; .loop_print:
;   mov rbx, [_sum_buf_idx]
;   mov rax, [rbp-0x10]
;   cmp rax, rbx
;   jge .end_print

;   mov rcx, _print_num
;   push rcx
;   mov rax, [rbp-0x10]
;   mov rbx, [_sum_buf+rax*8] 
;   push rbx
;   call _itoa

;   mov rax, _print_num
;   push rax
;   call _strlen

;   sys_write 1, _print_num, rax
;   call _endl

;   mov rax, [rbp-0x10]
;   inc rax
;   mov [rbp-0x10], rax

;   jmp .loop_print
; .end_print:


; solution1
sys_write 1, _solution1, _sol1len
mov rax, _print_num
push _print_num
mov rax, [_sum_buf]
push rax
call _itoa

mov rax, _print_num
push rax
call _strlen

sys_write 1, _print_num, rax
call _endl

; solution2
sys_write 1, _solution2, _sol2len
mov rcx, _sum_buf
mov rax, [rcx]
mov rbx, [rcx+0x8]
add rax, rbx
mov rbx, [rcx+0x10]
add rax, rbx

mov r15, rax

mov rax, _print_num
push _print_num
push r15
call _itoa

mov rax, _print_num
push rax
call _strlen

sys_write 1, _print_num, rax

call _endl


mov rsp, rbp ; clean stack
mov rax, 0
sys_exit rax ; exit program

section .data
_solution1 db "Solution1: ",0
_sol1len equ $-_solution1
_solution2 db "Solution2: ",0
_sol2len equ $-_solution2

; file variable
_file_name db "input.txt", 0
_file_len equ $-_file_name
_fd dq 0x0
_file_buf dq 0x0
_file_size dq 0x0

_st_size_offset dq 0x30

_iter_next dq 0x0
_iter dq 0x0
_buffer_len dq 0x0

_sum_buf_idx dq 0x0

_ascii_number db "0123456789"

section .bss
_stat: resb 145 ; struct stat
_print_num: resb 64
_sum_buf: resq 500 ; buffer with uint64_t callories list

; build schemat
; nasm -f elf64 syscalls.asm -o syscalls.elf
; ld syscalls.elf -o syscalls.o
; ./syscalls.o