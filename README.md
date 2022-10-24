# sar_adc_energy
Modeling energy for different SAR ADC switching schemes.


This repository presents Python models for calculation of voltage and energy in capacitive DAC topologies used in Charge Redistribution (CR) Successive Approximation Register(SAR) ADCs.

## Usage

See *theory.pdf* for the math behind the models.

Clone the repository, pip install the packages from *requirements.txt* and run *simulate.py*.
The simulation script compares the energy models contained in the directory *models* and plots their *energy* x *output code* behavior, as below.

![plot](https://raw.githubusercontent.com/taimurrabuske/sar_adc_energy/main/doc/plot.png)
