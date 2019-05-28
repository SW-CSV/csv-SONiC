#!/usr/bin/env python




# ssdutil.py
# platform-common SSD interface for SONIC





try:  
    import os
    import yaml
    import subprocess
except ImportError as e:
    raise ImportError("%s - required module not found" % str(e))



class SsdUtil():
    
    def __init__(self):
        pass 
        
    # get ssd firmware version info
    def get_firmware(self, device):
        check = 0
        command = "sudo smartctl -i " + device
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        output = proc.stdout.readlines()
        (out, err) = proc.communicate()
        if proc.returncode > 0:
            for line in output:
                print(line.strip())
            return
        else:
            for line in output:
                if "Firmware Version" in line:
                #  Firmware Version: S17411
                    check = 1
                    fwVersion = line.split(':')[-1].strip()
        if check == 0:
            print("Can't get 'Firmware Version' attributes")
            return
        else:
            return fwVersion
            # S17411
            
            
    # get ssd serial number info
    def get_serial_num(self, device):
        check = 0
        command = "sudo smartctl -i " + device
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        output = proc.stdout.readlines()
        (out, err) = proc.communicate()
        if proc.returncode > 0:
            for line in output:
                print(line.strip())
            return
        else:
            for line in output:
                if "Serial Number" in line:
                #Serial Number:    BCA11709250230058
                    check = 1
                    serialNum = line.split(':')[-1].strip()
        if check == 0:
            print("Can't get 'Serial Number' attributes")
            return
        else:
            return serialNum
            # 'BCA11709250230058'
            
        
    # get ssd device model info
    def get_device_model(self, device):
        check = 0
        command = "sudo smartctl -i " + device
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        output = proc.stdout.readlines()
        (out, err) = proc.communicate()
        if proc.returncode > 0:
            for line in output:
                print(line.strip())
            return
        else:
            for line in output:
                if "Device Model" in line:
                #Device Model:     InnoDisk Corp. - mSATA 3ME3
                    check = 1
                    dvModel = line.split(':')[-1].strip()
        if check == 0:
            print("Can't get 'Device Model' attributes")
            return
        else:
            return dvModel
            # 'InnoDisk Corp. - mSATA 3ME3'    
        
    
    
    def get_capacity(self, device):
        check = 0
        command = "sudo smartctl -i " + device
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        output = proc.stdout.readlines()
        (out, err) = proc.communicate()
        if proc.returncode > 0:
            for line in output:
                print(line.strip())
            return
        else:
            for line in output:
                if "User Capacity" in line:
                # User Capacity:    16,013,942,784 bytes [16.0 GB]
                    check = 1
                    capacity = line.split(':')[-1].strip()
        if check == 0:
            print("Can't get 'User Capacity' attributes")
            return
        else:
            return capacity
            # '16,013,942,784 bytes [16.0 GB]'
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
