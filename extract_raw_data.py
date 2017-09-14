from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import tarfile
from IPython.display import display, Image
from scipy import ndimage
from sklearn.linear_model import LogisticRegression
import zipfile
import urllib
from six.moves.urllib.request import urlretrieve
from six.moves import cPickle as pickle

last_percent_reported = None

class ExtractRawData:
    def __init__(self):
        self.url = 'https://s3-us-west-2.amazonaws.com/us-office/competition/'
        self.file_list = []
        self.data_root = './dataset/'
        if not os.path.isdir(self.data_root):
            print("Dataset folder {} is not existing. Creating...".format(self.data_root))
            os.mkdir(self.data_root)

    def download_progress_hook(count, blockSize, totalSize):
        """A hook to report the progress of a download. This is mostly intended for users with
        slow internet connections. Reports every 5% change in download progress.
        """
        global last_percent_reported
        percent = int(count * blockSize * 100 / totalSize)

        if last_percent_reported != percent:
            if percent % 5 == 0:
              sys.stdout.write("%s%%" % percent)
              sys.stdout.flush()
            else:
              sys.stdout.write(".")
              sys.stdout.flush()

        last_percent_reported = percent
        
    def maybe_download(self):
    #Download a file if not present.
        dest_filename_list = []
        for filename in self.file_list:
            dest_filename = os.path.join(self.data_root, filename)
            if not os.path.exists(dest_filename):
                print('Attempting to download:', filename)

            #Copy a network object denoted by a URL to a local file, if necessary.
            #If the URL points to a local file,
            #or a valid cached copy of the object exists, the object is not copied. 
                filename, _ = urlretrieve(self.url + filename, dest_filename)
                print('\nDownload Complete!')
            print('Found and verified', dest_filename)
            dest_filename_list.append(dest_filename)
        return dest_filename_list
    
    def maybe_extract(self, force=False):
        for filename in self.file_list:
            root = os.path.join(self.data_root, os.path.splitext(os.path.splitext(filename)[0])[0])  # remove .tar.gz
            if os.path.isdir(root) and not force:
            # You may override by setting force=True.
                print('%s already present - Skipping extraction of %s.' % (root, filename))
            else:
                print('Extracting data for %s. This may take a while. Please wait.' % root)
                zip_file = zipfile.ZipFile(os.path.join(self.data_root, filename), 'r')
                sys.stdout.flush()
                #Extract all members from the archive to the current working directory or directory path.
                zip_file.extractall(self.data_root)
                zip_file.close()
                print ('File {} has been extracted at {}'.format(filename, self.data_root))

if __name__ == '__main__':
    raw_data = ExtractRawData()
    raw_data.file_list = ['training.zip','testing.zip']
    raw_data.maybe_download()
    raw_data.maybe_extract()