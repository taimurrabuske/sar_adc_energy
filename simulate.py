#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Taimur Rabuske
"""

import numpy
import matplotlib.pyplot as plt

from sar_adc_conventional import sar_adc_conventional
from sar_adc_monotonic import sar_adc_monotonic
from sar_adc_mcs import sar_adc_mcs
from sar_adc_cs import sar_adc_cs

from multiprocessing import Pool, Lock

# ADC characteristics
BITS = 10
VREF = 1.0
PTS_SIM = 2 ** BITS

MULTIPROCESSING = True  # do computations in parallel. Useful for high resolutions.
SAVE_RESULTS = False
PLOT_RESULTS = True

# declare instances of ADCs
sar_adc_conventional = sar_adc_conventional(bits=BITS, Vref=VREF, Cu=1)
sar_adc_monotonic = sar_adc_monotonic(bits=BITS, Vref=VREF, Cu=1)
sar_adc_mcs = sar_adc_mcs(bits=BITS, Vref=VREF, Cu=1)
sar_adc_cs = sar_adc_cs(bits=BITS, Vref=VREF, Cu=1)

y = numpy.linspace(-VREF, VREF, num=PTS_SIM)

print("Simulating ADCs...")


def convert_adc(zipped_args):
    adc_instance, argument = zipped_args
    result, E = adc_instance.convert(argument)
    return result, E


#####PARALELL
pool = Pool(processes=7)
if MULTIPROCESSING:
    out_conventional = pool.map(convert_adc, list(zip(len(y) * [sar_adc_conventional], y)))
    out_monotonic = pool.map(convert_adc, list(zip(len(y) * [sar_adc_monotonic], y)))
    out_mcs = pool.map(convert_adc, list(zip(len(y) * [sar_adc_mcs], y)))
    out_cs = pool.map(convert_adc, list(zip(len(y) * [sar_adc_cs], y)))
else:
    out_conventional = list(map(convert_adc, list(zip(len(y) * [sar_adc_conventional], y))))
    out_monotonic = list(map(convert_adc, list(zip(len(y) * [sar_adc_monotonic], y))))
    out_mcs = list(map(convert_adc, list(zip(len(y) * [sar_adc_mcs], y))))
    out_cs = list(map(convert_adc, list(zip(len(y) * [sar_adc_cs], y))))
out_sar_adc_conventional = numpy.transpose(out_conventional)[0]
out_sar_adc_monotonic = numpy.transpose(out_monotonic)[0]
out_sar_adc_mcs = numpy.transpose(out_mcs)[0]
out_sar_adc_split = numpy.transpose(out_mcs)[0]
out_sar_adc_cs = numpy.transpose(out_cs)[0]
E_conventional = numpy.transpose(out_conventional)[1]
E_monotonic = numpy.transpose(out_monotonic)[1]
E_mcs = numpy.transpose(out_mcs)[1]
E_cs = numpy.transpose(out_cs)[1]

if SAVE_RESULTS:
    numpy.savetxt("E_conventional.csv", E_conventional, delimiter=",")
    numpy.savetxt("E_monotonic.csv", E_monotonic, delimiter=",")
    numpy.savetxt("E_mcs.csv", E_mcs, delimiter=",")
    numpy.savetxt("E_cs.csv", E_cs, delimiter=",")

if PLOT_RESULTS:
    plt.figure(0)
    plt.suptitle("Energy comparison of SAR ADC switching schemes")
    plt.xlabel("Vin (V)")
    plt.ylabel("Dout")
    plt.subplot(211)
    plt.plot(y, out_sar_adc_conventional, label="conventional")
    plt.plot(y, out_sar_adc_monotonic, label="monotonic")
    plt.plot(y, out_sar_adc_mcs, label="MCS")
    plt.plot(y, out_sar_adc_cs, label="charge sharing")
    plt.grid(True)
    plt.legend()
    plt.xlabel("Input voltage (*Vref)")
    plt.ylabel("Output code")
    plt.subplot(212)
    plt.plot(out_sar_adc_conventional, E_conventional, label="conventional")
    plt.plot(out_sar_adc_monotonic, E_monotonic, label="monotonic")
    plt.plot(out_sar_adc_mcs, E_mcs, label="MCS")
    plt.plot(out_sar_adc_conventional, E_cs, label="charge sharing")
    plt.grid(True)
    plt.legend()
    plt.xlabel("Output Code")
    plt.ylabel("Energy (*C*Vref²)")

    plt.show()
