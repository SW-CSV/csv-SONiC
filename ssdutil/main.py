#!/usr/bin/env python
#
# main.py
#
# Command-line utility for interacting with ssd in SONiC
#



try:
    from ssdutil import SsdUtil
    import imp
    import syslog
    import click
    import os
    import sys
except ImportError as e:
    raise ImportError("%s - required module not found" % str(e))

VERSION = '1.0'

VENDOR_PATH = "ssdvendors"


SYSLOG_IDENTIFIER = "ssdutil"

# Global ssd vendor class instance
global ssd_vendor


# ========================== Syslog wrappers ==========================


def log_info(msg, also_print_to_console=False):
    syslog.openlog(SYSLOG_IDENTIFIER)
    syslog.syslog(syslog.LOG_INFO, msg)
    syslog.closelog()

    if also_print_to_console:
        click.echo(msg)


def log_warning(msg, also_print_to_console=False):
    syslog.openlog(SYSLOG_IDENTIFIER)
    syslog.syslog(syslog.LOG_WARNING, msg)
    syslog.closelog()

    if also_print_to_console:
        click.echo(msg)


def log_error(msg, also_print_to_console=False):
    syslog.openlog(SYSLOG_IDENTIFIER)
    syslog.syslog(syslog.LOG_ERR, msg)
    syslog.closelog()

    if also_print_to_console:
        click.echo(msg)

# load ssd vendor module
def load_ssd_vendor(device):
    global ssd_vendor 
    dvModel = SsdUtil().get_device_model(device)   
    if "InnoDisk" in dvModel:    
        try:
            module_path = os.path.dirname(os.path.abspath(__file__))
            module_file = "/".join([module_path, VENDOR_PATH, "innodisk.py"]) 
            module = imp.load_source("innodisk", module_file)
        except IOError, e:
            log_error("Failed to load VENDOR module '%s': %s" % ("innodisk" , str(e)), True)
            return -1        
        try:
            ssd_vendor_class = getattr(module, "InnoDisk")
            ssd_vendor = ssd_vendor_class()
        except AttributeError, e:
            log_error("Failed to instantiate '%s' class: %s" % ("InnoDisk", str(e)), True)
            return -2
    elif "SanDisk" in dvModel:
        try:
            module_path = os.path.dirname(os.path.abspath(__file__))
            module_file = "/".join([module_path, VENDOR_PATH, "sandisk.py"]) 
            module = imp.load_source("sandisk", module_file)
        except IOError, e:
            log_error("Failed to load VENDOR module '%s': %s" % ("sandisk" , str(e)), True)
            return -1        
        try:
            ssd_vendor_class = getattr(module, "SanDisk")
            ssd_vendor = ssd_vendor_class()
        except AttributeError, e:
            log_error("Failed to instantiate '%s' class: %s" % ("SanDisk", str(e)), True)
            return -2
        
        pass
        # extend the ssd vendor module here
                
    return 0


# show ssd info

def print_test_title(testname):
    click.echo("{0:-^80s}".format("-"))
    click.echo("{name: ^80s}".format(name=testname))
    click.echo("{0:-^80s}".format("-"))





# ==================== CLI commands and groups ====================


# This is our main entrypoint - the main 'ssdutil' command
@click.group()
def cli():
    """ssdutil - Command line utility for providing SSD info"""
    if os.geteuid() != 0:
        click.echo("Root privileges are required for this operation")
        sys.exit(1)


# 'version' subcommand
@cli.command()
def version():
    """Display version info"""
    click.echo("ssdutil version {0}".format(VERSION))


# Vendor ssd info

@cli.command()
@click.argument("device")
def peCycle(device):
    """Show SSD P/E cycle"""    
    load_ssd_vendor(device)
    pecycle = ssd_vendor.get_pecycle(device)
    testname = "Show SSD P/E Cycle"
    print_test_title(testname)
    click.echo("Device P/E Cycle : {0}".format(pecycle))

   
@cli.command()
@click.argument("device")
def health(device):
    """Show SSD Health"""
    load_ssd_vendor(device)
    health = ssd_vendor.get_health(device)
    testname = "Show SSD Health"
    print_test_title(testname)
    click.echo("Device Health : {:.1%}".format(health))
  


@cli.command()
@click.argument("device")
def remaintime(device):
    """Show SSD Remaining Time"""
    load_ssd_vendor(device)
    rmtime = ssd_vendor.get_remain_time(device)
    testname = "Show SSD Remaining Time"
    print_test_title(testname)
    click.echo("Device Remaining Time : {} Hours".format(rmtime))
    
   


#['0', '0', '0', '0'] 
# for 'Later_Bad_Block' and 'Later_Bad_Blk_Inf_R/W/E'
@cli.command()
@click.argument("device")
def badblock(device):
    """Show SSD Bad Block"""
    load_ssd_vendor(device)
    infoList = ssd_vendor.get_bad_block(device)
    testname = "Show SSD Bad Block"
    print_test_title(testname)
    Later_Bad_Block = infoList[0]
    Later_Bad_Block_Read = infoList[1]
    Later_Bad_Block_Write = infoList[2]
    Later_Bad_Block_Erase = infoList[3]
    click.echo("Device Later_Bad_Block : {}".format(Later_Bad_Block))
    click.echo("Device Later_Bad_Block Read : {}".format(Later_Bad_Block_Read))
    click.echo("Device Later_Bad_Block Write : {}".format(Later_Bad_Block_Write))
    click.echo("Device Later_Bad_Block Erase : {}".format(Later_Bad_Block_Erase))
    
    
    
    
    
  
   

@cli.command()
@click.argument("device")
def temp(device):
    """Show SSD Temperature"""
    load_ssd_vendor(device)
    temp = ssd_vendor.get_temp(device)
    testname = "Show SSD Temperature"
    print_test_title(testname)
    click.echo("Device Temperature : {} C".format(temp))


#common ssd info

@cli.command()
@click.argument("device")
def device(device):
    """Show SSD Device Model"""
    dvModel = SsdUtil().get_device_model(device)
    testname = "Show SSD Device Model"
    print_test_title(testname)
    click.echo("Device Model : {}".format(dvModel))

   


@cli.command()
@click.argument("device")
def serialnum(device):
    """Show SSD Serial Number"""
    serialNum = SsdUtil().get_serial_num(device)
    testname = "Show SSD Serial Number"
    print_test_title(testname)
    click.echo("Device Serial Number : {}".format(serialNum))
  
    
@cli.command()
@click.argument("device")
def firmware(device):
    """Show SSD Firmware Version"""
    fwVersion = SsdUtil().get_firmware(device)
    testname = "Show SSD Firmware Version"
    print_test_title(testname)   
    click.echo("Device Firmware Version : {}".format(fwVersion))
 
 
@cli.command()
@click.argument("device")
def capacity(device):
    """Show SSD Capacity"""
    capacity = SsdUtil().get_capacity(device)
    testname = "Show SSD Capacity"
    print_test_title(testname) 
    click.echo("Device Capacity : {}".format(capacity))
   

if __name__ == '__main__':
    cli()
