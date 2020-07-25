#! /usr/bin/env python

""" This script is used to insert the data to database
    Running as a deamon, write stdout to record.log
"""

import sys, os, time, atexit
from signal import SIGTERM
import logging
import time
import sys
import abc
 
class Daemon(object):
    def __init__(self, pidfile, logfile=None):

        self.pidfile = pidfile
        self.log = logging.getLogger("{} Logging".format(self.__class__.__name__))

        self.log.setLevel(logging.INFO)
        ch = logging.FileHandler(filename = logfile if logfile 
                                                    else "{}.log".format(self.__class__.__name__))
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)
       
    def daemonize(self):
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as e:
            self.log.error("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
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
            self.log.error("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
        
        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
    
        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        open(self.pidfile,'w+').write("%s\n" % pid)
       
    def delpid(self):
        self.log.info("Stop running deamon...")
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
        self.log.info("Start running daemon...")
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

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError 


if __name__ == "__main__":

    class TestDaemon(Daemon):
        def __init__(self, pidfile):
            super().__init__(pidfile)

        def run(self):
            self.log.info("Start running deamon")
            while True:
                time.sleep(1)
                self.log.info("Waiting for 1s ...")

    pidf = "record.pid"
    dc = TestDaemon(pidf)

    if sys.argv[1] == "start":
        dc.start()
    elif sys.argv[1] == "stop":
        dc.stop()
    elif sys.argv[1] == "restart":
        dc.restart()
    else:
        print("Unknown command: ", sys.argv[1])
