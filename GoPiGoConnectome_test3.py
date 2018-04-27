# GoPiGo Connectome
# Written by Timothy Busbice, Gabriel Garrett, Geoffrey Churchill (c) 2014, in Python 2.7
# The GoPiGo Connectome uses a Postsynaptic dictionary based on the C Elegans Connectome Model
# This application can be ran on the Raspberry Pi GoPiGo robot with a Sonar that represents Nose Touch when activated
# To run standalone without a GoPiGo robot, simply comment out the sections with Start and End comments
# Modifications by Charles Hamilton
## Start Comment
from gopigo import *
## End Comment

##IMPORT CAH - dictionary library
import connectlib

#IMPORT CAH - process and system functions
import subprocess
import os
import sys


# The postsynaptic dictionary contains the accumulated weighted values as the
# connectome is executed
postsynaptic = {}

global thisState
global nextState
thisState = 0
nextState = 1

# The Threshold is the maximum sccumulated value that must be exceeded before
# the Neurite will fire
threshold = 30

# Accumulators are used to decide the value to send to the Left and Right motors
# of the GoPiGo robot
accumleft = 0
accumright = 0

# Used to remove from Axon firing since muscles cannot fire.
muscles = ['MVU', 'MVL', 'MDL', 'MVR', 'MDR']

# Used to accumulate muscle weighted values in body muscles 07-23 = worm locomotion
musDleft = ['MDL07', 'MDL08', 'MDL09', 'MDL10', 'MDL11', 'MDL12', 'MDL13', 'MDL14', 'MDL15', 'MDL16', 'MDL17', 'MDL18', 'MDL19', 'MDL20', 'MDL21', 'MDL22', 'MDL23']
musVleft = ['MVL07', 'MVL08', 'MVL09', 'MVL10', 'MVL11', 'MVL12', 'MVL13', 'MVL14', 'MVL15', 'MVL16', 'MVL17', 'MVL18', 'MVL19', 'MVL20', 'MVL21', 'MVL22', 'MVL23']
musDright = ['MDR07', 'MDR08', 'MDR09', 'MDR10', 'MDR11', 'MDR12', 'MDR13', 'MDR14', 'MDR15', 'MDR16', 'MDR17', 'MDR18', 'MDR19', 'MDR20', 'MDL21', 'MDR22', 'MDR23']
musVright = ['MVR07', 'MVR08', 'MVR09', 'MVR10', 'MVR11', 'MVR12', 'MVR13', 'MVR14', 'MVR15', 'MVR16', 'MVR17', 'MVR18', 'MVR19', 'MVR20', 'MVL21', 'MVR22', 'MVR23']

# This is the full C Elegans Connectome as expresed in the form of the Presynatptic
# neurite and the postsynaptic neurites
# postsynaptic['ADAR'][nextState] = (2 + postsynaptic['ADAR'][thisState])
# arr=postsynaptic['AIBR'] potential optimization

# def ADAL():
#         postsynaptic['ADAR'][nextState] = 2 + postsynaptic['ADAR'][thisState]
#         postsynaptic['ADFL'][nextState] = 1 + postsynaptic['ADFL'][thisState]
#         postsynaptic['AIBL'][nextState] = 1 + postsynaptic['AIBL'][thisState]
#         postsynaptic['AIBR'][nextState] = 2 + postsynaptic['AIBR'][thisState]
#         postsynaptic['ASHL'][nextState] = 1 + postsynaptic['ASHL'][thisState]
#         postsynaptic['AVAR'][nextState] = 2 + postsynaptic['AVAR'][thisState]
#         postsynaptic['AVBL'][nextState] = 4 + postsynaptic['AVBL'][thisState]
#         postsynaptic['AVBR'][nextState] = 7 + postsynaptic['AVBR'][thisState]
#         postsynaptic['AVDL'][nextState] = 1 + postsynaptic['AVDL'][thisState]
#         postsynaptic['AVDR'][nextState] = 2 + postsynaptic['AVDR'][thisState]
#         postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
#         postsynaptic['AVJR'][nextState] = 5 + postsynaptic['AVJR'][thisState]
#         postsynaptic['FLPR'][nextState] = 1 + postsynaptic['FLPR'][thisState]
#         postsynaptic['PVQL'][nextState] = 1 + postsynaptic['PVQL'][thisState]
#         postsynaptic['RICL'][nextState] = 1 + postsynaptic['RICL'][thisState]
#         postsynaptic['RICR'][nextState] = 1 + postsynaptic['RICR'][thisState]
#         postsynaptic['RIML'][nextState] = 3 + postsynaptic['RIML'][thisState]
#         postsynaptic['RIPL'][nextState] = 1 + postsynaptic['RIPL'][thisState]
#         postsynaptic['SMDVR'][nextState] = 2 + postsynaptic['SMDVR'][thisState]
#
# def ADAR():
#         postsynaptic['ADAL'][nextState] = 1 + postsynaptic['ADAL'][thisState]
#
# def ADEL():
#         postsynaptic['ADAL'][nextState] = 1 + postsynaptic['ADAL'][thisState]
#
# def ADER():
#         postsynaptic['ADAR'][nextState] = 1 + postsynaptic['ADAR'][thisState]
#
# def ADFL():
#         postsynaptic['ADAL'][nextState] = 2 + postsynaptic['ADAL'][thisState]
#
# def ADFR():
#         postsynaptic['ADAR'][nextState] = 2 + postsynaptic['ADAR'][thisState]
#
# def ADLL():
#         postsynaptic['ADLR'][nextState] = 1 + postsynaptic['ADLR'][thisState]
#
# def ADLR():
#         postsynaptic['ADLL'][nextState] = 1 + postsynaptic['ADLL'][thisState]
#
# def AFDL():
#         postsynaptic['AFDR'][nextState] = 1 + postsynaptic['AFDR'][thisState]
#
# def AFDR():
#         postsynaptic['AFDL'][nextState] = 1 + postsynaptic['AFDL'][thisState]
#
# def AIAL():
#         postsynaptic['ADAL'][nextState] = 1 + postsynaptic['ADAL'][thisState]
#
# def AIAR():
#         postsynaptic['ADAR'][nextState] = 1 + postsynaptic['ADAR'][thisState]
#
# def AIBL():
#         postsynaptic['AFDL'][nextState] = 1 + postsynaptic['AFDL'][thisState]
#
# def AIBR():
#         postsynaptic['AFDR'][nextState] = 1 + postsynaptic['AFDR'][thisState]
#
# def AIML():
#         postsynaptic['AIAL'][nextState] = 5 + postsynaptic['AIAL'][thisState]
#
# def AIMR():
#         postsynaptic['AIAR'][nextState] = 5 + postsynaptic['AIAR'][thisState]
#
# def AINL():
#         postsynaptic['ADEL'][nextState] = 1 + postsynaptic['ADEL'][thisState]
#
# def AINR():
#         postsynaptic['AFDL'][nextState] = 4 + postsynaptic['AFDL'][thisState]
#
# def AIYL():
#         postsynaptic['AIYR'][nextState] = 1 + postsynaptic['AIYR'][thisState]
#
# def AIYR():
#         postsynaptic['ADFR'][nextState] = 1 + postsynaptic['ADFR'][thisState]
#
# def AIZL():
#         postsynaptic['AIAL'][nextState] = 3 + postsynaptic['AIAL'][thisState]
#
# def AIZR():
#         postsynaptic['AIAR'][nextState] = 1 + postsynaptic['AIAR'][thisState]

# def ALA():
#         postsynaptic['ADEL'][nextState] = 1 + postsynaptic['ADEL'][thisState]
#
# def ALML():
#         postsynaptic['AVDR'][nextState] = 1 + postsynaptic['AVDR'][thisState]
#
# def ALMR():
#         postsynaptic['AVM'][nextState] = 1 + postsynaptic['AVM'][thisState]
#
# def ALNL():
#         postsynaptic['SAAVL'][nextState] = 3 + postsynaptic['SAAVL'][thisState]
#
# def ALNR():
#         postsynaptic['ADER'][nextState] = 1 + postsynaptic['ADER'][thisState]
#
# def AQR():
#         postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
#
# def AS1():
#         postsynaptic['AVAL'][nextState] = 3 + postsynaptic['AVAL'][thisState]

# def AS2():
#         postsynaptic['DA2'][nextState] = 1 + postsynaptic['DA2'][thisState]
#
# def AS3():
#         postsynaptic['AVAL'][nextState] = 2 + postsynaptic['AVAL'][thisState]
#
# def AS4():
#         postsynaptic['AS5'][nextState] = 1 + postsynaptic['AS5'][thisState]
#
# def AS5():
#         postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
#
# def AS6():
#         postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
#
# def AS7():
#         postsynaptic['AVAL'][nextState] = 6 + postsynaptic['AVAL'][thisState]
#
# def AS8():
#         postsynaptic['AVAL'][nextState] = 4 + postsynaptic['AVAL'][thisState]
#
# def AS9():
#         postsynaptic['AVAL'][nextState] = 4 + postsynaptic['AVAL'][thisState]
#
# def AS10():
#         postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
#
# def AS11():
#         postsynaptic['MDL21'][nextState] = 1 + postsynaptic['MDL21'][thisState]
#
# def ASEL():
#         postsynaptic['ADFR'][nextState] = 1 + postsynaptic['ADFR'][thisState]
#
# def ASER():
#         postsynaptic['AFDL'][nextState] = 1 + postsynaptic['AFDL'][thisState]
#
# def ASGL():
#         postsynaptic['AIAL'][nextState] = 9 + postsynaptic['AIAL'][thisState]

# def ASGR():
#         postsynaptic['AIAR'][nextState] = 10 + postsynaptic['AIAR'][thisState]
#
# def ASHL():
#         postsynaptic['ADAL'][nextState] = 2 + postsynaptic['ADAL'][thisState]
#
# def ASHR():
#         postsynaptic['ADAR'][nextState] = 3 + postsynaptic['ADAR'][thisState]
#
# def ASIL():
#         postsynaptic['AIAL'][nextState] = 2 + postsynaptic['AIAL'][thisState]
#
# def ASIR():
#         postsynaptic['AIAL'][nextState] = 1 + postsynaptic['AIAL'][thisState]
#
# def ASJL():
#         postsynaptic['ASJR'][nextState] = 1 + postsynaptic['ASJR'][thisState]
#
# def ASJR():
#         postsynaptic['ASJL'][nextState] = 1 + postsynaptic['ASJL'][thisState]
#
# def ASKL():
#         postsynaptic['AIAL'][nextState] = 11 + postsynaptic['AIAL'][thisState]
#
# def ASKR():
#         postsynaptic['AIAR'][nextState] = 11 + postsynaptic['AIAR'][thisState]
#
# def AUAL():
#         postsynaptic['AINR'][nextState] = 1 + postsynaptic['AINR'][thisState]
#
# def AUAR():
#         postsynaptic['AINL'][nextState] = 1 + postsynaptic['AINL'][thisState]
#
# def AVAL():
#         postsynaptic['AS1'][nextState] = 3 + postsynaptic['AS1'][thisState]
#
# def AVAR():
#         postsynaptic['ADER'][nextState] = 1 + postsynaptic['ADER'][thisState]
#
# def AVBL():
#         postsynaptic['AQR'][nextState] = 1 + postsynaptic['AQR'][thisState]
#
# def AVBR():
#         postsynaptic['AS1'][nextState] = 1 + postsynaptic['AS1'][thisState]
#
# def AVDL():
#         postsynaptic['ADAR'][nextState] = 2 + postsynaptic['ADAR'][thisState]
#
# def AVDR():
#         postsynaptic['ADAL'][nextState] = 2 + postsynaptic['ADAL'][thisState]
#
# def AVEL():
#         postsynaptic['AS1'][nextState] = 1 + postsynaptic['AS1'][thisState]
#
# def AVER():
#         postsynaptic['AS1'][nextState] = 3 + postsynaptic['AS1'][thisState]
#
# def AVFL():
#         postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]

# def AVFR():
#         postsynaptic['ASJL'][nextState] = 1 + postsynaptic['ASJL'][thisState]
#
# def AVG():
#         postsynaptic['AVAR'][nextState] = 3 + postsynaptic['AVAR'][thisState]
#
# def AVHL():
#         postsynaptic['ADFR'][nextState] = 3 + postsynaptic['ADFR'][thisState]
#
# def AVHR():
#         postsynaptic['ADLL'][nextState] = 1 + postsynaptic['ADLL'][thisState]
#
# def AVJL():
#         postsynaptic['AVAL'][nextState] = 2 + postsynaptic['AVAL'][thisState]
#
# def AVJR():
#         postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]
#
# def AVKL():
#         postsynaptic['ADER'][nextState] = 1 + postsynaptic['ADER'][thisState]
#
# def AVKR():
#         postsynaptic['ADEL'][nextState] = 1 + postsynaptic['ADEL'][thisState]
#
# def AVL():
#         postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]
#
# def AVM():
#         postsynaptic['ADER'][nextState] = 1 + postsynaptic['ADER'][thisState]
#
# def AWAL():
#         postsynaptic['ADAL'][nextState] = 1 + postsynaptic['ADAL'][thisState]
#
# def AWAR():
#         postsynaptic['ADFR'][nextState] = 3 + postsynaptic['ADFR'][thisState]
#
# def AWBL():
#         postsynaptic['ADFL'][nextState] = 9 + postsynaptic['ADFL'][thisState]
#
# def AWBR():
#         postsynaptic['ADFR'][nextState] = 4 + postsynaptic['ADFR'][thisState]
#
# def AWCL():
#         postsynaptic['AIAL'][nextState] = 2 + postsynaptic['AIAL'][thisState]
#
# def AWCR():
#         postsynaptic['AIAR'][nextState] = 1 + postsynaptic['AIAR'][thisState]
#
# def BAGL():
#         postsynaptic['AIBL'][nextState] = 1 + postsynaptic['AIBL'][thisState]
#
# def BAGR():
#         postsynaptic['AIYL'][nextState] = 1 + postsynaptic['AIYL'][thisState]
#
# def BDUL():
#         postsynaptic['ADEL'][nextState] = 3 + postsynaptic['ADEL'][thisState]
#
# def BDUR():
#         postsynaptic['ADER'][nextState] = 1 + postsynaptic['ADER'][thisState]
#
# def CEPDL():
#         postsynaptic['AVER'][nextState] = 5 + postsynaptic['AVER'][thisState]
#
# def CEPDR():
#         postsynaptic['AVEL'][nextState] = 6 + postsynaptic['AVEL'][thisState]
#
# def CEPVL():
#         postsynaptic['ADLL'][nextState] = 1 + postsynaptic['ADLL'][thisState]
#
# def CEPVR():
#         postsynaptic['ASGR'][nextState] = 1 + postsynaptic['ASGR'][thisState]
#
# def DA1():
#         postsynaptic['AVAL'][nextState] = 2 + postsynaptic['AVAL'][thisState]
#
# def DA2():
#         postsynaptic['AS2'][nextState] = 2 + postsynaptic['AS2'][thisState]
#
# def DA3():
#         postsynaptic['AS4'][nextState] = 2 + postsynaptic['AS4'][thisState]
#
# def DA4():
#         postsynaptic['AVAL'][nextState] = 3 + postsynaptic['AVAL'][thisState]

# def DA5():
#         postsynaptic['AS6'][nextState] = 2 + postsynaptic['AS6'][thisState]
#
# def DA6():
#         postsynaptic['AVAL'][nextState] = 10 + postsynaptic['AVAL'][thisState]
#
# def DA7():
#         postsynaptic['AVAL'][nextState] = 2 + postsynaptic['AVAL'][thisState]
#
# def DA8():
#         postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]
#
# def DA9():
#         postsynaptic['DA8'][nextState] = 1 + postsynaptic['DA8'][thisState]
#
# def DB1():
#         postsynaptic['AIBR'][nextState] = 1 + postsynaptic['AIBR'][thisState]
#
# def DB2():
#         postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
#
# def DB3():
#         postsynaptic['AS4'][nextState] = 1 + postsynaptic['AS4'][thisState]
#
# def DB4():
#         postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
#
# def DB5():
#         postsynaptic['AVAR'][nextState] = 2 + postsynaptic['AVAR'][thisState]
#
# def DB6():
#         postsynaptic['AVAL'][nextState] = 3 + postsynaptic['AVAL'][thisState]
#
# def DB7():
#         postsynaptic['AVBL'][nextState] = 2 + postsynaptic['AVBL'][thisState]
#
# def DD1():
#         postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]
#
# def DD2():
#         postsynaptic['DA3'][nextState] = 1 + postsynaptic['DA3'][thisState]
#
# def DD3():
#         postsynaptic['DD2'][nextState] = 2 + postsynaptic['DD2'][thisState]
#
# def DD4():
#         postsynaptic['DD3'][nextState] = 1 + postsynaptic['DD3'][thisState]
#
# def DD5():
#         postsynaptic['MDL17'][nextState] = -7 + postsynaptic['MDL17'][thisState]
#
# def DD6():
#         postsynaptic['MDL19'][nextState] = -7 + postsynaptic['MDL19'][thisState]
#
# def DVA():
#         postsynaptic['AIZL'][nextState] = 3 + postsynaptic['AIZL'][thisState]
#
# def DVB():
#         postsynaptic['AS9'][nextState] = 7 + postsynaptic['AS9'][thisState]
#
# def DVC():
#         postsynaptic['AIBL'][nextState] = 2 + postsynaptic['AIBL'][thisState]
#
# def FLPL():
#         postsynaptic['ADEL'][nextState] = 2 + postsynaptic['ADEL'][thisState]
#
# def FLPR():
#         postsynaptic['ADER'][nextState] = 1 + postsynaptic['ADER'][thisState]
#
# def HSNL():
#         postsynaptic['AIAL'][nextState] = 1 + postsynaptic['AIAL'][thisState]
#
# def HSNR():
#         postsynaptic['AIBL'][nextState] = 1 + postsynaptic['AIBL'][thisState]
#
# def I1L():
#         postsynaptic['I1R'][nextState] = 1 + postsynaptic['I1R'][thisState]
#
# def I1R():
#         postsynaptic['I1L'][nextState] = 1 + postsynaptic['I1L'][thisState]
#
# def I2L():
#         postsynaptic['I1L'][nextState] = 1 + postsynaptic['I1L'][thisState]
#
# def I2R():
#         postsynaptic['I1L'][nextState] = 1 + postsynaptic['I1L'][thisState]

# def I3():
#         postsynaptic['M1'][nextState] = 4 + postsynaptic['M1'][thisState]
#
# def I4():
#         postsynaptic['I2L'][nextState] = 5 + postsynaptic['I2L'][thisState]
#
# def I5():
#         postsynaptic['I1L'][nextState] = 4 + postsynaptic['I1L'][thisState]
#
# def I6():
#         postsynaptic['I2L'][nextState] = 2 + postsynaptic['I2L'][thisState]
#
# def IL1DL():
#         postsynaptic['IL1DR'][nextState] = 1 + postsynaptic['IL1DR'][thisState]
#
# def IL1DR():
#         postsynaptic['IL1DL'][nextState] = 1 + postsynaptic['IL1DL'][thisState]
#
# def IL1L():
#         postsynaptic['AVER'][nextState] = 2 + postsynaptic['AVER'][thisState]
#
# def IL1R():
#         postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]

# def IL1VL():
#         postsynaptic['IL1L'][nextState] = 2 + postsynaptic['IL1L'][thisState]
#
# def IL1VR():
#         postsynaptic['IL1R'][nextState] = 2 + postsynaptic['IL1R'][thisState]
#
# def IL2DL():
#         postsynaptic['AUAL'][nextState] = 1 + postsynaptic['AUAL'][thisState]
#
# def IL2DR():
#         postsynaptic['CEPDR'][nextState] = 1 + postsynaptic['CEPDR'][thisState]

# def IL2L():
#         postsynaptic['ADEL'][nextState] = 2 + postsynaptic['ADEL'][thisState]
#
# def IL2R():
#         postsynaptic['ADER'][nextState] = 1 + postsynaptic['ADER'][thisState]
#
# def IL2VL():
#         postsynaptic['BAGR'][nextState] = 1 + postsynaptic['BAGR'][thisState]
#
# def IL2VR():
#         postsynaptic['IL1VR'][nextState] = 6 + postsynaptic['IL1VR'][thisState]
#
# def LUAL():
#         postsynaptic['AVAL'][nextState] = 6 + postsynaptic['AVAL'][thisState]
#
# def LUAR():
#         postsynaptic['AVAL'][nextState] = 3 + postsynaptic['AVAL'][thisState]
#
# def M1():
#         postsynaptic['I2L'][nextState] = 2 + postsynaptic['I2L'][thisState]
#
# def M2L():
#         postsynaptic['I1L'][nextState] = 3 + postsynaptic['I1L'][thisState]
#
# def M2R():
#         postsynaptic['I1L'][nextState] = 3 + postsynaptic['I1L'][thisState]
#
# def M3L():
#         postsynaptic['I1L'][nextState] = 4 + postsynaptic['I1L'][thisState]
#
# def M3R():
#         postsynaptic['I1L'][nextState] = 4 + postsynaptic['I1L'][thisState]
#
# def M4():
#         postsynaptic['I3'][nextState] = 1 + postsynaptic['I3'][thisState]
#
# def M5():
#         postsynaptic['I5'][nextState] = 3 + postsynaptic['I5'][thisState]
#
# def MCL():
#         postsynaptic['I1L'][nextState] = 3 + postsynaptic['I1L'][thisState]
#
# def MCR():
#         postsynaptic['I1L'][nextState] = 3 + postsynaptic['I1L'][thisState]
#
# def MI():
#         postsynaptic['I1L'][nextState] = 1 + postsynaptic['I1L'][thisState]
#
# def NSML():
#         postsynaptic['I1L'][nextState] = 1 + postsynaptic['I1L'][thisState]
#
# def NSMR():
#         postsynaptic['I1L'][nextState] = 2 + postsynaptic['I1L'][thisState]
#
# def OLLL():
#         postsynaptic['AVER'][nextState] = 21 + postsynaptic['AVER'][thisState]
#
# def OLLR():
#         postsynaptic['AVEL'][nextState] = 16 + postsynaptic['AVEL'][thisState]
#
# def OLQDL():
#         postsynaptic['CEPDL'][nextState] = 1 + postsynaptic['CEPDL'][thisState]

# def OLQDR():
#         postsynaptic['CEPDR'][nextState] = 2 + postsynaptic['CEPDR'][thisState]

# def OLQVL():
#         postsynaptic['ADLL'][nextState] = 1 + postsynaptic['ADLL'][thisState]

# def OLQVR():
#         postsynaptic['CEPVR'][nextState] = 1 + postsynaptic['CEPVR'][thisState]

# def PDA():
#         postsynaptic['AS11'][nextState] = 1 + postsynaptic['AS11'][thisState]

# def PDB():
#         postsynaptic['AS11'][nextState] = 2 + postsynaptic['AS11'][thisState]

# def PDEL():
#         postsynaptic['AVKL'][nextState] = 6 + postsynaptic['AVKL'][thisState]

# def PDER():
#         postsynaptic['AVKL'][nextState] = 16 + postsynaptic['AVKL'][thisState]

# def PHAL():
#         postsynaptic['AVDR'][nextState] = 1 + postsynaptic['AVDR'][thisState]

# def PHAR():
#         postsynaptic['AVG'][nextState] = 3 + postsynaptic['AVG'][thisState]

# def PHBL():
#         postsynaptic['AVAL'][nextState] = 9 + postsynaptic['AVAL'][thisState]

# def PHBR():
#         postsynaptic['AVAL'][nextState] = 7 + postsynaptic['AVAL'][thisState]

# def PHCL():
#         postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]

# def PHCR():
#         postsynaptic['AVHR'][nextState] = 1 + postsynaptic['AVHR'][thisState]

# def PLML():
#         postsynaptic['HSNL'][nextState] = 1 + postsynaptic['HSNL'][thisState]
#
# def PLMR():
#         postsynaptic['AS6'][nextState] = 1 + postsynaptic['AS6'][thisState]

# def PLNL():
#         postsynaptic['SAADL'][nextState] = 5 + postsynaptic['SAADL'][thisState]
#
# def PLNR():
#         postsynaptic['SAADR'][nextState] = 4 + postsynaptic['SAADR'][thisState]
#
# def PQR():
#         postsynaptic['AVAL'][nextState] = 8 + postsynaptic['AVAL'][thisState]

'# def PVCL():
#         postsynaptic['AS1'][nextState] = 1 + postsynaptic['AS1'][thisState]

# def PVCR():
#         postsynaptic['AQR'][nextState] = 1 + postsynaptic['AQR'][thisState]

# def PVDL():
#         postsynaptic['AVAL'][nextState] = 6 + postsynaptic['AVAL'][thisState]

# def PVDR():
#         postsynaptic['AVAL'][nextState] = 6 + postsynaptic['AVAL'][thisState]

'# def PVM():
#         postsynaptic['AVKL'][nextState] = 11 + postsynaptic['AVKL'][thisState]

# def PVNL():
#         postsynaptic['AVAL'][nextState] = 2 + postsynaptic['AVAL'][thisState]

# def PVNR():
#         postsynaptic['AVAL'][nextState] = 2 + postsynaptic['AVAL'][thisState]

# def PVPL():
#         postsynaptic['ADAL'][nextState] = 1 + postsynaptic['ADAL'][thisState]

# def PVPR():
#         postsynaptic['ADFR'][nextState] = 1 + postsynaptic['ADFR'][thisState]

# def PVQL():
#         postsynaptic['ADAL'][nextState] = 1 + postsynaptic['ADAL'][thisState]

# def PVQR():
#         postsynaptic['ADAR'][nextState] = 1 + postsynaptic['ADAR'][thisState]

# def PVR():
#         postsynaptic['ADAL'][nextState] = 1 + postsynaptic['ADAL'][thisState]

# def PVT():
#         postsynaptic['AIBL'][nextState] = 3 + postsynaptic['AIBL'][thisState]

# def PVWL():
#         postsynaptic['AVJL'][nextState] = 1 + postsynaptic['AVJL'][thisState]

# def PVWR():
#         postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]

# def RIAL():
#         postsynaptic['CEPVL'][nextState] = 1 + postsynaptic['CEPVL'][thisState]

# def RIAR():
#         postsynaptic['CEPVR'][nextState] = 1 + postsynaptic['CEPVR'][thisState]

# def RIBL():
#         postsynaptic['AIBR'][nextState] = 2 + postsynaptic['AIBR'][thisState]

# def RIBR():
#         postsynaptic['AIBL'][nextState] = 1 + postsynaptic['AIBL'][thisState]

# def RICL():
#         postsynaptic['ADAR'][nextState] = 1 + postsynaptic['ADAR'][thisState]

# def RICR():
#         postsynaptic['ADAR'][nextState] = 1 + postsynaptic['ADAR'][thisState]

# def RID():
#         postsynaptic['ALA'][nextState] = 1 + postsynaptic['ALA'][thisState]

# def RIFL():
#         postsynaptic['ALML'][nextState] = 2 + postsynaptic['ALML'][thisState]

# def RIFR():
#         postsynaptic['ASHR'][nextState] = 2 + postsynaptic['ASHR'][thisState]

# def RIGL():
#         postsynaptic['AIBR'][nextState] = 3 + postsynaptic['AIBR'][thisState]

# def RIGR():
#         postsynaptic['AIBL'][nextState] = 3 + postsynaptic['AIBL'][thisState]

# def RIH():
#         postsynaptic['ADFR'][nextState] = 1 + postsynaptic['ADFR'][thisState]

# def RIML():
#         postsynaptic['AIBR'][nextState] = 1 + postsynaptic['AIBR'][thisState]
#
# def RIMR():
#         postsynaptic['ADAR'][nextState] = 1 + postsynaptic['ADAR'][thisState]

#
# def RIPL():
#         postsynaptic['OLQDL'][nextState] = 1 + postsynaptic['OLQDL'][thisState]
#
# def RIPR():
#         postsynaptic['OLQDL'][nextState] = 1 + postsynaptic['OLQDL'][thisState]
#
# def RIR():
#         postsynaptic['AFDR'][nextState] = 1 + postsynaptic['AFDR'][thisState]

# def RIS():
#         postsynaptic['AIBR'][nextState] = 1 + postsynaptic['AIBR'][thisState]
#
# def RIVL():
#         postsynaptic['AIBL'][nextState] = 1 + postsynaptic['AIBL'][thisState]

# def RIVR():
#         postsynaptic['AIBR'][nextState] = 1 + postsynaptic['AIBR'][thisState]

# def RMDDL():
#         postsynaptic['MDR01'][nextState] = 1 + postsynaptic['MDR01'][thisState]

# def RMDDR():
#         postsynaptic['MDL01'][nextState] = 1 + postsynaptic['MDL01'][thisState]

# def RMDL():
#         postsynaptic['MDL03'][nextState] = 1 + postsynaptic['MDL03'][thisState]

# def RMDR():
#         postsynaptic['AVKL'][nextState] = 1 + postsynaptic['AVKL'][thisState]

# def RMDVL():
#         postsynaptic['AVER'][nextState] = 1 + postsynaptic['AVER'][thisState]

# def RMDVR():
#         postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]

# def RMED():
#         postsynaptic['IL1VL'][nextState] = 1 + postsynaptic['IL1VL'][thisState]

# def RMEL():
#         postsynaptic['MDR01'][nextState] = -5 + postsynaptic['MDR01'][thisState]

# def RMER():
#         postsynaptic['MDL01'][nextState] = -7 + postsynaptic['MDL01'][thisState]

# def RMEV():
#         postsynaptic['AVEL'][nextState] = 1 + postsynaptic['AVEL'][thisState]

# def RMFL():
#         postsynaptic['AVKL'][nextState] = 4 + postsynaptic['AVKL'][thisState]

# def RMFR():
#         postsynaptic['AVKL'][nextState] = 3 + postsynaptic['AVKL'][thisState]

# def RMGL():
#         postsynaptic['ADAL'][nextState] = 1 + postsynaptic['ADAL'][thisState]

# def RMGR():
#         postsynaptic['ADAR'][nextState] = 1 + postsynaptic['ADAR'][thisState]

# def RMHL():
#         postsynaptic['MDR01'][nextState] = 2 + postsynaptic['MDR01'][thisState]

# def RMHR():
#         postsynaptic['MDL01'][nextState] = 2 + postsynaptic['MDL01'][thisState]

# def SAADL():
#         postsynaptic['AIBL'][nextState] = 1 + postsynaptic['AIBL'][thisState]

# def SAADR():
#         postsynaptic['AIBR'][nextState] = 1 + postsynaptic['AIBR'][thisState]

# def SAAVL():
#         postsynaptic['AIBL'][nextState] = 1 + postsynaptic['AIBL'][thisState]
#
# def SAAVR():
#         postsynaptic['AVAR'][nextState] = 13 + postsynaptic['AVAR'][thisState]

# def SABD():
#         postsynaptic['AVAL'][nextState] = 4 + postsynaptic['AVAL'][thisState]

# def SABVL():
#         postsynaptic['AVAR'][nextState] = 3 + postsynaptic['AVAR'][thisState]

# def SABVR():
#         postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]

# def SDQL():
#         postsynaptic['ALML'][nextState] = 2 + postsynaptic['ALML'][thisState]

# def SDQR():
#         postsynaptic['ADLL'][nextState] = 1 + postsynaptic['ADLL'][thisState]

# def SIADL():
#         postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]
#
# def SIADR():
#         postsynaptic['RIBR'][nextState] = 1 + postsynaptic['RIBR'][thisState]
#
# def SIAVL():
#         postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]
#
# def SIAVR():
#         postsynaptic['RIBR'][nextState] = 1 + postsynaptic['RIBR'][thisState]
#
# def SIBDL():
#         postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]

# def SIBDR():
#         postsynaptic['AIML'][nextState] = 1 + postsynaptic['AIML'][thisState]

# def SIBVL():
#         postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]

# def SIBVR():
#         postsynaptic['RIBL'][nextState] = 1 + postsynaptic['RIBL'][thisState]

# def SMBDL():
#         postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]

# def SMBDR():
#         postsynaptic['ALNL'][nextState] = 1 + postsynaptic['ALNL'][thisState]

# def SMBVL():
#         postsynaptic['MVL01'][nextState] = 1 + postsynaptic['MVL01'][thisState]

# def SMBVR():
#         postsynaptic['AVKL'][nextState] = 1 + postsynaptic['AVKL'][thisState]

# def SMDDL():
#         postsynaptic['MDL04'][nextState] = 1 + postsynaptic['MDL04'][thisState]

# def SMDDR():
#         postsynaptic['MDL04'][nextState] = 1 + postsynaptic['MDL04'][thisState]

# def SMDVL():
#         postsynaptic['MVL03'][nextState] = 1 + postsynaptic['MVL03'][thisState]

# def SMDVR():
#         postsynaptic['MVL02'][nextState] = 1 + postsynaptic['MVL02'][thisState]

# def URADL():
#         postsynaptic['IL1DL'][nextState] = 2 + postsynaptic['IL1DL'][thisState]

# def URADR():
#         postsynaptic['IL1DR'][nextState] = 1 + postsynaptic['IL1DR'][thisState]

# def URAVL():
#         postsynaptic['MVL01'][nextState] = 2 + postsynaptic['MVL01'][thisState]

# def URAVR():
#         postsynaptic['IL1R'][nextState] = 1 + postsynaptic['IL1R'][thisState]

# def URBL():
#         postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]

# def URBR():
#         postsynaptic['ADAR'][nextState] = 1 + postsynaptic['ADAR'][thisState]

# def URXL():
#         postsynaptic['ASHL'][nextState] = 1 + postsynaptic['ASHL'][thisState]

# def URXR():
#         postsynaptic['AUAR'][nextState] = 4 + postsynaptic['AUAR'][thisState]

# def URYDL():
#         postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]

# def URYDR():
#         postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]

# def URYVL():
#         postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]

# def URYVR():
#         postsynaptic['AVAL'][nextState] = 2 + postsynaptic['AVAL'][thisState]

# def VA1():
#         postsynaptic['AVAL'][nextState] = 3 + postsynaptic['AVAL'][thisState]

# def VA2():
#         postsynaptic['AVAL'][nextState] = 5 + postsynaptic['AVAL'][thisState]

# def VA3():
#         postsynaptic['AS1'][nextState] = 1 + postsynaptic['AS1'][thisState]

# def VA4():
#         postsynaptic['AS2'][nextState] = 2 + postsynaptic['AS2'][thisState]

# def VA5():
#         postsynaptic['AS3'][nextState] = 2 + postsynaptic['AS3'][thisState]

# def VA6():
#         postsynaptic['AVAL'][nextState] = 6 + postsynaptic['AVAL'][thisState]

# def VA7():
#         postsynaptic['AS5'][nextState] = 1 + postsynaptic['AS5'][thisState]

# def VA8():
#         postsynaptic['AS6'][nextState] = 1 + postsynaptic['AS6'][thisState]

# def VA9():
#         postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]

# def VA10():
#         postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]

# def VA11():
#         postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]

# def VA12():
#         postsynaptic['AS11'][nextState] = 2 + postsynaptic['AS11'][thisState]

# def VB1():
#         postsynaptic['AIBR'][nextState] = 1 + postsynaptic['AIBR'][thisState]

# def VB2():
#         postsynaptic['AVBL'][nextState] = 3 + postsynaptic['AVBL'][thisState]

# def VB3():
#         postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]

# def VB4():
#         postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]

# def VB5():
#         postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]
#
# def VB6():
#         postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]

# def VB7():
#         postsynaptic['AVBL'][nextState] = 2 + postsynaptic['AVBL'][thisState]

# def VB8():
#         postsynaptic['AVBL'][nextState] = 7 + postsynaptic['AVBL'][thisState]

# def VB9():
#         postsynaptic['AVAL'][nextState] = 5 + postsynaptic['AVAL'][thisState]

# def VB10():
#         postsynaptic['AVBL'][nextState] = 2 + postsynaptic['AVBL'][thisState]

# def VB11():
#         postsynaptic['AVBL'][nextState] = 2 + postsynaptic['AVBL'][thisState]

# def VC1():
#         postsynaptic['AVL'][nextState] = 2 + postsynaptic['AVL'][thisState]

# def VC2():
#         postsynaptic['DB4'][nextState] = 1 + postsynaptic['DB4'][thisState]

# def VC3():
#         postsynaptic['AVL'][nextState] = 1 + postsynaptic['AVL'][thisState]

# def VC4():
#         postsynaptic['AVBL'][nextState] = 1 + postsynaptic['AVBL'][thisState]

# def VC5():
#         postsynaptic['AVFL'][nextState] = 1 + postsynaptic['AVFL'][thisState]

# def VC6():
#         postsynaptic['MVULVA'][nextState] = 1 + postsynaptic['MVULVA'][thisState]
#
# def VD1():
#         postsynaptic['DD1'][nextState] = 5 + postsynaptic['DD1'][thisState]

# def VD2():
#         postsynaptic['AS1'][nextState] = 1 + postsynaptic['AS1'][thisState]

# def VD3():
#         postsynaptic['MVL09'][nextState] = -7 + postsynaptic['MVL09'][thisState]

# def VD4():
#         postsynaptic['DD2'][nextState] = 2 + postsynaptic['DD2'][thisState]

# def VD5():
#         postsynaptic['AVAR'][nextState] = 1 + postsynaptic['AVAR'][thisState]

# def VD6():
#         postsynaptic['AVAL'][nextState] = 1 + postsynaptic['AVAL'][thisState]

# def VD7():
#         postsynaptic['MVL15'][nextState] = -7 + postsynaptic['MVL15'][thisState]

# def VD8():
#         postsynaptic['DD4'][nextState] = 2 + postsynaptic['DD4'][thisState]
#
# def VD9():
#         postsynaptic['MVL17'][nextState] = -10 + postsynaptic['MVL17'][thisState]

# def VD10():
#         postsynaptic['AVBR'][nextState] = 1 + postsynaptic['AVBR'][thisState]

# def VD11():
#         postsynaptic['AVAR'][nextState] = 2 + postsynaptic['AVAR'][thisState]

# def VD12():
#         postsynaptic['MVL19'][nextState] = -5 + postsynaptic['MVL19'][thisState]

# def VD13():
#         postsynaptic['AVAR'][nextState] = 2 + postsynaptic['AVAR'][thisState]
#
# def createpostsynaptic():
#         # The PostSynaptic dictionary maintains the accumulated values for
#         # each neuron and muscle. The Accumulated values are initialized to Zero
#         postsynaptic['ADAL'] = [0,0]
#         postsynaptic['ADAR'] = [0,0]
#         postsynaptic['ADEL'] = [0,0]
#         postsynaptic['ADER'] = [0,0]
#         postsynaptic['ADFL'] = [0,0]
#         postsynaptic['ADFR'] = [0,0]
#         postsynaptic['ADLL'] = [0,0]
#         postsynaptic['ADLR'] = [0,0]
#         postsynaptic['AFDL'] = [0,0]
#         postsynaptic['AFDR'] = [0,0]
#         postsynaptic['AIAL'] = [0,0]
#         postsynaptic['AIAR'] = [0,0]
#         postsynaptic['AIBL'] = [0,0]
#         postsynaptic['AIBR'] = [0,0]
#         postsynaptic['AIML'] = [0,0]
#         postsynaptic['AIMR'] = [0,0]
#         postsynaptic['AINL'] = [0,0]
#         postsynaptic['AINR'] = [0,0]
#         postsynaptic['AIYL'] = [0,0]
#         postsynaptic['AIYR'] = [0,0]
#         postsynaptic['AIZL'] = [0,0]
#         postsynaptic['AIZR'] = [0,0]
#         postsynaptic['ALA'] = [0,0]
#         postsynaptic['ALML'] = [0,0]
#         postsynaptic['ALMR'] = [0,0]
#         postsynaptic['ALNL'] = [0,0]
#         postsynaptic['ALNR'] = [0,0]
#         postsynaptic['AQR'] = [0,0]
#         postsynaptic['AS1'] = [0,0]
#         postsynaptic['AS10'] = [0,0]
#         postsynaptic['AS11'] = [0,0]
#         postsynaptic['AS2'] = [0,0]
#         postsynaptic['AS3'] = [0,0]
#         postsynaptic['AS4'] = [0,0]
#         postsynaptic['AS5'] = [0,0]
#         postsynaptic['AS6'] = [0,0]
#         postsynaptic['AS7'] = [0,0]
#         postsynaptic['AS8'] = [0,0]
#         postsynaptic['AS9'] = [0,0]
#         postsynaptic['ASEL'] = [0,0]
#         postsynaptic['ASER'] = [0,0]
#         postsynaptic['ASGL'] = [0,0]
#         postsynaptic['ASGR'] = [0,0]
#         postsynaptic['ASHL'] = [0,0]
#         postsynaptic['ASHR'] = [0,0]
#         postsynaptic['ASIL'] = [0,0]
#         postsynaptic['ASIR'] = [0,0]
#         postsynaptic['ASJL'] = [0,0]
#         postsynaptic['ASJR'] = [0,0]
#         postsynaptic['ASKL'] = [0,0]
#         postsynaptic['ASKR'] = [0,0]
#         postsynaptic['AUAL'] = [0,0]
#         postsynaptic['AUAR'] = [0,0]
#         postsynaptic['AVAL'] = [0,0]
#         postsynaptic['AVAR'] = [0,0]
#         postsynaptic['AVBL'] = [0,0]
#         postsynaptic['AVBR'] = [0,0]
#         postsynaptic['AVDL'] = [0,0]
#         postsynaptic['AVDR'] = [0,0]
#         postsynaptic['AVEL'] = [0,0]
#         postsynaptic['AVER'] = [0,0]
#         postsynaptic['AVFL'] = [0,0]
#         postsynaptic['AVFR'] = [0,0]
#         postsynaptic['AVG'] = [0,0]
#         postsynaptic['AVHL'] = [0,0]
#         postsynaptic['AVHR'] = [0,0]
#         postsynaptic['AVJL'] = [0,0]
#         postsynaptic['AVJR'] = [0,0]
#         postsynaptic['AVKL'] = [0,0]
#         postsynaptic['AVKR'] = [0,0]
#         postsynaptic['AVL'] = [0,0]
#         postsynaptic['AVM'] = [0,0]
#         postsynaptic['AWAL'] = [0,0]
#         postsynaptic['AWAR'] = [0,0]
#         postsynaptic['AWBL'] = [0,0]
#         postsynaptic['AWBR'] = [0,0]
#         postsynaptic['AWCL'] = [0,0]
#         postsynaptic['AWCR'] = [0,0]
#         postsynaptic['BAGL'] = [0,0]
#         postsynaptic['BAGR'] = [0,0]
#         postsynaptic['BDUL'] = [0,0]
#         postsynaptic['BDUR'] = [0,0]
#         postsynaptic['CEPDL'] = [0,0]
#         postsynaptic['CEPDR'] = [0,0]
#         postsynaptic['CEPVL'] = [0,0]
#         postsynaptic['CEPVR'] = [0,0]
#         postsynaptic['DA1'] = [0,0]
#         postsynaptic['DA2'] = [0,0]
#         postsynaptic['DA3'] = [0,0]
#         postsynaptic['DA4'] = [0,0]
#         postsynaptic['DA5'] = [0,0]
#         postsynaptic['DA6'] = [0,0]
#         postsynaptic['DA7'] = [0,0]
#         postsynaptic['DA8'] = [0,0]
#         postsynaptic['DA9'] = [0,0]
#         postsynaptic['DB1'] = [0,0]
#         postsynaptic['DB2'] = [0,0]
#         postsynaptic['DB3'] = [0,0]
#         postsynaptic['DB4'] = [0,0]
#         postsynaptic['DB5'] = [0,0]
#         postsynaptic['DB6'] = [0,0]
#         postsynaptic['DB7'] = [0,0]
#         postsynaptic['DD1'] = [0,0]
#         postsynaptic['DD2'] = [0,0]
#         postsynaptic['DD3'] = [0,0]
#         postsynaptic['DD4'] = [0,0]
#         postsynaptic['DD5'] = [0,0]
#         postsynaptic['DD6'] = [0,0]
#         postsynaptic['DVA'] = [0,0]
#         postsynaptic['DVB'] = [0,0]
#         postsynaptic['DVC'] = [0,0]
#         postsynaptic['FLPL'] = [0,0]
#         postsynaptic['FLPR'] = [0,0]
#         postsynaptic['HSNL'] = [0,0]
#         postsynaptic['HSNR'] = [0,0]
#         postsynaptic['I1L'] = [0,0]
#         postsynaptic['I1R'] = [0,0]
#         postsynaptic['I2L'] = [0,0]
#         postsynaptic['I2R'] = [0,0]
#         postsynaptic['I3'] = [0,0]
#         postsynaptic['I4'] = [0,0]
#         postsynaptic['I5'] = [0,0]
#         postsynaptic['I6'] = [0,0]
#         postsynaptic['IL1DL'] = [0,0]
#         postsynaptic['IL1DR'] = [0,0]
#         postsynaptic['IL1L'] = [0,0]
#         postsynaptic['IL1R'] = [0,0]
#         postsynaptic['IL1VL'] = [0,0]
#         postsynaptic['IL1VR'] = [0,0]
#         postsynaptic['IL2L'] = [0,0]
#         postsynaptic['IL2R'] = [0,0]
#         postsynaptic['IL2DL'] = [0,0]
#         postsynaptic['IL2DR'] = [0,0]
#         postsynaptic['IL2VL'] = [0,0]
#         postsynaptic['IL2VR'] = [0,0]
#         postsynaptic['LUAL'] = [0,0]
#         postsynaptic['LUAR'] = [0,0]
#         postsynaptic['M1'] = [0,0]
#         postsynaptic['M2L'] = [0,0]
#         postsynaptic['M2R'] = [0,0]
#         postsynaptic['M3L'] = [0,0]
#         postsynaptic['M3R'] = [0,0]
#         postsynaptic['M4'] = [0,0]
#         postsynaptic['M5'] = [0,0]
#         postsynaptic['MANAL'] = [0,0]
#         postsynaptic['MCL'] = [0,0]
#         postsynaptic['MCR'] = [0,0]
#         postsynaptic['MDL01'] = [0,0]
#         postsynaptic['MDL02'] = [0,0]
#         postsynaptic['MDL03'] = [0,0]
#         postsynaptic['MDL04'] = [0,0]
#         postsynaptic['MDL05'] = [0,0]
#         postsynaptic['MDL06'] = [0,0]
#         postsynaptic['MDL07'] = [0,0]
#         postsynaptic['MDL08'] = [0,0]
#         postsynaptic['MDL09'] = [0,0]
#         postsynaptic['MDL10'] = [0,0]
#         postsynaptic['MDL11'] = [0,0]
#         postsynaptic['MDL12'] = [0,0]
#         postsynaptic['MDL13'] = [0,0]
#         postsynaptic['MDL14'] = [0,0]
#         postsynaptic['MDL15'] = [0,0]
#         postsynaptic['MDL16'] = [0,0]
#         postsynaptic['MDL17'] = [0,0]
#         postsynaptic['MDL18'] = [0,0]
#         postsynaptic['MDL19'] = [0,0]
#         postsynaptic['MDL20'] = [0,0]
#         postsynaptic['MDL21'] = [0,0]
#         postsynaptic['MDL22'] = [0,0]
#         postsynaptic['MDL23'] = [0,0]
#         postsynaptic['MDL24'] = [0,0]
#         postsynaptic['MDR01'] = [0,0]
#         postsynaptic['MDR02'] = [0,0]
#         postsynaptic['MDR03'] = [0,0]
#         postsynaptic['MDR04'] = [0,0]
#         postsynaptic['MDR05'] = [0,0]
#         postsynaptic['MDR06'] = [0,0]
#         postsynaptic['MDR07'] = [0,0]
#         postsynaptic['MDR08'] = [0,0]
#         postsynaptic['MDR09'] = [0,0]
#         postsynaptic['MDR10'] = [0,0]
#         postsynaptic['MDR11'] = [0,0]
#         postsynaptic['MDR12'] = [0,0]
#         postsynaptic['MDR13'] = [0,0]
#         postsynaptic['MDR14'] = [0,0]
#         postsynaptic['MDR15'] = [0,0]
#         postsynaptic['MDR16'] = [0,0]
#         postsynaptic['MDR17'] = [0,0]
#         postsynaptic['MDR18'] = [0,0]
#         postsynaptic['MDR19'] = [0,0]
#         postsynaptic['MDR20'] = [0,0]
#         postsynaptic['MDR21'] = [0,0]
#         postsynaptic['MDR22'] = [0,0]
#         postsynaptic['MDR23'] = [0,0]
#         postsynaptic['MDR24'] = [0,0]
#         postsynaptic['MI'] = [0,0]
#         postsynaptic['MVL01'] = [0,0]
#         postsynaptic['MVL02'] = [0,0]
#         postsynaptic['MVL03'] = [0,0]
#         postsynaptic['MVL04'] = [0,0]
#         postsynaptic['MVL05'] = [0,0]
#         postsynaptic['MVL06'] = [0,0]
#         postsynaptic['MVL07'] = [0,0]
#         postsynaptic['MVL08'] = [0,0]
#         postsynaptic['MVL09'] = [0,0]
#         postsynaptic['MVL10'] = [0,0]
#         postsynaptic['MVL11'] = [0,0]
#         postsynaptic['MVL12'] = [0,0]
#         postsynaptic['MVL13'] = [0,0]
#         postsynaptic['MVL14'] = [0,0]
#         postsynaptic['MVL15'] = [0,0]
#         postsynaptic['MVL16'] = [0,0]
#         postsynaptic['MVL17'] = [0,0]
#         postsynaptic['MVL18'] = [0,0]
#         postsynaptic['MVL19'] = [0,0]
#         postsynaptic['MVL20'] = [0,0]
#         postsynaptic['MVL21'] = [0,0]
#         postsynaptic['MVL22'] = [0,0]
#         postsynaptic['MVL23'] = [0,0]
#         postsynaptic['MVR01'] = [0,0]
#         postsynaptic['MVR02'] = [0,0]
#         postsynaptic['MVR03'] = [0,0]
#         postsynaptic['MVR04'] = [0,0]
#         postsynaptic['MVR05'] = [0,0]
#         postsynaptic['MVR06'] = [0,0]
#         postsynaptic['MVR07'] = [0,0]
#         postsynaptic['MVR08'] = [0,0]
#         postsynaptic['MVR09'] = [0,0]
#         postsynaptic['MVR10'] = [0,0]
#         postsynaptic['MVR11'] = [0,0]
#         postsynaptic['MVR12'] = [0,0]
#         postsynaptic['MVR13'] = [0,0]
#         postsynaptic['MVR14'] = [0,0]
#         postsynaptic['MVR15'] = [0,0]
#         postsynaptic['MVR16'] = [0,0]
#         postsynaptic['MVR17'] = [0,0]
#         postsynaptic['MVR18'] = [0,0]
#         postsynaptic['MVR19'] = [0,0]
#         postsynaptic['MVR20'] = [0,0]
#         postsynaptic['MVR21'] = [0,0]
#         postsynaptic['MVR22'] = [0,0]
#         postsynaptic['MVR23'] = [0,0]
#         postsynaptic['MVR24'] = [0,0]
#         postsynaptic['MVULVA'] = [0,0]
#         postsynaptic['NSML'] = [0,0]
#         postsynaptic['NSMR'] = [0,0]
#         postsynaptic['OLLL'] = [0,0]
#         postsynaptic['OLLR'] = [0,0]
#         postsynaptic['OLQDL'] = [0,0]
#         postsynaptic['OLQDR'] = [0,0]
#         postsynaptic['OLQVL'] = [0,0]
#         postsynaptic['OLQVR'] = [0,0]
#         postsynaptic['PDA'] = [0,0]
#         postsynaptic['PDB'] = [0,0]
#         postsynaptic['PDEL'] = [0,0]
#         postsynaptic['PDER'] = [0,0]
#         postsynaptic['PHAL'] = [0,0]
#         postsynaptic['PHAR'] = [0,0]
#         postsynaptic['PHBL'] = [0,0]
#         postsynaptic['PHBR'] = [0,0]
#         postsynaptic['PHCL'] = [0,0]
#         postsynaptic['PHCR'] = [0,0]
#         postsynaptic['PLML'] = [0,0]
#         postsynaptic['PLMR'] = [0,0]
#         postsynaptic['PLNL'] = [0,0]
#         postsynaptic['PLNR'] = [0,0]
#         postsynaptic['PQR'] = [0,0]
#         postsynaptic['PVCL'] = [0,0]
#         postsynaptic['PVCR'] = [0,0]
#         postsynaptic['PVDL'] = [0,0]
#         postsynaptic['PVDR'] = [0,0]
#         postsynaptic['PVM'] = [0,0]
#         postsynaptic['PVNL'] = [0,0]
#         postsynaptic['PVNR'] = [0,0]
#         postsynaptic['PVPL'] = [0,0]
#         postsynaptic['PVPR'] = [0,0]
#         postsynaptic['PVQL'] = [0,0]
#         postsynaptic['PVQR'] = [0,0]
#         postsynaptic['PVR'] = [0,0]
#         postsynaptic['PVT'] = [0,0]
#         postsynaptic['PVWL'] = [0,0]
#         postsynaptic['PVWR'] = [0,0]
#         postsynaptic['RIAL'] = [0,0]
#         postsynaptic['RIAR'] = [0,0]
#         postsynaptic['RIBL'] = [0,0]
#         postsynaptic['RIBR'] = [0,0]
#         postsynaptic['RICL'] = [0,0]
#         postsynaptic['RICR'] = [0,0]
#         postsynaptic['RID'] = [0,0]
#         postsynaptic['RIFL'] = [0,0]
#         postsynaptic['RIFR'] = [0,0]
#         postsynaptic['RIGL'] = [0,0]
#         postsynaptic['RIGR'] = [0,0]
#         postsynaptic['RIH'] = [0,0]
#         postsynaptic['RIML'] = [0,0]
#         postsynaptic['RIMR'] = [0,0]
#         postsynaptic['RIPL'] = [0,0]
#         postsynaptic['RIPR'] = [0,0]
#         postsynaptic['RIR'] = [0,0]
#         postsynaptic['RIS'] = [0,0]
#         postsynaptic['RIVL'] = [0,0]
#         postsynaptic['RIVR'] = [0,0]
#         postsynaptic['RMDDL'] = [0,0]
#         postsynaptic['RMDDR'] = [0,0]
#         postsynaptic['RMDL'] = [0,0]
#         postsynaptic['RMDR'] = [0,0]
#         postsynaptic['RMDVL'] = [0,0]
#         postsynaptic['RMDVR'] = [0,0]
#         postsynaptic['RMED'] = [0,0]
#         postsynaptic['RMEL'] = [0,0]
#         postsynaptic['RMER'] = [0,0]
#         postsynaptic['RMEV'] = [0,0]
#         postsynaptic['RMFL'] = [0,0]
#         postsynaptic['RMFR'] = [0,0]
#         postsynaptic['RMGL'] = [0,0]
#         postsynaptic['RMGR'] = [0,0]
#         postsynaptic['RMHL'] = [0,0]
#         postsynaptic['RMHR'] = [0,0]
#         postsynaptic['SAADL'] = [0,0]
#         postsynaptic['SAADR'] = [0,0]
#         postsynaptic['SAAVL'] = [0,0]
#         postsynaptic['SAAVR'] = [0,0]
#         postsynaptic['SABD'] = [0,0]
#         postsynaptic['SABVL'] = [0,0]
#         postsynaptic['SABVR'] = [0,0]
#         postsynaptic['SDQL'] = [0,0]
#         postsynaptic['SDQR'] = [0,0]
#         postsynaptic['SIADL'] = [0,0]
#         postsynaptic['SIADR'] = [0,0]
#         postsynaptic['SIAVL'] = [0,0]
#         postsynaptic['SIAVR'] = [0,0]
#         postsynaptic['SIBDL'] = [0,0]
#         postsynaptic['SIBDR'] = [0,0]
#         postsynaptic['SIBVL'] = [0,0]
#         postsynaptic['SIBVR'] = [0,0]
#         postsynaptic['SMBDL'] = [0,0]
#         postsynaptic['SMBDR'] = [0,0]
#         postsynaptic['SMBVL'] = [0,0]
#         postsynaptic['SMBVR'] = [0,0]
#         postsynaptic['SMDDL'] = [0,0]
#         postsynaptic['SMDDR'] = [0,0]
#         postsynaptic['SMDVL'] = [0,0]
#         postsynaptic['SMDVR'] = [0,0]
#         postsynaptic['URADL'] = [0,0]
#         postsynaptic['URADR'] = [0,0]
#         postsynaptic['URAVL'] = [0,0]
#         postsynaptic['URAVR'] = [0,0]
#         postsynaptic['URBL'] = [0,0]
#         postsynaptic['URBR'] = [0,0]
#         postsynaptic['URXL'] = [0,0]
#         postsynaptic['URXR'] = [0,0]
#         postsynaptic['URYDL'] = [0,0]
#         postsynaptic['URYDR'] = [0,0]
#         postsynaptic['URYVL'] = [0,0]
#         postsynaptic['URYVR'] = [0,0]
#         postsynaptic['VA1'] = [0,0]
#         postsynaptic['VA10'] = [0,0]
#         postsynaptic['VA11'] = [0,0]
#         postsynaptic['VA12'] = [0,0]
#         postsynaptic['VA2'] = [0,0]
#         postsynaptic['VA3'] = [0,0]
#         postsynaptic['VA4'] = [0,0]
#         postsynaptic['VA5'] = [0,0]
#         postsynaptic['VA6'] = [0,0]
#         postsynaptic['VA7'] = [0,0]
#         postsynaptic['VA8'] = [0,0]
#         postsynaptic['VA9'] = [0,0]
#         postsynaptic['VB1'] = [0,0]
#         postsynaptic['VB10'] = [0,0]
#         postsynaptic['VB11'] = [0,0]
#         postsynaptic['VB2'] = [0,0]
#         postsynaptic['VB3'] = [0,0]
#         postsynaptic['VB4'] = [0,0]
#         postsynaptic['VB5'] = [0,0]
#         postsynaptic['VB6'] = [0,0]
#         postsynaptic['VB7'] = [0,0]
#         postsynaptic['VB8'] = [0,0]
#         postsynaptic['VB9'] = [0,0]
#         postsynaptic['VC1'] = [0,0]
#         postsynaptic['VC2'] = [0,0]
#         postsynaptic['VC3'] = [0,0]
#         postsynaptic['VC4'] = [0,0]
#         postsynaptic['VC5'] = [0,0]
#         postsynaptic['VC6'] = [0,0]
#         postsynaptic['VD1'] = [0,0]
#         postsynaptic['VD10'] = [0,0]
#         postsynaptic['VD11'] = [0,0]
#         postsynaptic['VD12'] = [0,0]
#         postsynaptic['VD13'] = [0,0]
#         postsynaptic['VD2'] = [0,0]
#         postsynaptic['VD3'] = [0,0]
#         postsynaptic['VD4'] = [0,0]
#         postsynaptic['VD5'] = [0,0]
#         postsynaptic['VD6'] = [0,0]
#         postsynaptic['VD7'] = [0,0]
#         postsynaptic['VD8'] = [0,0]
#         postsynaptic['VD9'] = [0,0]

#global postsynapticNext = copy.deepcopy(postsynaptic)

def motorcontrol():
        global accumright
        global accumleft

        # accumulate left and right muscles and the accumulated values are
        # used to move the left and right motors of the robot
        for pscheck in postsynaptic:
                if pscheck in musDleft or pscheck in musVleft:
                   accumleft += postsynaptic[pscheck][thisState]
                   postsynaptic[pscheck][thisState] = 0                 #Both states have to be set to 0 once the muscle is fired, or
                   #postsynaptic[pscheck][nextState] = 0                 # it will keep returning beyond the threshold within one iteration.
                elif pscheck in musDright or pscheck in musVright:
                   accumright += postsynaptic[pscheck][thisState]
                   postsynaptic[pscheck][thisState] = 0
                   #postsynaptic[pscheck][nextState] = 0
        # We turn the wheels according to the motor weight accumulation
        new_speed = abs(accumleft) + abs(accumright)
        if new_speed > 150:
                new_speed = 150
        elif new_speed < 75:
                new_speed = 75
        print "Left: ", accumleft, "Right:", accumright, "Speed: ", new_speed
        ## Start Commented section
        set_speed(new_speed)
        if accumleft == 0 and accumright == 0:
                stop()
        elif accumright <= 0 and accumleft < 0:
                set_speed(150)
                turnratio = float(accumright) / float(accumleft)
                # print "Turn Ratio: ", turnratio
                if turnratio <= 0.6:
                         left_rot()
                         time.sleep(0.8)
                elif turnratio >= 2:
                         right_rot()
                         time.sleep(0.8)
                bwd()
                time.sleep(0.5)
        elif accumright <= 0 and accumleft >= 0:
                right_rot()
                time.sleep(.8)
        elif accumright >= 0 and accumleft <= 0:
                left_rot()
                time.sleep(.8)
        elif accumright >= 0 and accumleft > 0:
                turnratio = float(accumright) / float(accumleft)
                # print "Turn Ratio: ", turnratio
                if turnratio <= 0.6:
                         left_rot()
                         time.sleep(0.8)
                elif turnratio >= 2:
                         right_rot()
                         time.sleep(0.8)
                fwd()
                time.sleep(0.5)
        else:
                stop()
         ## End Commented section
        accumleft = 0
        accumright = 0
        time.sleep(0.5)


def dendriteAccumulate(dneuron):
        f = eval(dneuron)
        f()

def fireNeuron(fneuron):
        # The threshold has been exceeded and we fire the neurite
        if fneuron != "MVULVA":
                f = eval(fneuron)
                f()

def runconnectome():
        # Each time a set of neurons is stimulated, this method will execute
        # The weighted values are accumulated in the PostSynaptic array
        # Once the accumulation is read, we see what neurons are greater
        # than the threshold and fire the neuron or muscle that has exceeded
        # the threshold
        global thisState
        global nextState
        for ps in postsynaptic:
                if ps[:3] not in muscles and abs(postsynaptic[ps][thisState]) > threshold:
                        fireNeuron(ps)
                        postsynaptic[ps] = [0,0]
        motorcontrol()
        thisState,nextState=nextState,thisState


# Create the dictionary
createpostsynaptic()
dist=0
set_speed(120)
print "Voltage: ", volt()
tfood = 0
try:
### Here is where you would put in a method to stimulate the neurons ###
### We stimulate chemosensory neurons constantly unless nose touch   ###
### (sonar) is stimulated and then we fire nose touch neurites       ###
### Use CNTRL-C to stop the program
    while True:
        ## Start comment - use a fixed value if you want to stimulte nose touch
        ## use something like "dist = 27" if you want to stop nose stimulation
        dist = us_dist(15)
        ## End Comment

        #Do we need to switch states at the end of each loop? No, this is done inside the runconnectome()
        #function, called inside each loop.
        if dist>0 and dist<30:
            print "OBSTACLE (Nose Touch)", dist

##CAH EDITS
            worm1 = "/home/pi/GoPiGo/worm1.wav"
            devnull = open("/dev/null","w")
            subprocess.call(["aplay",  worm1],stderr=devnull)

## Original code
            dendriteAccumulate("FLPR")
            dendriteAccumulate("FLPL")
            dendriteAccumulate("ASHL")
            dendriteAccumulate("ASHR")
            dendriteAccumulate("IL1VL")
            dendriteAccumulate("IL1VR")
            dendriteAccumulate("OLQDL")
            dendriteAccumulate("OLQDR")
            dendriteAccumulate("OLQVR")
            dendriteAccumulate("OLQVL")
            runconnectome()
        else:
            if tfood < 2:
                    print "FOOD"
                    print (thisState)
## CAH EDITS
                    food1 = "/home/pi/GoPiGo/food1.wav"
                    devnull = open("/dev/null","w")
                    subprocess.call(["aplay",  food1],stderr=devnull)
## Original code
                    dendriteAccumulate("ADFL")
                    dendriteAccumulate("ADFR")
                    dendriteAccumulate("ASGR")
                    dendriteAccumulate("ASGL")
                    dendriteAccumulate("ASIL")
                    dendriteAccumulate("ASIR")
                    dendriteAccumulate("ASJR")
                    dendriteAccumulate("ASJL")
                    runconnectome()
                    time.sleep(0.5)
            tfood += 0.5
            if (tfood > 20):
                    tfood = 0



except KeyboardInterrupt:
    ## Start Comment
    stop()
    ## End Comment
    print "Ctrl+C detected. Program Stopped!"
    for pscheck in postsynaptic:
        print (pscheck,' ',postsynaptic[pscheck][0],' ',postsynaptic[pscheck][1])
