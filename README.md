# Optimal design of sero surveys 

The worst case design can be obtained by running the script:

```shell
python3 main.py 
```
which uses `optimization/yin_yang.py` to get the optimization for the worst case-design proposed in Theorem  2.

In addition to the optimization methods, the `main.py` script also allows users to enter custom inputs using the following input flags:

input flag| description
---|---|
-C | specify total budget
-cRAT | cost of one RAT test
-cRTPCR | cost of one RT-PCR Test
-cIGG | cost of one IGG test

The following snippet is an example for a complete input arguments supplied to the python script

```shell
python main.py -C 10000 -cRAT 0.5 -cRTPCR 0.1 -cIGG 0.45 
```


## Citation
If you are using this code, please consider citing the paper
```bibtex
@misc{athreya2020covid19,
      title={COVID-19: Optimal Design of Serosurveys for Disease Burden Estimation}, 
      author={Siva Athreya and Giridhara R. Babu and Aniruddha Iyer and Mohammed Minhaas B. S. and Nihesh Rathod and Sharad Shriram and Rajesh Sundaresan and Nidhin Koshy Vaidhiyan and Sarath Yasodharan},
      year={2020},
      eprint={2012.12135},
      archivePrefix={arXiv},
      primaryClass={stat.AP}
}
```

## License
The source code is publicly available under the Apache2 license terms.
Copyrights for the work belongs to the Indian Institute of Science Bangalore, Indian Statistical Institute Bangalore Centre, Indian Institute of Public Health Bangalore and Strand Life Sciences, Bangalore.
