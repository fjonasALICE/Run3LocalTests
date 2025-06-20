#!/bin/bash
# outputname=LHC24ar_PbPb_EMCalCF_TimeShift
# python3 runO2Analysis.py --output=/alf/data/flo/Run3LocalTests/Output/${outputname} --configuration=/alf/data/flo/Run3LocalTests/Input/LHC24ar_PbPb_EMCalCF --nFilesPerJob=5 --partition=long

# Track QA
outputname=LHC25a2_JJTest
python3 runO2Analysis.py --output=${PWD}/Output/${outputname} --configuration=${PWD}/Input/LHC25a2_JJMC_GammaJet --nFilesPerJob=5
