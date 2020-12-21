# Optimal Design of sero surveys 
This repository contains the source code for the paper titled, "*COVID-19: Optimal Design of Serosurveys for Disease Burden Estimation*".

The full-text article is available on [platform](#)

The code is written mostly in Python with a few R code and have been used to get the results reported in Table 3. The required packages for the python scripts are mentioned under `requirements.txt`.

It is possible for users to set the total budget for the sero study (C), along with cost for each test namely, RAT, RT-PCR and iGG antibody tests. *Note: The unit of all costs are in 1 thousand units*

The python script is used for the results obtained from Theorem 1

```shell
python main.py -m local
```
which uses `optimization/local.py` to do an optimization for a given budget $C$ and a fixed parameter $p$ proposed in Theorem 1.

The worst case design can be obtained by running the script:

```shell
python main.py -m grid
```
which uses `optimization/grid_search.py` to get the optimization for the worst case-design proposed in Theorem  2.

In addition to the optimization methods, the `main.py` script also allows users to enter custom inputs using the following input flags:

input flag| description
---|---|
-C | specify total budget
-cRAT | cost of one RAT test
-cRTPCR | cost of one RT-PCR Test
-cIGG | cost of one IGG test

The following snippet is an example for a complete input arguments supplied to the python script

```shell
python main.py -C 10000 -cRAT 0.5 -cRTPCR 0.1 -cIGG 0.45 -m grid
```



`optimization/by_symptomatics.R` is the implementation of the optimization with respect to the symptomatic fraction that are detected using the rapid antigent test, as proposed in Theorem 4.

## Citation
If you are using this code, please consider citing the paper
```bibtex

```

## License
The source code is publicly available under the Apache2 license terms.
Copyrights for the work belongs to the Indian Institute of Science Bangalore, Indian Statistical Institute Bangalore Centre and Indian Institute of Public Health Bangalore.
