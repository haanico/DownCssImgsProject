from hashlib import md5

def calMD5(str):
  m = md5()
  m.update(str)
  return m.hexdigest() 
   
 
def calMD5ForFile(file):
  m = md5()
  a_file = open(file, 'rb')
  m.update(a_file.read())
  a_file.close()
  return m.hexdigest()
    
def calMD5ForFolder(dir,MD5File):
  import os
  outfile = open(MD5File,'w')
  for root, subdirs, files in os.walk(dir):
    for file in files:
      filefullpath = os.path.join(root,file)
      print filefullpath
      filerelpath = os.path.relpath(filefullpath,dir)
      md5 = calMD5ForFile(filefullpath)
      outfile.write(filerelpath + ' ' + md5 + '\n')
  outfile.close()
  
  
print calMD5('This is one test string')
print calMD5ForFile('g:\\t3.py')
calMD5ForFolder('g:\\alipay','g:\\mdfile.md5')