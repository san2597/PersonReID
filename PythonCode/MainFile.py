########## This code has been tested with Python 3.6.8 [GCC 8.3.0] on Ubuntu 18.0 ##########
##### Module Versions listed below:
### NumPy - 1.17.2
### Scikit-learn - 0.21.3
### SciPy - 1.3.1
### OpenCV - 4.1.0

#######################################################All Modules######################################################

#### System Modules (In-built) ####
import os
import operator
import pdb  ##Python Debugger Module

#### Installed modules ####
import numpy as np    ##Numpy Version 1.17.2
from sklearn.decomposition import PCA ##SciKit-Learn Version 0.21.3
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import euclidean

#### Custom modules ####
import ami                      # Contains functions to calculate Affine Moment Invariants
from functions_module import *  # Contains functions to generate AEI and compute accuracy


#################################################Modifiable Parameters##################################################
#CASIA-B Dataset Location
casiab_location = 'C:\\Users\\san_2\\OneDrive\\Documents\\CDAC Gait Analysis\\CASIA-B Datasets\\'

#Train_test_split
split = 5  ##### No of sequences in training set

# No. of areas to divide AEI into
K = 23

#No of Affine Moment Invariants to be used for distance calculation
pca_dimensions = 5


################################################PCA Object Initialization###############################################
pca = PCA(pca_dimensions,whiten = True,svd_solver='auto')


##################################################List initializations##################################################
predictions = []
database = []
testSet = []


##########################################Train Test Split and Dataset Creation#########################################
#list of persons
print("Reading database")
person = sorted(os.listdir(casiab_location))

for p in person:
    for i in range(0,6):
        location = casiab_location+p+str("\\nm-{:02d}\\090\\".format(i+1))
        database.append(aei_generate(location))
    for j in range(split,6):
        testSet.append(p)

print("Active Energy Images generated for full database")

##pdb.set_trace()
database_set = list(divide_chunks(database,6))

# Image sequence separation and division into areas
print("Dividing the image into ", K, "segments")
print("Calculating affine moment invariants")

for i in range(0, len(person)):
    for j in range(0,6):
        locals()["DB_image_"+str("{:03d}_{:d}_areas".format(i+1, j+1))] = image_divide(database_set[i][j], K)
        locals()["DB_ami_"+str("{:03d}_{:d}".format(i+1, j+1))] = np.asarray([ami.affine_moment_vectors(x) for x in locals()["DB_image_"+str("{:03d}_{:d}_areas".format(i+1, j+1))]])

temp = None
for i in range(0,len(person)):
    for k in range(0,K):
        for j in range(0,6):
##            print(str("DB_ami_{:03d}_{:d}[{:d}]".format(i+1,j+1,k)))
            if temp is None:
                temp = locals()["DB_ami_"+str("{:03d}_{:d}".format(i+1,j+1))][k]
            else:
                temp = np.vstack((temp,locals()["DB_ami_"+str("{:03d}_{:d}".format(i+1,j+1))][k]))

print("Performing standardization and principal component analysis")
A_DB = pca.fit_transform(StandardScaler().fit_transform(temp))



#################For checking Test subject AMI order#################
##for i in range(0,len(person)):
##    for j in range(0,split):
##        for k in range(0,K):
##            print(str("DB_ami_{:03d}_{:d}[{:d}]".format(i+1,j+1,k)))           

###################For checking Database AMI order###################
##for i in range(0,len(person)):
##    for k in range(0,K):
##        for j in range(0,split):
##            print(str("DB_ami_{:03d}_{:d}[{:d}]".format(i+1,j+1,k)))


####################################Test Subject split and concatenate in A_SUB_list####################################
SUB_list_indices = []
A_SUB_list = []

print("Splitting the database into training and test data")

for i in range(0,A_DB.shape[0]):
    if i%6 >=split:
        SUB_list_indices.append(i)

A_SUB_temp = np.zeros((len(SUB_list_indices),pca_dimensions))

for i in range(0,len(SUB_list_indices)):
    A_SUB_temp[i] = A_DB[SUB_list_indices[i]]

person_set = K*(6-split)

for m in range(0,len(person)):
    locals()["A_SUB_"+str("{:03d}".format(m+1))] = A_SUB_temp[m*person_set:(m+1)*person_set]
    for j in range(0,6-split):
        locals()["A_SUB_"+str("{:03d}_{:d}".format(m+1,j+split+1))] = None
        for k in range(0,K):
            if locals()["A_SUB_"+str("{:03d}_{:d}".format(m+1,j+split+1))] is None:
                locals()["A_SUB_"+str("{:03d}_{:d}".format(m+1,j+split+1))] = locals()["A_SUB_"+str("{:03d}".format(m+1))][j+k*(6-split)]
            else:
                locals()["A_SUB_"+str("{:03d}_{:d}".format(m+1,j+split+1))] = np.vstack((locals()["A_SUB_"+str("{:03d}_{:d}".format(m+1,j+split+1))],locals()["A_SUB_"+str("{:03d}".format(m+1))][j+k*(6-split)]))
        A_SUB_list.append(locals()["A_SUB_"+str("{:03d}_{:d}".format(m+1,j+split+1))])


####################################Train Subject split and concatenate in A_DB_i_j#####################################
A_Train_DB = np.delete(A_DB,SUB_list_indices,0)

for i in range(0,len(person)):
    for j in range(0,K):
        locals()["A_DB_"+str("{:03d}_{:d}".format(i+1,j+1))] = A_Train_DB[0:split]
        A_Train_DB = np.delete(A_Train_DB,[k for k in range(0,split)],0)




#################################Evaluating for each test subject and predicting person#################################
print("Calculating Euclidean distance for each test subject and predicting output using nearest neighbor")
for test_subject in A_SUB_list:
    A_SUB_test = test_subject

    ####################################Distance calculation between subject and dataset####################################
    for j in range(0,len(person)):
        for i in range(0,K):
            locals()["d_"+str("{:03d}_{:d}".format(j+1,i+1))] = np.zeros((split,1))
            for k in range(0,split):
                locals()["d_"+str("{:03d}_{:d}".format(j+1,i+1))][k] = euclidean(A_SUB_test[i],locals()["A_DB_"+str("{:03d}_{:d}".format(j+1,i+1))][k])
            locals()["d_"+str("{:03d}_{:d}".format(j+1,i+1))] = np.transpose(locals()["d_"+str("{:03d}_{:d}".format(j+1,i+1))])


    ##############################################Maximum distance calculation##############################################
    maximum_d = []
    for i in range(0,len(person)):
        for j in range(0,K):
            maximum_d.append(locals()["d_"+str("{:03d}_{:d}".format(i+1,j+1))])
    d_max = np.amax(np.vstack(maximum_d))
##    print(d_max)

    max_d_list = [] ##List of all distance sequences where least similarity exists


    #######################################Minimum distance calculation for each area#######################################
            
    for j in range(0,K):
        temp = None
        for i in range(0,len(person)):
            if temp is None:
                temp = np.mean(locals()["d_"+str("{:03d}_{:d}".format(i+1,j+1))])
    ##            print(str("d_{:03d}_{:d}".format(i+1,j+1)))
            else:
                temp = np.vstack((temp,np.mean(locals()["d_"+str("{:03d}_{:d}".format(i+1,j+1))])))
    ##            print(str("d_{:03d}_{:d}".format(i+1,j+1)))
    ##    print(str("d_min_{:d}".format(j+1)))
        locals()["d_min_"+str("{:d}".format(j+1))] = np.amin(temp)


    #############################################Matching weights###########################################################
        for i in range(0,len(person)):
            x = locals()["d_"+str("{:03d}_{:d}".format(i+1,j+1))] < locals()["d_min_"+str("{:d}".format(j+1))]
            if anyTrueCheck(x):
                continue
            else:
                max_d_list.append(str("d_{:03d}_{:d}".format(i+1,j+1)))
                for k in range(0,locals()["d_"+str("{:03d}_{:d}".format(i+1,j+1))].shape[1]):
                    locals()["d_"+str("{:03d}_{:d}".format(i+1,j+1))][0,k] = d_max
    


    ##############################################Concatenating all distances###############################################
    DB_distance_list = None            
    for i in range(0,len(person)):
        locals()["d_"+str("{:03d}".format(i+1))] = np.zeros((1,split))
        for j in range(0,K):
            locals()["d_"+str("{:03d}".format(i+1))] += locals()["d_"+str("{:03d}_{:d}".format(i+1,j+1))]
        if DB_distance_list is None:
            DB_distance_list = locals()["d_"+str("{:03d}".format(i+1))]
        else:
            DB_distance_list = np.vstack((DB_distance_list,locals()["d_"+str("{:03d}".format(i+1))]))

    ######################################Nearest Neighbor and prediction set creation######################################
    result = np.where(np.amin(DB_distance_list)==DB_distance_list)
    x = str("{:03d}".format(np.asscalar(result[0])+1))
    predictions.append(x)

##    print(sum(pca.explained_variance_ratio_[0:3]))


##Calculating accuracy of algorithm
print("Predictions done")
      
accuracy = getAccuracy(testSet,predictions)
print(str("Accuracy = {0:f}%".format(accuracy)))
