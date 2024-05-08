import subprocess

if __name__ == '__main__':
   
    
    process2 = subprocess.Popen(['python', 'mysqldata.py'])
    process3 = subprocess.Popen(['python', 'maincarla.py'])
    process1 = subprocess.Popen(['python', 'gui.py'])
    process4 = subprocess.Popen(['python', 'mainsa.py'])

    
    process2.wait()
    process3.wait()
    process1.wait()
    process4.wait()

    print("Both processes completed.")