# Run3LocalTests - Tool to run O2Physics analyses locally and on computing clusters

A toolkit for running ALICE O2 Physics analyses locally, designed for testing and validation of physics analysis workflows before submitting to the Grid.

## Overview

This framework provides tools for:
- Running O2 Physics analyses on local computing resources  
- Downloading data from ALICE Hyperloop infrastructure
- Managing multiple analysis configurations and input datasets
- Batch processing with job scheduling support

## Prerequisites

- ALICE O2 Physics framework installed and configured
- Valid ALICE Grid certificate and token
- Python 3.6+ with required packages:
  - `rich` for enhanced logging and progress bars
  - `pathlib` for path handling
- ALIEN tools for data access
- SLURM or compatible job scheduler (for batch processing)

## Quick Start

1. **Clone and navigate to the project:**
   ```bash
   cd Run3LocalTests
   ```

2. **Run a simple analysis:**
   ```bash
   ./start.sh
   ```

3. **Check the output:**
   ```bash
   ls Output/LHC25a2_JJTest/
   ```

## Main Components

### 1. runO2Analysis.py

The main analysis runner that handles job submission and file processing.

**Usage:**
```bash
python3 runO2Analysis.py [OPTIONS]
```

**Options:**
- `--inputfiles`: Path to input file list (default: uses inputfiles.txt in configuration directory)
- `--output`: Output directory path (required)
- `--configuration`: Configuration directory containing analysis setup files (required)
- `--nFilesPerJob`: Number of files to process per job (default: 1)
- `--debug`: Enable debug mode for local execution without job submission
- `--scheduler`: Job scheduler to use (default: sbatch)

**Example:**
```bash
python3 runO2Analysis.py \
  --output=./Output/MyAnalysis \
  --configuration=./Input/ExampleConfig \
  --nFilesPerJob=5 \
  --debug
```

### 2. downloadHyperloop.py

Tool for downloading ALICE data from the Hyperloop infrastructure.

**Usage:**
```bash
python3 downloadHyperloop.py [OPTIONS]
```

**Options:**
- `--inputfilelist`: Text file with comma-separated list of hyperloop directories
- `--outputfolder`: Local destination folder for downloaded files  
- `--filename`: Name of files to download (e.g., AO2D.root) or comma-separated list
- `--isDerived`: Whether data is derived data (affects path structure)
- `--nThreads`: Number of parallel download threads (default: 4)

**Example:**
```bash
python3 downloadHyperloop.py \
  --inputfilelist=hyperloop_dirs.txt \
  --outputfolder=./Data \
  --filename=AO2D.root \
  --nThreads=8
```

## Configuration Setup

Each analysis requires a configuration directory containing:

### Required Files:
1. **`configuration.json`**: O2 Physics analysis configuration
2. **`runcommand.sh`**: Shell script with the O2 analysis command pipeline. It has to contain the loading of the environment and also the command to run 
3. **`inputfiles.txt`**: List of input data files (one per line). Can also be path to alien or local files!
4. **`OutputDirector.json`**: Output configuration (optional)


### Example Configuration Structure:
```
Input/MyAnalysis/
├── configuration.json    # O2 analysis parameters
├── runcommand.sh        # Analysis execution pipeline
├── inputfiles.txt       # Input file paths
└── OutputDirector.json  # Output settings
```

### Sample runcommand.sh:
```bash
#!/bin/bash
#SBATCH --job-name=TrackQA
#SBATCH --partition=long

# Load O2 environment
eval `$(which alienv) -w /software/alice/sw --no-refresh printenv O2Physics/latest`

# Set ALICE Grid tokens
export JALIEN_TOKEN_CERT=/path/to/tokencert.pem
export JALIEN_TOKEN_KEY=/path/to/tokenkey.pem

# Run O2 analysis pipeline
o2-analysis-je-track-jet-qa -b --configuration json://configuration.json | \
o2-analysis-timestamp -b --configuration json://configuration.json | \
o2-analysis-event-selection -b --configuration json://configuration.json | \
o2-analysis-multiplicity-table -b --configuration json://configuration.json | \
o2-analysis-trackselection -b --configuration json://configuration.json \
--aod-file @input_data.txt
```

## Workflow Examples

### 1. Local Test Run
```bash
# Quick local test with debug mode
python3 runO2Analysis.py \
  --output=./Output/TestRun \
  --configuration=./Input/ExampleConfig \
  --nFilesPerJob=1 \
  --debug
```

### 2. Batch Production Run
```bash
# Submit jobs to SLURM cluster
python3 runO2Analysis.py \
  --output=./Output/ProductionRun \
  --configuration=./Input/LHC24ar_PbPb_EMCalCF \
  --nFilesPerJob=10 \
  --scheduler=sbatch
```

### 3. Data Download and Analysis
```bash
# 1. Download data from Hyperloop
python3 downloadHyperloop.py \
  --inputfilelist=run_directories.txt \
  --outputfolder=./RawData \
  --filename=AO2D.root \
  --nThreads=6

# 2. Create input file list
find ./RawData -name "AO2D.root" > ./Input/MyConfig/inputfiles.txt

# 3. Run analysis
python3 runO2Analysis.py \
  --output=./Output/MyAnalysis \
  --configuration=./Input/MyConfig \
  --nFilesPerJob=5
```

## Troubleshooting

### Debug Mode:
Use `--debug` flag to run locally without job submission for testing:
```bash
python3 runO2Analysis.py --debug --configuration=./Input/ExampleConfig --output=./Output/Debug
```

## Contributing

When adding new analysis configurations:
1. Create a new directory under `Input/`
2. Include all required configuration files
3. Test with debug mode before production runs
4. Document any special requirements or dependencies


## License

This project follows ALICE Collaboration software policies and guidelines.
