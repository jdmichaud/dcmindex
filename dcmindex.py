#!/usr/bin/env python

import os
import sys

import pydicom

# Recursively walk the directory tree starting from path and returns a generator
# that yield the filename.
def walk(path):
  import os
  for dirName, subdirList, fileList in os.walk(path):
    for filename in fileList:
      yield os.path.join(dirName, filename)
    for subdir in subdirList:
      walk(subdir)

def main(argv):
  if len(argv) != 2:
    print('error: missing path')
    print('usage: ./dcmindex.py /path/to/index')
    sys.exit(1)

  pathToIndex = argv[1]
  print('Modality,PhotometricInterpretation,PixelRepresentation,BitsAllocated,BitsStored,Rows,Columns,NumberOfFrames,RescaleType,ModalityLUTSequence,VOILUTFunction,VOILUTSequence,TransferSyntaxUID,PatientName,SOPInstanceUID,filename')
  for file in walk(pathToIndex):
    if pydicom.misc.is_dicom(file):
      ds = pydicom.dcmread(file)
      Modality = ds.get('Modality', 'not present')
      PhotometricInterpretation = ds.get('PhotometricInterpretation', 'not present')
      PixelRepresentation = ds.get('PixelRepresentation', 'not present')
      BitsAllocated = ds.get('BitsAllocated', 'not present')
      BitsStored = ds.get('BitsStored', 'not present')
      Rows = ds.get('Rows', 'not present')
      Columns = ds.get('Columns', 'not present')
      Rows = ds.get('Rows', 'not present')
      NumberOfFrames = ds.get('NumberOfFrames', 0) > 1
      RescaleType = ds.get('RescaleType', 'not present')
      ModalityLUTSequence = 'yes' if 'ModalityLUTSequence' in ds else 'not present'
      VOILUTFunction = ds.get('VOILUTFunction', 'not present')
      VOILUTSequence = 'yes' if 'VOILUTSequence' in ds else 'not present'
      PatientName = ds.get('PatientName', 'not present')
      TransferSyntaxUID = ds.file_meta.get('TransferSyntaxUID', 'not present')
      SOPInstanceUID = ds.file_meta.get('SOPInstanceUID', 'not present')
      filename = file[len(pathToIndex):]
      print(f'{Modality},{PhotometricInterpretation},{PixelRepresentation},{BitsAllocated},{BitsStored},{Rows},{Columns},{NumberOfFrames},{RescaleType},{ModalityLUTSequence},{VOILUTFunction},{VOILUTSequence},{TransferSyntaxUID},{PatientName},{SOPInstanceUID},{filename}')

if __name__ == '__main__':
  main(sys.argv)

