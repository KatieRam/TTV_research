#!/bin/env python

# Katie's Code for Transit Time Variations

import numpy as np
import math as math
import pandas as pd
import os
import subprocess



t=4300
ins= "1.00000000      0.000003003     365.3     0.0      1.57079637      -1.57079637   0.0    3.0     0.000945792    {}  0.0    1.57079637    -1.57079637    0.0    5.0".format(t)
f = open('input.txt','w')
f.write(ins)
f.close()

subprocess.run(["predict_formula", "2", "input.txt", "0", "10000", "6", "output.Earth_Jupiter"])
   
#Data for planets 'b' and 'c'

list0 = []
list1 = []
list2 = []


#with open('output.{}','r'.format(t)) as file:
with open("output.Earth_Jupiter","r") as file:
   for row in file:
      a,b,c = row.split()
      list0.append(a)
      list1.append(b)
      list2.append(c)
       
   transit_number_b = []
   transit_time_b = []
   transit_number_c = []
   transit_time_c = []
       
   for i in range(0,len(list0)):
      if (list0[i]=='0'):
         transit_number_b.append(list1[i])
         transit_time_b.append(list2[i])
      if (list0[i]=='1'):
         transit_number_c.append(list1[i])
         transit_time_c.append(list2[i])
           
     # print(transit_time_b)
     # print(list0)

##PLANET B

#<X> Average Transit # (0,1,2,...,N)

   xb=0

#<Y> average time

   yb=0
   xyb=0
   x2b=0
   nb = len(transit_number_b)
   for i in range(0,len(transit_number_b)):
      xb = xb + float(transit_number_b[i])
      yb = yb + float(transit_time_b[i])
      xyb = xyb + float(transit_number_b[i])*float(transit_time_b[i])
      x2b = x2b + float(transit_number_b[i])**2
   xb = xb/nb
   yb = yb/nb
   xyb = xyb
   x2b = x2b
     # print(xb)
     # print(x2b)

#These are 'a' and 'b' from linear fit Y=aX+b

   a_b = (xyb - nb*xb*yb)/(x2b-nb*xb**2)
   b_b = (x2b*yb-xyb*xb)/(x2b-nb*xb**2)
      #print(a_b)
      #print(b_b)

##PLANET C

#<X> Average Transit # (0,1,2,...,N)

   xc=0

#<Y> average time

   yc=0
   xyc=0
   x2c=0
   nc = len(transit_number_c)
   for i in range(0,len(transit_number_c)):
      xc = xc + float(transit_number_c[i])
      yc = yc + float(transit_time_c[i])
      xyc = xyc + float(transit_number_c[i])*float(transit_time_c[i])
      x2c = x2c + float(transit_number_c[i])**2
   xc = xc/nc
   yc = yc/nc
   xyc = xyc
   x2c = x2c
     # print(x2c)

#These are 'a' and 'b' from the linear fit Y=aX+b

   a_c = (xyc - nc*xc*yc)/(x2c-nc*xc**2)
   b_c = (x2c*yc-xyc*xc)/(x2c-nc*xc**2)
      #print(a_c)
      #print(b_c)

##Calculate and difference in Observed for Planet B

#'C_b' is Calculated time Y for planet b
   C_b = np.zeros(len(transit_number_b))

#'O_C_b' is Observed/simulated transit time for planet b
   O_C_b = np.zeros(len(transit_number_b))

   for i in range(0,len(transit_number_b)):
      C_b[i] = a_b*i+b_b
      O_C_b[i] = (float(transit_time_b[i]) - C_b[i])*24.0*60.0
    
      #print(O_C_b)

##Calculate and difference in Observed for Planet C

#'C_c' is Calculated time y for planet c
   C_c = np.zeros(len(transit_number_c))

#'O_C_c is Observed/simulated transit time for planet c
   O_C_c = np.zeros(len(transit_number_c))

   for i in range(0,len(transit_number_c)):
      C_c[i] = a_c*i+b_c
      O_C_c[i] = (float(transit_time_c[i]) - C_c[i])*24.0*60.0
    
      #print(O_C_c)

#get_ipython().magic('matplotlib inline')

   import matplotlib.pyplot as plt
   plt.figure(i) 
   plt.plot(C_b,O_C_b,'o',markersize = 5)
   plt.xlabel('time (days)')
   plt.ylabel('TTV (min)')
   plt.savefig("graph_Earth_Jupiter.jpg".format(t))
#plt.show()

   MAX_inner = max(O_C_b)
   MAX_outer = max(O_C_c)

   P_inner = 10;
   P_outer = t;

   P_syn = abs(1/P_inner - 1/P_outer)
   print(P_syn)

   P_super = abs(1/P_inner - 3/P_outer)
   print(P_super)

   print('Max',MAX_inner,'  ',MAX_outer)
   



