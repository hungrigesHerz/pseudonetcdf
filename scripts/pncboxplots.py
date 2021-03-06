#!/usr/bin/env python
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from PseudoNetCDF.coordutil import gettimes
import numpy as np
import os

def plot_boxplot(ifiles, args):
    fig = plt.figure()
    if len(args.figure_keywords) > 0:
        plt.setp(fig, **args.figure_keywords)
    sax = fig.add_subplot(111)#add_axes([.1, .15, .8, .8])
    if len(args.axes_keywords) > 0:
        plt.setp(sax, **args.axes_keywords)
    
    split = 25
    ifiles
    for target in args.variables:
        vars = [ifile.variables[target] for ifile in ifiles]
        vals = [var[:] for var in vars]
        units = [getattr(var, 'units', '') for var in vars]
        xs = range(len(vars))
        del sax.lines[:]
        del sax.collections[:]
        del sax.patches[:]
        if args.violin:
            sax.violinplot(vals, positions = xs, **args.boxkwds)
        else:
            sax.boxplot(vals, positions = xs, **args.boxkwds)
        sax.set_xticks(xs)
        sax.set_xticklabels(args.xlabels)
        #plt.setp(sax.xaxis.get_ticklabels(),rotation = 45)
        figpath = args.outpath + target + '.' + args.figformat
        fig.savefig(figpath)
        if args.verbose > 0: print('Saved fig', figpath)

if __name__ == '__main__':
    from PseudoNetCDF.pncparse import getparser, pncparse
    parser = getparser(plot_options = True, has_ofile = True)
    parser.add_argument('--violin', dest = 'violin', action = 'store_true', default = False, help = 'Use violins')
    parser.add_argument('--xlabel', dest = 'xlabels', action = 'append', default = [], help = 'Use violins')
    parser.add_argument('--box-keywords', dest = 'boxkwds', type = lambda x: eval('dict(' + x + ')'), default = dict(), help = 'Keywords for boxplot or violinplot')
    parser.epilog += """
    -----
pncviolin.py inobs inmod target [target ...]
inobs - path to obs (or other model)
inmod - path to mod (or other obs)
target - variable name
"""
    ifiles, args = pncparse(plot_options = True, has_ofile = True, parser = parser)
    xlabels = [path.replace('.nc', '') for path in args.ipath]
    if not args.xlabels is None:
        for xi, xlabel in enumerate(args.xlabels):
            xlabels[xi] = xlabel
    args.xlabels = xlabels
    plot_boxplot(ifiles, args)
