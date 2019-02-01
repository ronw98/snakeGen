import os

if __name__=='__main__':
    os.system('mkdir test')
    os.system('cd test')
    with open('test.txt','w') as file:
        file.write("oui")