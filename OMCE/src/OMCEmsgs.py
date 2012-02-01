#
# -*- coding: latin-1 -*-
#-----------------------------------------------------
#
# OMCE standard messages
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
msg={}
msg[   1]=["%s aborted!",['<tool>']]
msg[   2]=['Warning: config file "%s" not found, option ignored',['<filename>']]
msg[   3]=['Warning: PRINT() used with non string argument of %s: ',['<type>']]
msg[   4]=['Warning: option line ""%s"" ("%s") not well formed, line is ignored',['<option>','<filename>']]
msg[   5]=['User Interrupt.',[]]
msg[   6]=['Server refuses the connection: unknown user name or password!',[]]
msg[   7]=['Warning: command file "%s" not found, option ignored',['<filename>']]
msg[   8]=['',['']]
msg[   9]=['Warning: Function is not implemented in "%s"',['<context>']]
msg[ 100]=['Warning: correlation coefficient r(%s,%s)="%s" is not a number, set to 0.0!',
          ['<name>','<name>','<value>']]
msg[ 101]=["Warning: Option -wb is ignored in client/server mode!",[]]
msg[ 102]=["Warning: Option %s is unknown and ignored!",['<option>']]
msg[ 103]=["Warning: All standard OMCE options are ignored in client/server mode!",[]]
msg[ 104]=["Starting server...",[]]
msg[ 105]=["Warning: Password is empty, user %s is ignored.",[]]
msg[ 106]=["Generate plot for %s",['<symbol>']]
msg[ 107]=["Writing plots %s to %s",['<plot numbers>','<filename>']]
msg[ 108]=['Warning: to many data for plotting, plot only the first %s data rows',['<number>']]
msg[ 109]=['Warning: command "%s" not found!',['<command>']]
msg[ 110]=['Warning "%s" will be redefined to %s!',['<name>','<value>']]
msg[ 111]=['Warning "%s" cannot be found the plotting parameters!',['<name>']]



