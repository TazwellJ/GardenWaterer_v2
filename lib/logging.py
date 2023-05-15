import io, os
 
class logToFile(io.IOBase):
    def __init__(self):
        pass
 
    def write(self, data):
        logFileName = 'info_{}.log'.format(strftime('%d_%m_%Y_%T'))
        with open(logFileName, mode="a") as f:
            f.write(data)
        return len(data)
      
# now your console text output is saved into file
os.dupterm(logToFile())
 
# disable logging to file
os.dupterm(None)
