#
# -*- coding: latin-1 -*-
#-----------------------------------------------------
#
# OMCE error messages
#
# Author: Ruediger Kessel
#         National Institute of Standards and Technology (NIST)
#
# Disclaimer:
#
# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the
# course of their official duties. Pursuant to title 17 Section 105
# of the United States Code this software is not subject to
# copyright protection and is in the public domain. This software is
# experimental. NIST assumes no responsibility whatsoever for its
# use by other parties, and makes no guarantees, expressed or
# implied, about its quality, reliability, or any other
# characteristic. We would appreciate acknowledgement if the
# software is used.
#-----------------------------------------------------
error={}
error[  1]=["Option %s is not valid!",['<opt>']]
error[  2]=["File not found (%s)!",['<filename>']]
error[  3]=["It is not a file (%s)!",['<string>']]
error[  4]=["Format ""%s"" is not supported!",['<format>']]
error[  5]=["Option %s should be a number (%s)!",['<option>','<value>']]
error[  6]=["Option out of range (%s=%s...%s)!",['<option>','<from>','<to>']]
error[  7]=["Bin-file format ""%s"" not supported!",['<format-id>']]
error[  8]=["Bin-file %s is corrupted (%s)!",['<filename>','<details>']]
error[  9]=["No. of Runs in bin-file is zero!",[]]
error[ 10]=["Mathematical loop in process list!%s",['']]
error[ 11]=["Input quantity ""%s"" is not defined!",['<name>']]
error[ 12]=["Duplicated quantity name (%s)!" ,['<name>']]
error[ 13]=["Error in expression: %s!" ,['<expression>']]
error[ 14]=["Quantity ""%s"" in Result ""%s"" is unknown!",['<name>','<name>']]
error[ 15]=["Model Parameter ""%s"" not supported!" ,['<parameter>']]
error[ 16]=["Correlation matrix is not positive semi-definite!",[]]
error[ 17]=["Quantity name unknown in correlation entry (%s)!",['<name>']]
error[ 18]=["Correlations are not supported for non-Gaussian Quantities (%s)!",['<name>']]
error[ 19]=["Correlation coefficient out of range r(%s,%s)=%s!",['<name>','<name>','<value>']]
error[ 20]=["Matrix modification exceeds limit (-e2=%s)!",['<limit>']]
error[ 21]=["Diagonal elements of the correlation matrix must be one [r(%s,%s)=%s]!",['<name>','<name>','<value>']]
error[ 22]=["Quantity name ""%s"" is a reserved symbol!",['<name>']]
error[ 23]=["Quantity ""%s"", parameter ""%s"", syntax error in ""%s""!",['<name>','<param>','<value>']]
error[ 24]=["Parameter of function ""%s()"" is not a constant!",['<name>']]
error[ 25]=["Function ""%s"" is used without parameter!",['<name>']]
error[ 26]=["Quantity unknown for ""val(%s)""!",['<name>']]
error[ 27]=["The uncertainty for a t-distribution with dof&lt;3 is not defined in ""u(%s)""!",['<name>']]
error[ 28]=["Quantity unknown for ""u(%s)""!",['<name>']]
error[ 29]=["Grammar type not supported (%s)!",['<type-id>']]
error[ 30]=["Function ""%s()"" is used recursively in its definition!",['<name>']]
error[ 31]=["Quantity ""%s"" is defined as parameter and as global in function ""%s()""!",['<name>','<name>']]
error[ 32]=["Global quantity ""%s"" in function ""%s()"" is not defined!",['<name>','<name>']]
error[ 33]=["Quantity ""%s"" in function ""%s()"" is not defined as parameter or global!",['<name>','<name>']]
error[ 34]=["Unknown command line parameter name ""%s""!",['<name>']]
error[ 35]=["Quantity ""%s"", parameter ""%s"", value ""%s"" is not an integer!",['<name>','<param>','<value>']]
error[ 36]=["Quantity ""%s"", parameter ""%s"", parameter unknown in ""%s""!",['<name>','<param>','<value>']]
error[ 37]=["Quantity ""%s"", parameter ""%s"", %%-character is not supported (%s)!",['<name>','<param>','<value>']]
error[ 38]=["Quantity ""%s"", parameter ""%s"", syntax error in ""%s""!",['<name>','<param>','<value>']]
error[ 39]=["Quantity name ""%s"" is a predefined function!",['<name>']]
error[ 40]=["Quantity name ""%s"" is a predefined symbol!",['<name>']]
error[ 41]=["Quantity name ""%s"" is a reserved name!",['<name>']]
error[ 42]=["Quantity name ""%s"" is the name of a user defined function!",['<name>']]
error[ 43]=["Parameter name ""%s"" is a predefined function!",['<name>']]
error[ 44]=["Parameter name ""%s"" is a reserved name!",['<name>']]
error[ 45]=["Quantity ""%s"" in <Discrete> or <Import> element is unknown in the bin-file %s!",['<name>','<filename>']]
error[ 46]=["Index unknown!",[]]
error[ 47]=["Result name ""%s"" is used twice in result section!",['<name>']]
error[ 48]=["No result defined in source file!",[]]
error[ 49]=['Unknown symbol "%s" in parameter value "%s"!',['<name>','<value>']]
error[ 50]=['Unknown symbol in parameter value "%s"!',['<value>']]
error[ 51]=["Double assignment for r(%s,%s): %s and %s!",['<name>','<name>','<value>','<value>']]
error[ 52]=["A near correlation matrix could not be found in %s runs!",['<runs>']]
error[ 53]=["Function ""%s"" is used with %s parameter!",['<name>','<n>']]
error[ 54]=["Format definition file ""%s"": the line ""%s"" cannot be decoded!",['<filename>','<line>']]
error[ 55]=["Format definition header ""%s"", key ""%s"" and function ""%s"" cannot be interpretated!",['<header>','<key>','<func>']]
error[ 56]=["Less than %s %% of the simulated results are valid!",['<value>']]
error[ 57]=["The constraint for %s: %s invalidates all data!",['<name>','<expression>']]
error[ 58]=["Output File Definition not found (%s)!",['<filename>']]
error[ 59]=["Constraint for %s: %s cannot be evaluated!",['<name>','<expression>']]
error[ 60]=["Unknown command line parameter argument  ""%s""!",['<argument>']]
error[ 61]=["Parameter ""%s"" in section <Simulation> is unknown!",['<param>']]
error[ 62]=["Loop increment (Step) must be non-zero!",[]]
error[ 63]=["Parameter ""%s"" in section <Loop> is unknown!",['<param>']]
error[ 64]=["Error in %s name: %s!" ,['<element>','<text>']]
error[ 65]=["quantile estimation method is unknown for -pq=%s!" ,['<value>']]
error[ 66]=["The sub-block size -sbs=%s must be a multiple of 10!" ,['<value>']]
error[ 67]=["The block size -bs=%s must be a multiple of the sub-block size -sbs=%s!" ,['<value>','<value>']]
error[ 68]=["Result data entry '%s' unknown in ofd-file!" ,['<name>']]
error[ 69]=["Result data entry '%s' unknown in vfd-file!" ,['<name>']]
error[ 70]=["The attribute mcsimulations is not set correctly (%s)!",['<value>']]
error[ 71]=["The binary data format %s is not supported!",['<number>']]
error[ 72]=["Internal, Matrix structure does not match!",[]]
error[ 73]=["Filenames starting with \\,/ or containing .. or : are not permitted in server mode (%s)!",['<filename>']]
error[ 75]=["User dbm filename is not specified, use option --VDB=filename!",[]]
error[ 76]=['Incorrect number of parameter for "%s" command!',['<command>']]
error[ 77]=['Missing parameter for option "%s!',['<option>']]
error[ 78]=['Command "%s" unknown for --USER option!',['<command>']]
error[ 79]=['User "%s" does not exist in dbm "%s"!',['<user>','<dbm-file>']]
error[ 80]=['The user name or password must not be an empty string!',[]]
error[ 81]=['Error in quoting of string "%s"!',['<strin>']]
error[ 82]=['Amara version not supported!',[]]
error[ 83]=["Row count does not match (%s!=%s)!",['<cnt-1>','<cnt-2>']]
error[ 84]=["Col count does not match (%s!=%s)!",['<cnt-1>','<cnt-2>']]
error[ 85]=["Content Column %s, Row %s does not match (%s != %s)!",['<row>','<col>','<content-1>','<content-2>']]
error[ 86]=['Name "%s" used in Option -mark is not defined in input file!',['<name>']]
error[ 87]=['Command "%s" needs %s parameters, %s are given!',['<cmd>','<number>','<number>']]
error[ 88]=['Parameter type error (%s: %s expected)!',['<number>','<type>']]
error[ 89]=['Parameter "%s" unknown!',['<parameter>']]
error[ 90]=['End of file reached before the command was complete!',[]]
error[ 91]=['The number of pre-run blocks is too small (see option -pr)!',[]]
error[ 92]=['The value for Parameter "%s" must evaluate to an integer (%s)!',['<name>','<value>']]
error[ 93]=['The value for Parameter "%s" must evaluate to a float (%s)!',['<name>','<value>']]
error[ 94]=['The coding "%s" is unknown in function definition for %s!',['<coding>','<function>']]

error[100]=['Script raised an error!',[]]

error[250]=["(PYTHON) %s!",['<error message>']]

error[252]=["File not found (%s) on the server!",['<filename>']]
error[253]=["Path is not a file (%s) on the server!",['<string>']]
error[254]=["ConText I/O Error (%s)!",['<error message>']]
error[255]=["%s!",['<error message>']]
