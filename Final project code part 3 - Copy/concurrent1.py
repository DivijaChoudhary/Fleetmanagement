import subprocess

if __name__ == '__main__':
   
    
    process2 = subprocess.Popen(['python', 'mysqldata.py'])
    process3 = subprocess.Popen(['python', 'maincarla.py'])
    process1 = subprocess.Popen(['python', 'gui.py'])

    
    process2.wait()
    process2.wait()
    process1.wait()

    print("Both processes completed.")