#! /usr/bin/env python

""" This script is used to insert the data to database
    Running as a deamon, write stdout to record.log
"""

import sys, os, time, atexit
from signal import SIGTERM
import logging
import time
import sys

from sqlalchemy import Table, MetaData, create_engine
from sqlalchemy.dialects.postgresql import insert
import sensor
import datetime
 
class Daemon:
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
       
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
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
        
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
            sys.stderr.write(message % self.pidfile)
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
                message = "pidfile %s does not exist. Daemon not running?\n"
                sys.stderr.write(message % self.pidfile)
                return # not an error in a restart
 
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
                        print(str(err))
                        sys.exit(1)
 
    def restart(self):
        self.stop()
        self.start()
 
    def run(self):
        raise NotImplementedError 

def insert_data(engine):
    with engine.connect() as conn:
        meta = MetaData()
        wp = Table('weather_param', meta, autoload=True, autoload_with=conn)
        # print(meta.tables)
        t, h, p = sensor.bme280.temperature, sensor.bme280.humidity, sensor.bme280.pressure
        st = insert(wp).values(temperature=t,
                               humidity=h, 
                               pressure=p,
                               record_time=datetime.datetime.now())
        conn.execute(st)
    return t, h, p

class DataCollectorDaemon(Daemon):
    
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null', interval=10):
        super().__init__(pidfile, stdin, stdout, stderr)
        self.interval = interval

    def run(self):
       
        logging.basicConfig(format='%(asctime)s - %(process)d - %(levelname)s - %(message)s')
        logging.info("Collecting process started...")

        engine = create_engine("postgresql:///weather")

        while True:
            ret = insert_data(engine)
            logging.info(str(ret))
            time.sleep(self.interval)

if __name__ == "__main__":
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
