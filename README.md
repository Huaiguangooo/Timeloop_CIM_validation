# CIM Implementation Based on Timeloop

This project implements a CIM (Compute-In-Memory) architecture based on Timeloop.

## Usage

To run the CIM implementation, execute the following command:

```bash
bash ./run.sh
```

The detailed output files will be generated in the output directory, and a summarized result will be output to the terminal.

## Configuration

You can adjust the CIM parameters in the ```config.py``` file. Please note that currently, this is a simple implementation that only supports cases where the weight matrix size and CIM array dimensions (rows and columns) are the same.

## Notes

- You have to install Timeloop first.

- Implementing a bit-serial MAC (Multiply-Accumulate) operation is quite complex, and since Timeloop may not support this kind of parameter adjustment (it might still use the typical full-word multiplication), this implementation simulates the process by loading the data into the CIM array in a M * data_width format.

- The total theoretical computation cycle is assumed to be the number of cycles required to multiplying the data_width with the number of GEMV operations (also the number of rows in the input matrix), which corresponds to the result of timeloop simulation.

- For simplicity, this model does not include the cycle needed to load data from SRAM 6T cells into the CIM compute units. However, we can add this cycle later for more accurate simulations if required.