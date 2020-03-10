from tkinter import *
from tkinter.filedialog import askdirectory
import glob
import os
from collections import defaultdict




class FormattedScanlist():
    def __init__(self, scan_n = 2, workPath = None):

        self.scan_n = scan_n

        self.workPath = askdirectory() if workPath is None else workPath
        
    def _getBlock(self, scanLists):
        frames = {'diffNum':[], 'diffName':[]}


        for v in scanLists.values():
            frames['diffNum'].append(len(v))
            frames['diffName'].append('>'.join(v))

        block = {'filenum':[], 'filenames':[]}
        """
        {'filenum': [4, 3], 'filenames': ['191106-K2-2 V6-IL-Ag-Ir-Pd-Pt-Ru_400_deg_001.gfrm>191106-K2-2
        """
        index = 0
        while index <= len(frames['diffNum']):
            filenum = min([len(frames['diffNum'])-index, self.scan_n])
            block['filenum'].append(filenum)
            s = '>'.join([v for v in frames['diffName'][index:filenum+index]])
            ss =  ' '.join(['"{}"'.format(c) for c in s.split('>')])
            block['filenames'].append(ss)
            index += self.scan_n
        return block
        
    def _scanLists(self):

        files = glob.glob(os.path.join(self.workPath, '*.gfrm'))

        #sorted file names in a given directory
        filenames = sorted([os.path.basename(f) for f in files])
        scanLists = defaultdict(list)
        for f in filenames:
            scanLists[f[0:-8]].append(f)
        return scanLists
        

    def frames(self):
        scanLists = self._scanLists()
        frames = {'diffNum':[], 'diffName':[]}
        for v in scanLists.values():
            frames['diffNum'].append(len(v))
            frames['diffName'].append(' '.join(['"{}"'.format(c) for c in v]))
        return frames
        


