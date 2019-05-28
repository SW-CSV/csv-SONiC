#!/usr/bin/env python


# SSD specific interface for Innodisk Vendor

try:  
    import os
    import yaml
    import subprocess
except ImportError as e:
    raise ImportError("%s - required module not found" % str(e))

class InnoDisk():
    def __init__(self):
        pass
    
    # get ssd P/E cycle info
    def get_pecycle(self, device):
        check = 0
        command = "sudo smartctl -i " + device
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        output = proc.stdout.readlines()
        (out, err) = proc.communicate()
        #smartctl cmd return failed
        if proc.returncode > 0:
            for line in output:
                print(line.strip())
            return
        else:
            for line in output:
                if "Device Model" in line:
                    check = 1
                    if ("3ME3" in line) or ("3ME4" in line):
                        cycle = 3000
                    elif ("3IE3" in line):
                        cycle = 20000
                    else:
                        print(line.strip())
                        print("Device Model Not Match 3ME3 3ME4 or 3IE3")
                        return
        if check == 0:
            print("Can't get 'Device Model' attributes")
            return
        else:
            return cycle
            #3000
    
    # get ssd health info
    def get_health(self, device):
        check = 0
        # get the SSd P/E cycle
        cycle = self.get_pecycle(device)
        command = "sudo smartctl -A " + device
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        output = proc.stdout.readlines()
        (out, err) = proc.communicate()
        #smartctl cmd return failed
        if proc.returncode > 0:
            for line in output:
                print(line.strip())
            return
        else:
            for line in output:
                if "Average_Erase_Count" in line:
                #  Average_Erase_Count     0x0002   048   001   000    Old_age   Always       -       48
                    check = 1
                    rawval = line.split()[-1]
                    avgerase = float(rawval)  
               #health_pre = (P/E cycle - AVG erese)/ P/E cycle
                    health= (cycle - avgerase) / cycle
                    health = round(health, 5)
        if check == 0:
            print("Can't get 'Device Model' attributes")
            return
        else:
            return health
        # 0.983

    # get ssd remainning time info
    def get_remain_time(self, device):
        check = 0
        # get the SSD health
        health = self.get_health(device)     
        command = "sudo smartctl -A " + device
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        output = proc.stdout.readlines()
        (out, err) = proc.communicate()
        #smartctl cmd return failed
        if proc.returncode > 0:
            for line in output:
                print(line.strip())
            return
        else:
            for line in output:
                if "Power_On_Hours" in line:
                # 9 Power_On_Hours          0x0002   080   000   000    Old_age   Always       -       2640
                    check = 1
                    rawval = line.split()[-1]
                    poweron = int(rawval)
                    #remain_time = poweron_time / (1 - health_pre) - poweron_time
                    remainTime = poweron / (1 - health  ) - poweron
        if check == 0:
            print("Can't get 'Power_On_Hours' attributes")
            return
        else:
            return int(remainTime)
        #  12345
        
    # get ssd badblock info  
    def get_bad_block(self, device):
        check = 0
        _blockList = []
        command = "sudo smartctl -A " + device
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        output = proc.stdout.readlines()
        (out, err) = proc.communicate()
        if proc.returncode > 0:
            for line in output:
                print(line.strip())
            return
        else:
            for line in output:
                if "Later_Bad_Block" in line:
                    check += 1 
                #  Later_Bad_Block         0x0013   100   100   001    Pre-fail  Always       -       0        
                    rawval = line.split()[-1]
                    _blockList.append(rawval)
                if "Later_Bad_Blk_Inf_R/W/E" in line:
                    check += 1
                # Later_Bad_Blk_Inf_R/W/E 0x0002   000   000   000    Old_age   Always       -       0 0 0            
                    rawval_read = line.split()[-3]
                    rawval_write = line.split()[-2]
                    rawval_erase = line.split()[-1]
                    _blockList.append(rawval_read)
                    _blockList.append(rawval_write)
                    _blockList.append(rawval_erase)
        if check == 0:
            print("Can't get any 'Later_Bad_Block' attributes")
            return
        elif check == 1:
            print("Can't get all 'Later_Bad_Block' attributes")
            return _blockList
        else:
            return _blockList
            #['0', '0', '0', '0'] 
            # for 'Later_Bad_Block' and 'Later_Bad_Blk_Inf_R/W/E'
            
    # get ssd temperature info        
    def get_temp(self, device):
        check = 0
        command = "sudo smartctl -A " + device
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        output = proc.stdout.readlines()
        (out, err) = proc.communicate()
        if proc.returncode > 0:
            for line in output:
                print(line.strip())
            return
        else:
            for line in output:
                if "Temperature_Celsius" in line:
                # Temperature_Celsius     0x0000   030   100   000    Old_age   Offline      -       30 (2 100 0 0 0)
                    check = 1
                    rawval = line.split()[9]         
        if check == 0:
            print("Can't get all 'Temperature_Celsius' attributes")
            return 
        else:
            return rawval
            # '30'   
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        