#! /usr/bin/env python

""" This script is used to insert the data to database
    Running as a deamon, write stdout to record.log
"""

import sys, os, time, atexit
from signal import SIGTERM
import logging
import time
import sys
 
class Daemon(object):
    def __init__(self, pidfile, stdin=None, stdout=None, stderr=None):

        if not stdin:
            self.stdin = open("/dev/null", "r")
        else:
            self.stdin = open(stdin, "r")

        if not stdout:
            self.stdout = open("/dev/null", "a+")
        else:
            self.stdout = open(stdout, "a+")

        if stdout == stderr:
            self.stderr = self.stdout
        else:
            self.stderr = open(stderr, "a+")

        self.pidfile = pidfile
        self.log = logging.getLogger("{} Logging".format(self.__class__.__name__))
        self.log.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

       
    def daemonize(self):
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
        
        # decouple from parent environment
        #os.chdir("/")
        os.setsid()
        os.umask(0)
        
        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
        
        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        
        sys.stdin = self.stdin
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        
        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        open(self.pidfile,'w+').write("%s\n" % pid)
       
    def delpid(self):
        os.remove(self.pidfile)
 
    def start(self):
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = open(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
            
        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            self.log.error(message.format(self.pidfile))
            sys.exit(1)
            
        # Start the daemon
        self.daemonize()
        self.run()
 
    def stop(self):
        # Get the pid from the pidfile
        try:
            pf = open(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
       
        if not pid:
            message = "pidfile {} does not exist. Daemon not running?\n"
            self.log.warning(message.format(self.pidfile))
            return

        # Try killing the daemon process       
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                self.log.error(str(err))
                sys.exit(1)
 
    def restart(self):
        self.stop()
        self.start()
 
    def run(self):
        raise NotImplementedError 



if __name__ == "__main__":

    # class TestDaemon()


    fout = "record.log"
    pidf = "record.pid"
    dc = DataCollectorDaemon(pidf, "/dev/null", fout, fout, interval=600)

    if sys.argv[1] == "start":
        dc.start()
    elif sys.argv[1] == "stop":
        dc.stop()
    elif sys.argv[1] == "restart":
        dc.restart()
    else:
        print("Unknown command: ", sys.argv[1])
