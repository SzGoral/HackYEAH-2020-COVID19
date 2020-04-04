import scipy.io as sio
import logging


def parse(filename):
    """Parse pattern files from retinal experiments"""

    file_contents = sio.loadmat(filename)

    pattern = file_contents['Pattern']

    electrodes, amps = [], []
    for electrode in pattern[0]:
        electrodes.append(electrode[0][0, 0])
        amps.append(electrode[1][0])

    min_amps = [min(amp_list) for amp_list in amps]

    return {'electrodes': electrodes, 'amp': min_amps}


if __name__ == '__main__':
    print(parse('/home/szgoral/magisterka/testdata/2015-09-23-3/data001/pattern_files/pattern129_m17.mat'))
    print(parse('/home/szgoral/magisterka/testdata/2015-04-14-0/data001/pattern_files/pattern26_m189.mat'))
