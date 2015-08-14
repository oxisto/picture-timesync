#!/usr/bin/env python
import tempfile
import shutil
import glob
import os
import exifread
import sys
import pyexiv2
import datetime

src_dir = sys.argv[1]
minutes = float(sys.argv[2])

print "Scanning directory %s..." % src_dir

shift = datetime.timedelta(0, seconds)

print "Shifting %s seconds..." % shift

for path in glob.iglob(os.path.join(src_dir, '*.jpg')):
	metadata = pyexiv2.ImageMetadata(path)
	metadata.read()
	
	date = metadata["Exif.Photo.DateTimeOriginal"].value
	basename = os.path.basename(path)
	rr = basename.split("-")
	if len(rr) < 6:
		image_name = basename
	else:
		image_name = basename.split("-")[6]
		
	should_be = "%s-%s" % (date.strftime("%d-%m-%Y-%H-%M-%S"), image_name)		

	try:
		parsed_date = datetime.datetime.strptime(basename[0:19], "%d-%m-%Y-%H-%M-%S")
	except ValueError:
		print "Renaming..."
		new_path = os.path.join(src_dir, should_be)
		shutil.move(path, new_path)
		continue
		
	date += shift
	metadata["Exif.Photo.DateTimeOriginal"].value = date
	metadata["Exif.Photo.DateTimeDigitized"].value = date
	metadata.write()
	
	should_be = "%s-%s" % (date.strftime("%d-%m-%Y-%H-%M-%S"), image_name)	
			
	if not parsed_date == date:
		print "Mismatch in %s -> should be %s | %s" % (path, should_be, date - parsed_date)
		new_path = os.path.join(src_dir, should_be)
		shutil.move(path, new_path)