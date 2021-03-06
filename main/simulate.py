#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 11:09:51 2018

@author: sadra
"""

# Primary imports
import numpy as np

from main.auxilary_methods import find_mode,inside_X,find_mode_control
from main.controller import control_vanilla,control_convex,control_MPC

def simulate_vanilla(s,x):
    t=0
    s.traj=[]
    s.control_traj=[]
    s.value_traj=[]
    while t<100:
        t+=1
        s.traj.append(x)
        print("\n\n state:",x.T)
        u=control_vanilla(s,x)
        if u[0][0]==None:
            print("END of Control")
            return
        print("control:",u.T)
        x=evolve(s,x,u)
        
def simulate_convex(s,x,t_max=250):
    t=0
    s.traj=[]
    s.control_traj=[]
    s.value_traj=[]
    while t<t_max:
        t+=1
        s.traj.append(x)
        print("\n\n state:",x.T)
        u=control_convex(s,x)
        print(u)
        if u[0][0]==None:
            print("END Control")
            return
        s.control_traj.append(u)
        print("control:",u.T)
        x=evolve(s,x,u)
        
def simulate_MPC(s,x,H=2,t_max=250):
    t=0
    s.traj=[]
    s.control_traj=[]
    s.value_traj=[]
    while t<t_max:
        t+=1
        s.traj.append(x)
        print("\n\n state:",x.T)
        u=control_MPC(s,x,H)
        print(u)
        if u[0][0]==None:
            print("END Control")
            return
        s.control_traj.append(u)
        print("control:",u.T)
        x=evolve(s,x,u)
    
def evolve(s,x,u):
    i=find_mode_control(s,x)
    return np.dot(s.A[i],x)+np.dot(s.B[i],u)+s.c[i]

def evolve_nonlinear(s,x,u):
    pass

def simulate_0(s,x,T):
    for t in range(T):
        u=np.zeros((s.m,1))
        x_next=evolve(s,x,u)
        if inside_X(s,x_next)==False:
            return (x,T)
        else:
            x=x_next
    return (x,T)