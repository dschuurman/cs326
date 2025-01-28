// ARM64 Assembler program to print a greeting
// CS326 Embedded System and IoT

.data
message: .ascii  "Hello World!\nAssembled and run on a 64-bit Raspberry Pi.\n"

.text
.global _start

_start: 
// Linux system call to print message
    mov     w0, #1          // File descriptor 1 (stdout)
    ldr     x1, =message    // Load address of message
    mov     w2, #57         // Message length
    mov     w8, #64         // system call for write operation
    svc     #0              // perform system call

// Linux system call to terminate program
    mov     w0, #0          // Return code 0 (success)
    mov     w8, #93         // exit system call
    svc     #0              // terminate program
