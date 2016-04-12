#!/usr/bin/env python
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from PseudoNetCDF.coordutil import gettimes
import numpy as np
import os

def plot_diurnal_box(ifiles, args):
    times = [gettimes(ifile) for ifile in ifiles]
    fig = plt.figure()
    sax = fig.add_subplot(111)#add_axes([.1, .15, .8, .8])
    sax.set_xlabel('Time (UTC)')
    split = 25
    for target in args.variables:
        vars = [ifile.variables[target] for ifile in ifiles]
        unit = getattr(vars[0], 'units', 'unknown')
        sax.set_ylabel(target + '(' + unit + ')')
        del sax.lines[:]
        nvars = len(vars)
        varwidth = .8/nvars/1.1
        po = np.arange(24) + 0.1 + varwidth/2
        for vi, (time, var) in enumerate(zip(times, vars)):
            color = plt.get_cmap()((vi + .5)/float(nvars))
            vardesc = getattr(var, 'description', None)
            varb = sax.plot(time, var[:], color = color, label = vardesc)
        #plt.setp(sax.xaxis.get_ticklabels(),rotation = 45)
        plt.legend()
        figpath = args.outpath + target + '_ts.png'
        fig.savefig(figpath)
        print figpath

if __name__ == '__main__':
    from PseudoNetCDF.pncparse import getparser, pncparse
    parser = getparser(plot_options = True, has_ofile = True)
    parser.epilog += """
    -----
box.py inobs inmod target [target ...]
inobs - path to obs
inmod - path to mod
target - variable name
"""
    ifiles, args = pncparse(plot_options = True, has_ofile = True, parser = parser)
    plot_diurnal_box(ifiles, args)