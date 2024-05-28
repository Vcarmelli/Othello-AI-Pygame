import subprocess
import threading

def run_subprocess(command):
    # Start the subprocess
    proc = subprocess.Popen(command,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True)
    
    # Print the process ID of the subprocess
    print(f"Subprocess PID: {proc.pid}")
    
    # Write a command to the subprocess stdin
    input_command = "print('Hello from subprocess!')\n"
    proc.stdin.write(input_command)
    
    # Flush the stdin to ensure the command is sent
    proc.stdin.flush()
    
    # Read the output
    output = proc.stdout.readline()
    print(f"Subprocess output: {output}")
    input("PRESS")
    # Terminate the subprocess
    proc.terminate()

# List of commands to run in subprocesses
commands = [
    ['python', '-u', '-c', 'while True: exec(input())'],
    ['python', '-u', '-c', 'while True: exec(input())'],
    ['python', '-u', '-c', 'while True: exec(input())']
]

# Create and start threads
threads = []
for command in commands:
    thread = threading.Thread(target=run_subprocess, args=(command,))
    threads.append(thread)
    thread.start()
    

# Wait for all threads to complete
for thread in threads:
    thread.join()
