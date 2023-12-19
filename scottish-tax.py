#! /usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np

class TaxBand:
    def __init__(self, lower, upper, rate):
        self.lower = lower
        self.upper = upper
        self.rate = rate


def tax_for_band(salary, band):
    if salary < band.lower:
        return 0

    return int(min(salary - band.lower, band.upper - band.lower) * band.rate)


def main():
    salary_step = 1000
    salary_range = range(1000, 250000, salary_step)

    bands = [
        TaxBand(0, 12571, 0),                   # personal_allowance
        TaxBand(12571, 14733, 0.19),            # basic_rate_threshold
        TaxBand(14733, 25689, 0.20),            # intermediate_rate_threshold
        TaxBand(25689, 43633, 0.21),            # higher_rate_threshold
        TaxBand(43633, 125140, 0.42),           # top_rate_threshold
        TaxBand(125140, float('inf'), 0.47)     # additional_rate_threshold
    ]

    pa_reduction_threshold = 100000

    ni_bands = [
        TaxBand(242 * 52, 967 * 52, 0.12),      # ni_lower_threshold
        TaxBand(967 * 52, float('inf'), 0.02)   # ni_upper_threshold
    ]

    salaries = []
    tax_rates = []
    ni_rates = []
    total_rates = []

    for salary in salary_range:
        tax = 0

        if salary >= pa_reduction_threshold:
            reduction = min(salary - pa_reduction_threshold, bands[-1].upper - pa_reduction_threshold)
            reduction = reduction // 2
            bands[0].lower -= reduction

        for i in range(len(bands)):
            tax += tax_for_band(salary, bands[i])

        ni = 0

        for i in range(len(ni_bands)):
            ni += tax_for_band(salary, ni_bands[i])

        tax_rate = (100.0 * tax) / salary
        ni_rate = (100.0 * ni) / salary

        total_tax = tax + ni
        total_rate = tax_rate + ni_rate

        take_home = salary - total_tax

        salaries.append(salary)
        tax_rates.append(tax_rate)
        ni_rates.append(ni_rate)
        total_rates.append(total_rate)

    # Plotting
    plt.figure(figsize=(10, 6))

    plt.plot(salaries, tax_rates, label='Tax Rate')
    plt.plot(salaries, ni_rates, label='NI Rate', color='orange')
    plt.plot(salaries, total_rates, label='Total Rate', color='green')

    plt.xlabel('Salary')
    plt.ylabel('Rate')
    plt.legend()

    plt.ylim(0, 50)
    plt.yticks(np.arange(0, 51, 5))
    plt.grid(axis='y', linestyle='dotted', alpha=0.5)
    plt.tight_layout()
    plt.savefig('scottish-tax.png')


if __name__ == "__main__":
    main()

