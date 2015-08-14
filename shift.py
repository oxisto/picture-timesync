#!/usr/bin/env python
import shutil
import glob
import os
import sys
import pyexiv2
import datetime

src_dir = sys.argv[1]
seconds = int(sys.argv[2])

print "Scanning directory %s..." % src_dir

shift = datetime.timedelta(0, seconds)

print "Shifting %s ..." % shift

for path in glob.iglob(os.path.join(src_dir, '*.JPG')):
	metadata = pyexiv2.ImageMetadata(path)
	metadata.read()
	
	date = metadata["Exif.Photo.DateTimeOriginal"].value
	basename = os.path.basename(path)
	rr = basename.split("-")
	if len(rr) < 6:
		image_name = basename
	else:
		image_name = basename.split("-")[6]
		
	date += shift
	metadata["Exif.Photo.DateTimeOriginal"].value = date
	metadata["Exif.Photo.DateTimeDigitized"].value = date
	metadata.write()		
		
	should_be = "%s-%s" % (date.strftime("%d-%m-%Y-%H-%M-%S"), image_name)

	try:
		parsed_date = datetime.datetime.strptime(basename[0:19], "%d-%m-%Y-%H-%M-%S")
	except ValueError:
		print "Renaming..."
		new_path = os.path.join(src_dir, should_be)
		shutil.move(path, new_path)
		continue
			
	if not parsed_date == date:
		print "Mismatch in %s -> should be %s | %s" % (path, should_be, date - parsed_date)
		new_path = os.path.join(src_dir, should_be)
		shutil.move(path, new_path)