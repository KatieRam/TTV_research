#!/bin/env python

# Katie's Code for Transit Time Variations for editing

import numpy as np
import math as math
import pandas as pd
import os
import subprocess



#changing masses

E=2
for p in range(0,E):
    print(p)
    if p == 0:
        x = 0.50
    else:
       x=2.0

    print(x)

    N=1100
    M=11
    TTV = np.zeros(N)
    Pouter = np.zeros(N)
    for i in range(0,N):
       t = (11 + i*M/N)
       ins= "{}     0.00001     10     0.0      1.57079637      -1.57079637   0.0    3.0     0.00001    {}  -0.002    1.57079637    -1.57079637    0.0    5.0".format(x,t)
       f = open('input.txt','w')
       f.write(ins)
       f.close()


       subprocess.run(["predict_formula", "2", "input.txt", "0", "5000", "6", "sun/output.{}_{}.dat".format(x,t)])


   
#Data for planets 'b' and 'c'

    for i in range(0,N):
#t=19.8
       t = (11 + i*M/N)

       list0 = []
       list1 = []
       list2 = []


#with open('output.{}','r'.format(t)) as file:
       with open("sun/output.{}_{}.dat".format(x,t),"r") as file:
          for row in file:
             a,b,c = row.split()
             list0.append(a)
             list1.append(b)
             list2.append(c)
       
          transit_number_b = []
          transit_time_b = []
          transit_number_c = []
          transit_time_c = []
       
          for k in range(0,len(list0)):
             if (list0[k]=='0'):
                transit_number_b.append(list1[k])
                transit_time_b.append(list2[k])
             if (list0[k]=='1'):
                transit_number_c.append(list1[k])
                transit_time_c.append(list2[k])
           
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
          for k in range(0,len(transit_number_b)):
             xb = xb + float(transit_number_b[k])
             yb = yb + float(transit_time_b[k])
             xyb = xyb + float(transit_number_b[k])*float(transit_time_b[k])
             x2b = x2b + float(transit_number_b[k])**2
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
          for k in range(0,len(transit_number_c)):
             xc = xc + float(transit_number_c[k])
             yc = yc + float(transit_time_c[k])
             xyc = xyc + float(transit_number_c[k])*float(transit_time_c[k])
             x2c = x2c + float(transit_number_c[k])**2
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

          for k in range(0,len(transit_number_b)):
             C_b[k] = a_b*k+b_b
             O_C_b[k] = (float(transit_time_b[k]) - C_b[k])*24.0*60.0
    
      #print(O_C_b)

##Calculate and difference in Observed for Planet C

#'C_c' is Calculated time y for planet c
          C_c = np.zeros(len(transit_number_c))

#'O_C_c is Observed/simulated transit time for planet c
          O_C_c = np.zeros(len(transit_number_c))

          for k in range(0,len(transit_number_c)):
             C_c[k] = a_c*k+b_c
             O_C_c[k] = (float(transit_time_c[k]) - C_c[k])*24.0*60.0
    
      #print(O_C_c)

          MAX_inner = max(O_C_b)
          MIN_inner = min(O_C_b)

          if(MAX_inner >= 100):
             TTV[i]=0
          else:
             TTV[i]= abs(MAX_inner-MIN_inner)
          Pouter[i] = t
    f = open("sun/sundata/outputfile.{}.dat".format(x), "w") # open file and write to file
    for z in range(0,N):
         print(Pouter[z],TTV[z],file=f)
    f.close()

      


