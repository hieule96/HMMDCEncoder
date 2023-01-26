# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 09:43:38 2021

@author: hieu1
"""
import Transform as tf
import numpy as np
from scipy.optimize import curve_fit
import scipy.optimize
import scipy.stats
import Quadtreelib as qd
import pdb
import matplotlib.pyplot as plt
from skimage.metrics import mean_squared_error
from multiprocessing import Pool
from itertools import repeat

class OptimizerParamterForComputeLocale():
    mu1 = None
    mu2 = None
    Ci1 = None
    Ci2 = None
    lam1 = None
    lam2 = None
    def __init__(self, mu1, mu2, lam1,lam2):
        self.lam1 = lam1
        self.lam2 = lam2
        self.mu1 = mu1
        self.mu2 = mu2

class OptimizerParameterLambdaCst(OptimizerParamterForComputeLocale):
    def __init__(self,lam1,lam2, mu1, mu2,
         n0, LCU, Dm,Rt = 1.0,rN=0.01):
        super().__init__(lam1=lam1,lam2=lam2,mu1=mu1,mu2=mu2)
        self.n0 = n0
        self.LCU = LCU
        self.Dm = Dm
        self.rN = rN
        self.Rt = Rt
class ComputeStatistic():
    @staticmethod
    def computeSigmaNodeAC(node,LCU):
        img_cu = node.get_points(LCU.img)
        img_dct_cu_AC = tf.dct(img_cu - img_cu.mean())
        sigma = np.std(img_dct_cu_AC)
        return sigma
    @staticmethod
    def get_mse(img1, img2):
        return mean_squared_error(img1,img2)
    @staticmethod
    def entropy_node(img_dct_cu):
        # Calculate entropy
        entropy = 0
        _,counts =np.unique(img_dct_cu,return_counts=True)
        probalitity = counts/counts.sum()
        # n_classes = np.count_nonzero(probalitity)
        entropy = -np.sum(probalitity*np.log2(probalitity))
        return entropy
    @staticmethod
    def get_rsquare(data_fit,real_data):
        residuals = real_data - data_fit
        ss_tot = np.sum((real_data - np.mean(real_data))**2)
        ss_res = np.sum(residuals**2)
        r_squared = 1 - (ss_res / ss_tot)
        return r_squared
class Rounding():
    @staticmethod
    def roundTo3Decimal(value):
        return np.around(value, decimals=3)
class Optimizer():
    def __init__(self,oparam):
        self.globalparam = oparam
    def changeParameter(self,new_param):
        self.globalparam = new_param
    def setRt(self,Rt):
        self.globalparam.Rt = Rt
    def initializeCijSigma(self, qtree, compute_sigma_function,rN):
        """
        Parameters
        ----------
        qtree : Quadtree
        Quadtree
        compute_sigma_function: function to compute sigma (with AC Default quantized or not)
        Returns
        -------
        sigma : array of float
            standard deviation of the imqge
        Ci1 : array of float
            Redundancy parameter of Description 1
        Ci2 : array of float
            Redundancy parameter of Description 2
        """
        c = qtree
        Ci1 = np.ones(len(c))
        Ci2 = np.ones(len(c))
        sigma = np.zeros(len(c))
        index = range(0, len(c))
        LCU = self.globalparam.LCU
        AllocationSigma = np.zeros(len(c))
        for i in index:
            sigma[i] = compute_sigma_function(c[i],LCU)
            AllocationSigma[i] = sigma[i]
            turn = 0
        while (turn < len(c)):
            max_sigma_index = np.argmax(AllocationSigma)
            if (turn%2==0):
                Ci1[max_sigma_index] = 1
                Ci2[max_sigma_index] = rN
            else:
                Ci1[max_sigma_index] = rN
                Ci2[max_sigma_index] = 1
            AllocationSigma[max_sigma_index] = 0
            turn = turn + 1
        # logging.debug("Sigma: %s" %(sigma))
        # logging.debug("Ci1 %s Ci2 %s " %(Ci1,Ci2))
        return sigma, Ci1, Ci2
    def initializeCijSliceIntra(qtree,rN):
        c = qtree
        Ci1 = []
        Ci2 = []
        turn = 0
        for i in c:
            if (not i.isSkip):
                if (turn%2==0):
                    i.Ci1 = (1.0-rN)
                    i.Ci2 = rN
                else:
                    i.Ci1 = rN
                    i.Ci2 = (1.0-rN)
                Ci1.append(i.Ci1)
                Ci2.append(i.Ci2)
                turn+=1
            else:
                print ("Skipped CU")
        return Ci1, Ci2
    def initializeCijSliceInter(qtree,rN):
        c = qtree
        Ci1 = []
        Ci2 = []
        for i in c:
            if (not i.isSkip):
                if (i.CTURSIndex%2==0):
                    i.Ci1 = (1.0-rN)
                    i.Ci2 = rN
                else:
                    i.Ci1 = rN
                    i.Ci2 = (1.0-rN)
                Ci1.append(i.Ci1)
                Ci2.append(i.Ci2)
            else:
                print ("Skipped CU")
        return Ci1, Ci2
    def optimizeQuadtreeLambaCst(self, qtree,lam1,lam2,mu1,mu2,E1,E2,Ci1,Ci2,Dm,rN):
        raise NotImplementedError("Method optimizeQuadtreeLambaCst is not implemented")
    def optimize_LCU(self):        
        (Qi1, Qi2, D1, D2, Ratej_Q1, Ratej_Q2,r1,r2) = self.optimizeQuadtreeLambaCst(self.globalparam.LCU.CTUs[0],self.globalparam.lam1,self.globalparam.lam2,
                                                                               self.globalparam.mu1,self.globalparam.mu2,
                                                                               self.globalparam.Ci1,self.globalparam.Ci2,
                                                                               self.globalparam.Dm,self.globalparam.rN)
        pos = 0
        self.globalparam.LCU.D1est = D1
        self.globalparam.LCU.D2est = D2
        self.globalparam.LCU.R1est = Ratej_Q1
        self.globalparam.LCU.R2est = Ratej_Q2
        print ("Qi Size",len(Qi1),len(Qi2),sum(self.globalparam.LCU.nbCUperCTU))
        assert (sum(self.globalparam.LCU.nbCUperCTU)==len(Qi1) and sum(self.globalparam.LCU.nbCUperCTU)==len(Qi2))
        for x in self.globalparam.LCU.nbCUperCTU:
            self.globalparam.LCU.Qi1.append(Qi1[pos:pos+x])
            self.globalparam.LCU.Qi2.append(Qi2[pos:pos+x])
            pos+=x
        return self.globalparam.LCU
class FunctionCurveFitting():
    @staticmethod
    def negExponential(x, a, b):
        return a * np.exp(b * x)
    @staticmethod
    def exponential(x, a, b, c):
        return a * np.exp(b * x) + c
    @staticmethod
    def cubic(x, a, b, c, d):
        return a * x ** 3 + b * x ** 2 + c * x + d
    @staticmethod
    def linear(x, a, b):
        return a * x + b
    @staticmethod
    def derivateExp(x, a, b):
        return a * b * np.exp(b * x)
    @staticmethod
    def exponential_function2(x,a,b,c,d):
        return a*np.exp(b*x)+c*np.exp(d*x)
    @staticmethod
    def derivateExp2(x,a,b,c,d):
        return a*b*np.exp(b*x) + c*d*np.exp(d*x)
    @staticmethod
    def hyperbole(x,a,b,c):
        return a*x**b + c
    @staticmethod
    def derivatehyperbole(x,a,b):
        return a*b*x**(b-1)
class Optimizer_curvefitting(Optimizer):
    curve_fitting_function = FunctionCurveFitting.exponential
    derivate_function = FunctionCurveFitting.derivateExp
    nbCoeff = 0
    QPMin = 0
    QPMax = 51
    def __init__(self,oparam=None,curve_fitting_function = "exp",QPMin=0,QPMax=51):
        super().__init__(oparam)
        if (curve_fitting_function=="exp3"):
            self.curve_fitting_function = FunctionCurveFitting.exponential
            self.derivate_function = FunctionCurveFitting.derivateExp
            self.nbCoeff = 3
        elif (curve_fitting_function=="hyperbolic3"):
            self.curve_fitting_function = FunctionCurveFitting.hyperbole
            self.derivate_function = FunctionCurveFitting.derivatehyperbole
            self.nbCoeff = 3
        elif (curve_fitting_function=="exp2"):
            self.curve_fitting_function = FunctionCurveFitting.negExponential
            self.derivate_function = FunctionCurveFitting.derivateExp
            self.nbCoeff = 2
        elif (curve_fitting_function=="exp4"):
            self.curve_fitting_function = FunctionCurveFitting.exponential_function2
            self.derivate_function = FunctionCurveFitting.derivateExp2
            self.nbCoeff = 4
        self.QPMax = QPMax
        self.QPMin = QPMin
    def dj(self,qtree,rij):
        i=0
        dj = 0
        rj = 0
        for cu in qtree:
            # counting only not skip element
            if (not cu.isSkip):
                dij = self.curve_fitting_function(rij[i],*cu.DRcoeff)
                dj += dij*cu.aki
                rj += rij[i]*cu.aki
                i+=1
        return dj,rj
    def compteCurveCoefficientMultithread(self,LCU):
        with Pool() as p:
            result = p.starmap(self.curve_fitting,zip(repeat(LCU),LCU.CTUs[0]))
        i=0
        for cu in LCU.CTUs[0]:
            cu.isSkip = result[i][0]
            cu.set_DRcoeff(result[i][1])
            cu.set_bound(result[i][2],result[i][3])
            i+=1
    def computeCurveCoefficient(self,LCU):
        for cus in LCU.CTUs:
            for cu in cus:
                DRcoeff,MAX_E,MIN_E = self.curve_fitting(LCU,cu)
                cu.set_DRcoeff(DRcoeff)
                cu.set_bound(MAX_E,MIN_E)
    @staticmethod
    def compute_mse_entropy_QP(LCU, node, QPs):
        # Take image in partition and dct
        img_cu = node.get_points(LCU.img)
        if (img_cu.std()==0):
            node.isSkip = True
            return [],[]
        block8x8_dct = []
        for y in range(0,img_cu.shape[0],8):
            for x in range(0,img_cu.shape[1],8):
                block8x8_dct.append([x,y,tf.integerDctTransform8x8(img_cu[y:y+8,x:x+8])])
        entropy_list = []
        mse_list = []
        img_rec_2D = np.zeros(img_cu.shape)
        for QP in QPs:
            entropy = 0
            for x,y,tu in block8x8_dct:
            # Quantize the image
                tuQ = tf.quant(QP, tu)
                img_dct_cu_Reconstruct = tf.dequant(QP, tuQ)
                # Calculate entropy
                entropy += ComputeStatistic.entropy_node(tuQ)
                img_rec_2D[y:y+8,x:x+8] = tf.IintegerDctTransform8x8(img_dct_cu_Reconstruct)
                img_rec_2D [img_rec_2D <-128] = -128
                img_rec_2D [img_rec_2D >127] = 127
            entropy = entropy/(img_cu.shape[0]//8*img_cu.shape[1]//8)
            mse = ComputeStatistic.get_mse(img_rec_2D , img_cu)
            entropy_list.append (entropy)
            # Calculate MSE
            mse_list.append(mse)
        return mse_list,entropy_list
    @staticmethod
    def compute_mse_entropy_QP_TUVariable(LCU, node, QPs):
        # Take image in partition and dct
        mse_list = []
        entropy_list = []
        for QP in QPs:
            tu = qd.TransformUnit(node.x0, node.y0, node.width, node.height, 1, 0)
            tu.setQP(QP)
            tu.recursive_subdivide(LCU.img)
            mse,entropy = tu.computeRateDistortion()
            # Calculate MSE
            mse_list.append(mse)
            entropy_list.append(entropy)
        entropy_list = np.array(entropy_list)
        mse_list = np.array(mse_list)
        return mse_list,entropy_list
    def quantCU(QP,block8x8_dct,nbTU):
        entropy = 0
        ## Trunc because quantificator accept only integer number
        QP = int (QP)
        for x,y,tu in block8x8_dct:
            tuQ = tf.quant(QP, tu)
            entropy += ComputeStatistic.entropy_node(tuQ)
        # Calculate entropy
        entropy = entropy/nbTU
        return entropy

    def searchQP(QP,block8x8_dct,nbTU,rtarget):
        entropy = Optimizer_curvefitting.quantCU(QP,block8x8_dct,nbTU)
        return entropy - rtarget
    def searchQPTUVariable(QP,node,rtarget,img):
        QP = int(QP)
        tu = qd.TransformUnit(node.x0, node.y0, node.width, node.height, 1, 0)
        tu.setQP(QP)
        tu.recursive_subdivide(img)
        mse,entropy = tu.computeRateDistortion()
        return entropy - rtarget
    @staticmethod
    def searchForQPbyRateTUVariable(img,node,rtarget):
        # bisect algorithm
        QP = scipy.optimize.bisect(Optimizer_curvefitting.searchQPTUVariable,0,50,args=(node,rtarget,img))
        entropy = Optimizer_curvefitting.searchQPTUVariable(QP,node,rtarget,img) + rtarget
        return round(QP),entropy
    def searchForQPbyRate(self,img,node,rtarget):
        # Take image in partition and dct
        img_cu = node.get_points(img)
        block8x8_dct = []
        nbTU8x8 = img_cu.shape[0]//8*img_cu.shape[1]//8
        for y in range(0,img_cu.shape[0],8):
            for x in range(0,img_cu.shape[1],8):
                block8x8_dct.append([x,y,tf.integerDctTransform8x8(img_cu[y:y+8,x:x+8])])
        # bisect algorithm
        QP = scipy.optimize.bisect(Optimizer_curvefitting.searchQP,self.QPMin,self.QPMax,args=(block8x8_dct,nbTU8x8,rtarget))
        entropy = Optimizer_curvefitting.quantCU(QP,block8x8_dct,nbTU8x8)
        return round(QP),entropy
    def curve_fitting(self,LCU,node):
        #Make an array from 0 to 51 with the beginning point is zeros and the end is 51 with a step of 8, 
        # with 0 and 51 included
        interval = (self.QPMax-self.QPMin)//4
        QPs = range(self.QPMin, self.QPMax+1, interval)
        QPs = np.concatenate((QPs, [51]))
        QPs = np.concatenate(([10],QPs))
        mseQP,entropyQP = Optimizer_curvefitting.compute_mse_entropy_QP(LCU,node,QPs)
        MAX_E = MIN_E = 0
        DRcoeff = [0,0]
        if (not node.isSkip):
            try:
                #Check in mseQP array if there is a zero in the array, 
                # if yes, remove it from this list and the element at the same position in entropyQP
                mseQP = np.array(mseQP)
                entropyQP = np.array(entropyQP)
                entropyQP = entropyQP[mseQP != 0]
                mseQP = mseQP[mseQP != 0]
                #First fit the linear function then fit last the function exp
                log_mse_QP = np.log(mseQP)
                a,b,_,_,_ = scipy.stats.linregress(entropyQP,log_mse_QP)
                DRcoeff=[np.exp(b),a]
                DRcoeff, pcovDR = curve_fit(self.curve_fitting_function, entropyQP, mseQP,p0=DRcoeff,ftol=0.05, xtol=0.05)
                # DR_fit = self.curve_fitting_function(entropyQP, *DRcoeff)
                # err = ComputeStatistic.get_rsquare(DR_fit,mseQP)
                # if (True):
                #     print ("rsquared D(R): e:%s l:%s" %(err,r))
                #     plt.scatter(entropyQP, mseQP)
                #     plt.plot(entropyQP,DR_fit)
                #     plt.show()
            except ValueError:
                # print ("Curve fitting of DR at node: %s,%s,%s,%s failed" %(node.x0,node.y0,node.x0+node.width,node.y0+node.height))
                node.isSkip = True
        if (not node.isSkip):
            MAX_E = entropyQP[1]
            MIN_E = entropyQP[-2]
        return node.isSkip,DRcoeff,MAX_E,MIN_E
    def cost_func(self,r,lam,aki,DR_coeff,Ci,mu,Dm,Rt,rN):
        Di = aki*self.curve_fitting_function(r,*DR_coeff)
        Dcost = np.sum(Ci*Di)
        Dtotal = np.sum(Di)
        R = np.dot(aki,r)
        cost = Dcost + lam*(R-Rt) + mu*((np.abs(Dtotal-Dm) + (Dtotal-Dm))/2)**2
        return cost
    def grad_func(self,r,lam,aki,DR_coeff,Ci,mu,Dm,Rt,rN):
        #pdb.set_trace()
        Di = aki*self.curve_fitting_function(r,*DR_coeff)
        Dtotal = np.sum(Di)
        Diprime = aki*self.derivate_function(r,DR_coeff[0],DR_coeff[1])
        Riprime = aki
        E = 2*(np.abs(Dtotal-Dm) + (Dtotal-Dm))
        grad = Ci*Diprime + lam * Riprime + mu*E*Diprime
        return grad
    def RateContraint(r,aki,Rt):
        constraint = np.dot(aki,r) - Rt
        return constraint
    def compute_r(self,qtree,lami,mui,Ci,Dm,rN):
        DR_coeff_cu = []
        aki = []
        r = []
        bounds = []
        Rmin = 0
        count = 0
        for cu in qtree:
            if (len(cu.DRcoeff)>0 and not cu.isSkip):
                DR_coeff_cu.append(cu.DRcoeff)
                r.append(1.0)
                aki.append(cu.aki)
                bounds.append(cu.bound)
                Rmin += cu.bound[0]
                count += 1
        Rmin/=count
        DR_coeff_cu = np.array(DR_coeff_cu)
        DR_coeff_cu = np.hsplit(DR_coeff_cu,self.nbCoeff)
        for i in range (self.nbCoeff):
            DR_coeff_cu[i] = DR_coeff_cu[i].reshape(-1,)
        aki = np.array(aki)
        r = np.array(r)
        # Constraint on border
        #Solving to QP directly by TNC method
        result_minize = scipy.optimize.minimize(self.cost_func,
                                          r,
                                          jac=self.grad_func,
                                          args=(lami,aki,DR_coeff_cu,Ci,mui,Dm,self.globalparam.Rt/2,rN),
                                          bounds=bounds,method='L-BFGS-B')
        # print (result_minize.success,result_minize.fun)
        assert(result_minize.success)
        return result_minize.x
    # Direct lambda injection mode
    def contraintRT(self,lam,qtree,mu,Ci,Dm,rN,Rt):
        r = self.compute_r(qtree,lam,mu,Ci,Dm,rN)
        _,ri= self.dj(qtree,r)
        return ri - Rt
    def optimizeQuadtreeLambaCst(self, qtree,lam1,lam2,mu1,mu2,Ci1,Ci2,Dm,rN):
        Ci1_old, Ci2_old = Optimizer_curvefitting.initializeCijSliceIntra(qtree,self.globalparam.rN)
        QP1 = []
        QP2 = []
        entropy1 = []
        entropy2 = []
        lam1 = scipy.optimize.bisect(self.contraintRT,0,10000,args=(qtree,mu1,Ci1_old,Dm,rN,self.globalparam.Rt/2))
        lam2 = scipy.optimize.bisect(self.contraintRT,0,10000,args=(qtree,mu2,Ci2_old,Dm,rN,self.globalparam.Rt/2))
        print ("Ci Size:",len(Ci1_old),len(Ci2_old))
        r1 = self.compute_r(qtree,lam1,mu1,Ci1_old,Dm,rN)
        r2 = self.compute_r(qtree,lam2,mu2,Ci2_old,Dm,rN)
        r_count = 0
        for node in qtree:
            if (node.isSkip):
                QP1.append(self.QPMin)
                QP2.append(self.QPMin)
                entropy1.append(0)
                entropy2.append(0)
            else:
                a,b = self.searchForQPbyRate(self.globalparam.LCU.img,node,r1[r_count])
                c,d = self.searchForQPbyRate(self.globalparam.LCU.img,node,r2[r_count])
                QP1.append(a)
                entropy1.append(b)
                QP2.append(c)
                entropy2.append(d)
                r_count+=1
        Di1,ri1=self.dj(qtree,entropy1)
        Di2,ri2=self.dj(qtree,entropy2)
        return QP1,QP2, Di1, Di2, ri1, ri2,entropy1,entropy2        
    def getRecImg(self,LCU,img,QPs,r):
        img_rec_2D = np.zeros(img.shape)
        i=0
        mse = 0
        delta = 0
        for cus in LCU.CTUs:
            for node in cus:
                img_cu=node.get_points(img)
                for y in range(0,img_cu.shape[0],8):
                    for x in range(0,img_cu.shape[1],8):
                        tu = tf.integerDctTransform8x8(img_cu[y:y+8,x:x+8])
                        # pdb.set_trace()
                        tuQ = tf.quant(QPs[i], tu)
                        img_dct_cu_Reconstruct =  tf.dequant(QPs[i], tuQ)
                        # Calculate entropy
                        img_rec_2D[node.y0+y:node.y0+y+8,node.x0+x:node.x0+x+8] = tf.IintegerDctTransform8x8(img_dct_cu_Reconstruct)
                        img_rec_2D [img_rec_2D <-128] = -128
                        img_rec_2D [img_rec_2D >127] = 127
                mse2 = self.curve_fitting_function(r[i],*node.DRcoeff)*node.aki
                mse1 = ComputeStatistic.get_mse(node.get_points(img_rec_2D), img_cu)*node.aki
                delta+= abs(mse1 - mse2)
                mse += mse1
                i+=1
        print ("Delta Error :",delta)
        img_rec_2D = img_rec_2D+128
        return img_rec_2D.astype("uint8"),mse
        
            
# class OptimizerReal(Optimizer):
#     def quantCUReal(img, node, QP):
#         # Take image in partition and dct
#         img_cu = node.get_points(img)
#         block8x8_dct = []
#         for y in range(0,img_cu.shape[0],8):
#             for x in range(0,img_cu.shape[1],8):
#                 block8x8_dct.append([x,y,tf.integerDctTransform8x8(img_cu[y:y+8,x:x+8])])
#         img_rec_2D = np.zeros(img_cu.shape)
#         entropy = 0
#         for x,y,tu in block8x8_dct:
#         # Quantize each CU
#             tuQ = tf.quant(QP, tu)
#             img_dct_cu_Reconstruct = tf.dequant(QP, tuQ)
#             # Calculate entropy
#             entropy += ComputeStatistic.entropy_node(tuQ)
#             img_rec_2D[y:y+8,x:x+8] = tf.IintegerDctTransform8x8(img_dct_cu_Reconstruct)
#             img_rec_2D [img_rec_2D <-128] = -128
#             img_rec_2D [img_rec_2D >127] = 127
#         entropy = entropy/(img_cu.shape[0]//8*img_cu.shape[1]//8)
#         mse = ComputeStatistic.get_mse(img_rec_2D , img_cu)
#         return mse,entropy
#     def realcost(self,Q,qtree,img,lam,Rt):
#         Dcost = 0
#         Ri = 0
#         i = 0
#         for cu in qtree:
#             mse,entropy = OptimizerReal.quantCUReal(img,cu,int (Q[i]))
#             Dcost += cu.aki*cu.Ci1*mse
#             Ri += cu.aki*cu.Ci1*entropy
#             i+=1
#         cost = Dcost + lam*(Ri-Rt)
#         # print (Q)
#         return cost
#     def contraintRT(self,lam,qtree,img,Ci,Rt):
#         bounds = np.full((len(Ci),2),[0,51])
#         QPj = np.full((len(Ci),1),25)
#         result_minize = scipy.optimize.minimize(self.realcost,
#                                           QPj,
#                                           args=(qtree,img,lam,Rt),
#                                           bounds=bounds,method='L-BFGS-B',
#                                           options={'eps':3})
#         i = 0
#         Ri = 0
#         for cu in qtree:
#             _,entropy = OptimizerReal.quantCUReal(img,cu,result_minize.x[i])
#             Ri += cu.Ci*entropy
#             i+=1
#         return Ri - Rt
#     def optimizeQuadtree(self):
#         qtree = self.globalparam.LCU.CTUs[0]
#         img = self.globalparam.LCU.img
#         Ci1_old, Ci2_old = Optimizer_curvefitting.initializeCijSlice(qtree,1,self.globalparam.rN)
#         lam1 = scipy.optimize.bisect(self.contraintRT,0.01,500,args=(qtree,img,Ci1_old,self.globalparam.Rt/2))
#         lam2 = scipy.optimize.bisect(self.contraintRT,0.01,500,args=(qtree,img,Ci2_old,self.globalparam.Rt/2))
#         return lam1,lam2
#     def optimizeQuadtreeLamCst(self):
#         qtree = self.globalparam.LCU.CTUs[0]
#         img = self.globalparam.LCU.img
#         Ci1_old, Ci2_old = Optimizer_curvefitting.initializeCijSlice(qtree,1,self.globalparam.rN)
#         bounds = np.full((len(Ci1_old),2),[0,51])
#         Qj = np.full((len(Ci1_old),1),25)
#         result_minize = scipy.optimize.minimize(self.realcost,
#                                           Qj,
#                                           args=(qtree,img,self.globalparam.lam1,self.globalparam.Rt/2),
#                                           bounds=bounds,method='Nelder-Mead',
#                                           options={'adaptative':True,'maxiter':100})
#         return result_minize.x