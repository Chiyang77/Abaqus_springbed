
from abaqus import *
from abaqusConstants import *
import numpy as np
import sys
sys.path.append('C:/Python27/Lib/site-packages/')
from abaqusConstants import *
import regionToolset
# add reference point, fix rfp, add spring
import __main__


import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior	



def ballastspring(modelname,instanname,setname,sc,springstiff,dashpotcoef,offset,mass):
    
	
	
	
	instanname=instanname
	setname=str(setname)
	modelname=str(modelname)
	#ssp is for "sleeper spring"
	springname='ssp'+str(sc)
	fixspringname='fixspring'+str(sc)
	addmassname='mass'+str(sc)
	setnodeno=[]
	rffix=[]
	sp=[]
	re=[]
	


	lenset=len(mdb.models[modelname].rootAssembly.sets[setname].nodes)
	 # How many nodes in the set
	for y in range(lenset):
		setnodeno.append(mdb.models[modelname].rootAssembly.sets[setname].nodes[y].label)
		
		
		
	for x in range(len(setnodeno)):
		node1=setnodeno[x]
		b=mdb.models[modelname].rootAssembly.instances[instanname]
		rfp=[b.nodes[node1-1].coordinates[0],b.nodes[node1-1].coordinates[1]-offset,b.nodes[node1-1].coordinates[2]]
		a = mdb.models[modelname].rootAssembly
		myRPFeat = a.ReferencePoint(point=(tuple(rfp)))
		mySetMaster = a.Set(name='rf_'+str(sc)+str(node1),referencePoints=(a.referencePoints[myRPFeat.id], ))
		rgn1pair0=mdb.models[modelname].rootAssembly.sets['rf_'+str(sc)+str(node1)]
		rffix.append(mySetMaster)

	#Creating sets for selecting nodes 
		mdb.models[modelname].rootAssembly.Set(nodes=mdb.models[modelname].rootAssembly.instances[instanname].nodes[node1-1:node1], name='rfs_'+str(sc)+'_'+str(node1))
		rgn2pair0=mdb.models[modelname].rootAssembly.sets['rfs_'+str(sc)+'_'+str(node1)]
		sp=(rgn1pair0,rgn2pair0)
		lsp=list(sp)
		re.append(lsp)
		
			
	a1=re
	region=tuple(a1)
	mdb.models[modelname].rootAssembly.engineeringFeatures.TwoPointSpringDashpot(
	name=springname, regionPairs=region, axis=NODAL_LINE, springBehavior=ON, 
	springStiffness=springstiff, dashpotBehavior=ON, dashpotCoefficient=dashpotcoef)
	#fix ground rfp
	fixregion=mdb.models[modelname].rootAssembly.SetByMerge(name='fixregion'+str(sc),sets=rffix)
	mdb.models[modelname].EncastreBC(name=fixspringname, createStepName='Initial',region=fixregion, localCsys=None)

	#add mass to rfp     
	region=mdb.models[modelname].rootAssembly.sets['fixregion'+str(sc)]
	mdb.models[modelname].rootAssembly.engineeringFeatures.PointMassInertia(
		name=addmassname, region=region, mass=mass, alpha=0.0, composite=0.0)
