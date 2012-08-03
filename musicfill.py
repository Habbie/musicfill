#!/usr/bin/env python
import os, sys, random, bisect, shutil

# size in MB
def dirsize(dir, files):
	total = 0
	for f in files:
		size = os.stat(os.path.join(dir, f)).st_size
		size = size / (1024*1024)
		total = total + size
	return total

def scan(path):
	dirs=list()
	for dir in os.walk(path):
		path, subdirs, files = dir
		files = [s for s in files if not s.startswith('.')]
		if not files:
			continue
		# print path, files
		size=dirsize(path, files)
		dirs.append((size, path))
	dirs.sort()
	return dirs

def copy(path, dir):
	if dir.startswith("./"):
		dir = dir[2:]
	targetpath = os.path.join(path, "-".join(os.path.split(dir)))
	print "copying %s to %s" % (dir, targetpath)
	shutil.copytree(dir, targetpath)

# size and sizes in MB
# modifies dirs, dirs
def fill(path, dirs):
	while True:
		s = os.statvfs(path)
		free = (s.f_frsize*s.f_bfree / 1048576) * 0.9  # megabytes
		cutoff = bisect.bisect(dirs, (free, None))
		if cutoff == 0:
			print "free %sM, %s dirs left, nothing fits" % (free, len(dirs))
			break
		choice = random.randint(0, cutoff-1)
		print "free %sM, picked %s (%sM) out of %s left" % (free, dirs[choice][1], dirs[choice][0], len(dirs))
		copy(path, dirs[choice][1])
		del dirs[choice]

def main():
	# sizes in MB
	dirs = scan('.')
	while dirs:
		targetpath = ""
		while not targetpath:
			os.system('/sbin/mount')
			targetpath=raw_input("enter path and push enter... ")
		fill(targetpath, dirs)

if __name__ == '__main__':
	main()