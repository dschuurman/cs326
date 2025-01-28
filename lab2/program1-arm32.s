@ ARM32 Assembler program to print a greeting
@ CS326 Embedded System and IoT

.data
message: .ascii  "Hello World!\nAssembled and run on a 32-bit Raspberry Pi.\n"
.text
.global _start
_start:
@ Make a Linux system call to print the message
   mov r0, #1        @ File descriptor 1 (stdout)
   ldr r1, =message  @ Load message address into r1
   mov r2, #57       @ Length of message in bytes
   mov r7, #4        @ System call number 4 (write)
   svc 0             @ perform system call

@ Make Linux system call to terminate program
   mov     r0, #0    @ Return code 0 (success)
   mov     r7, #1    @ System call number 1 (exit)
   svc     0         @ perform system call
