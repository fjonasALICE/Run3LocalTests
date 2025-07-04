# EXAMPLE: python3 runGammaJetTreeProducer.py --input=/alf/data/calorimetrees/je_derived_data/JE_LHC23zzm_pass4_Cl_8/fullInputList_AO2D.txt --output=/alf/data/calorimetrees/JE_PbPb_AO2D/000003_LHC23zzm_PbPb --configuration=/software/flo/CalorimeTree/tools/LocalRunConfigs/PbPb_JEDerived
import sys
import os
import argparse
import subprocess
import threading
import logging
import time
from pathlib import Path
from rich.logging import RichHandler
import glob

# setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)

log = logging.getLogger("rich")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converts a directory of files to a different format")
    parser.add_argument("--inputfiles", help="txt files with the input files. If not specified, then inputfiles.txt in the configuration directory will be used", default="")
    parser.add_argument("--output", help="The output directory. If empty, then inputdir/converted will be used", default="")
    parser.add_argument("--configuration", help="Folder containing the configuration files (configuration.json, OutputDirector.json and runcommand.sh)", default="")
    parser.add_argument("--nFilesPerJob", help="The number of files to convert per job", default=1)
    parser.add_argument("--debug", help="Debug mode. If enabled no job is submitted and command is run locally in shell", action="store_true", default=False)
    parser.add_argument("--scheduler", help="The scheduler to use", default="sbatch")
    args = parser.parse_args()

        # if input files 
    output_dir = args.output
    configuration_dir = args.configuration

    if not output_dir:
        log.error(f"Output directory not provided")
        sys.exit(1)
    if not configuration_dir or not Path(configuration_dir).exists():
        log.error(f"Configuration directory not provided")
        sys.exit(1)

    input_files = Path(configuration_dir) / "inputfiles.txt"
    if args.inputfiles:
        input_files = Path(args.inputfiles)
    log.info(f"Using input files {input_files}")

    # create output directory if it does not exist
    output_dir = Path(output_dir)
    if not output_dir.exists():
        log.info(f"Creating output directory {output_dir}")
        os.makedirs(output_dir)

    # read all lines in input_files txt list and split them into chunks each containing nFilesPerJob
    with open(input_files, "r") as f:
        files = f.readlines()
    files = [f.strip() for f in files]
    log.info(f"Found {len(files)} files to process")
    
    # split the files into chunks each containing nFilesPerJob
    nFilesPerJob = int(args.nFilesPerJob)
    filechunks = [files[i:i + nFilesPerJob] for i in range(0, len(files), nFilesPerJob)]
    # if debug mode, then run all files in one chunk
    if args.debug:
        log.info(f"Debug mode: Running all files in one chunk")
        filechunks = [files]
    else:
        log.info(f"Splitting files into {len(filechunks)} chunks with {nFilesPerJob} files each")
    log.info(f"Using configuration directory {configuration_dir}")

    # print the content of {configuration_dir}/runcommand.sh
    with open(Path(configuration_dir) / "runcommand.sh", "r") as f:
        log.info(f"Using runcommand.sh: {f.read()}")
    
    # loop over chunks
    for i, filechunk in enumerate(filechunks):
        log.info(f"Submitting chunk {i+1}/{len(filechunks)}: ")
        for f in filechunk:
            log.info(f"{f}")

        # create folder {i} in output_dir
        output_dir_chunk = output_dir / str(i)
        if not output_dir_chunk.exists():
            os.makedirs(output_dir_chunk)
        # copy all files in configuration_dir to output_dir_chunk
        os.system(f"cp -r {configuration_dir}/* {output_dir_chunk}")

        # write files in filechunk to {output_dir_chunk}/input_data.txt
        with open(output_dir_chunk / "input_data.txt", "w") as f:
            f.write("\n".join(filechunk))
        # submit job
        
        slurm_log = output_dir_chunk / "slurm.log"
        if args.debug:
            log.info(f"Debug mode: Skipping job submission")
            os.system(f"cd {output_dir_chunk} && bash runcommand.sh")
        else:
            os.system(f"cd {output_dir_chunk} && {args.scheduler} runcommand.sh")


        




    
    

    

