path='D:\QLTDL.txt'
def save(line):

   
    f=open(path, 'a', encoding='utf8')
    f.writelines('\n')
    f.close()

def read(): 
    dl=[]

    
    f=open(path, 'r', encoding='utf8')
    for i in f:
        data=i.strip()
        arr=data.strip('-')
        dl.append(arr)
    f.close()

    return dl