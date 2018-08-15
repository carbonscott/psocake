import json
import h5py
import psana

def getNoe(args, facility):
    if facility == 'LCLS':
        runStr = "%04d" % args.run
        access = "exp=" + args.exp + ":run=" + runStr + ':idx'
        if 'ffb' in args.access.lower(): access += ':dir=/reg/d/ffb/' + args.exp[:3] + '/' + args.exp + '/xtc'
        ds = psana.DataSource(access)
        run = ds.runs().next()
        times = run.times()
        numJobs = len(times)
    elif facility == 'PAL':
        _temp = args.dir + '/' + args.exp[:3] + '/' + args.exp + '/data/run' + str(args.run).zfill(4) + '/*.h5'
        numJobs = len(glob.glob(_temp))
    # check if the user requested specific number of events
    if args.noe > -1 and args.noe <= numJobs:
        numJobs = args.noe
    return numJobs

def str2bool(v): return v.lower() in ("yes", "true", "t", "1")

def writeStatus(fname, d):
    json.dump(d, open(fname, 'w'))

def convert_peaks_to_cheetah(s, r, c) :
    """Converts seg, row, col assuming (32,185,388)
       to cheetah 2-d table row and col (8*185, 4*388)
    """
    segs, rows, cols = (32,185,388)
    row2d = (int(s)%8) * rows + int(r) # where s%8 is a segment in quad number [0,7]
    col2d = (int(s)/8) * cols + int(c) # where s/8 is a quad number [0,3]
    return row2d, col2d

def reshapeHdf5(h5file, dataset, ind, numAppend):
    h5file[dataset].resize((ind + numAppend,))

def cropHdf5(h5file, dataset, ind):
    h5file[dataset].resize((ind,))

def updateHdf5(h5file, dataset, ind, val):
    try:
        h5file[dataset][ind] = val
    except:
        h5file[dataset][ind] = 0