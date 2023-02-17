@ ARM Assembler program to print a greeting
@ CS326 Embedded System and IoT

.data
message: .ascii  "Hello World!\nAssembled and run on a Raspberry Pi.\n"
.text
.global _start
_start: 
@ Make a Linux system call to print the message
   mov r0, #0
   ldr r1, =message
   mov r2, #49
   mov r7, #4
   svc 0

@ Make Linux system call to terminate program
   mov     r0, #0
   mov     r7, #1
   svc     0
