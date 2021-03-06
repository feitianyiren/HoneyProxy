import os, os.path, shutil, psutil
from datetime import date
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--file', dest='filename', action='store', type=str)
args = parser.parse_args()

filename = "snapshot-%(date)s-web.zip" % {"date": date.today().strftime("%Y%m%d")} if not args.filename else args.filename

print "Working directory: %s" % os.getcwd()

if os.path.isfile(filename):
    print "Delete existing %s" % filename
    os.remove(filename)

url = "http://honeyproxy.org/download/%s" % filename
print "Download latest snapshot"
os.system("wget %s" % url)
	
honeyproxy_processes = filter(lambda x: x.name == "python2" and any("honeyproxy.py" in y for y in x.cmdline), psutil.process_iter())
for p in honeyproxy_processes:
	print "Kill HoneyProxy instance..."
	p.kill()
	
if os.path.isdir('./honeyproxy'):
	print "Delete existing installation"
	shutil.rmtree('./honeyproxy')

print "Unzip new snapshot..."
os.system("unzip -q %s -d honeyproxy" % filename)
print "Start HoneyProxy..."
os.system("sh honey.sh")
print "Delete snapshot zip archive..."
os.remove(filename)
print "done!"
