def geomoment(img,p,q):
    row = img.shape[0]
    col = img.shape[1]

    gm = 0;
    for i in range(0,row):
        for j in range(0,col):
            gm = gm+((i-1)**p)*((j-1)**q)*(img[i,j])

    return gm

    

#Calculate centroid of image
def centroid_image(img):
    gm10 = geomoment(img,1,0)
    gm01 = geomoment(img,0,1)
    m00 = sum(sum(img))

    x_bar = (gm10)/m00
    y_bar = (gm01)/m00

    return x_bar,y_bar


#calculate central moments
def central_moment(img,xbar,ybar,p,q):
    row = img.shape[0]
    col = img.shape[1]

    cm = 0
    for i in range(0,row):
        for j in range(0,col):
            cm = cm+((i-1-xbar)**p)*((j-1-ybar)**q)*(img[i,j])

    return cm


#Computing affine moment invariants 
def affine_moment_vectors(img):
    x_bar,y_bar = centroid_image(img)

    #Central moments of each img
    mu_00 = sum(sum(img))
    mu_11 = central_moment(img, x_bar,y_bar,1,1)
    mu_13 = central_moment(img, x_bar,y_bar,1,3)
    mu_20 = central_moment(img, x_bar,y_bar,2,0)
    mu_02 = central_moment(img, x_bar,y_bar,0,2)
    mu_21 = central_moment(img, x_bar,y_bar,2,1)
    mu_22 = central_moment(img, x_bar,y_bar,2,2)
    mu_12 = central_moment(img, x_bar,y_bar,1,2)
    mu_03 = central_moment(img, x_bar,y_bar,0,3)
    mu_30 = central_moment(img, x_bar,y_bar,3,0)
    mu_31 = central_moment(img, x_bar,y_bar,3,1)
    mu_40 = central_moment(img, x_bar,y_bar,4,0)
    mu_04 = central_moment(img, x_bar,y_bar,0,4)


    #Calculating affine moments
    I1 = ((mu_20*mu_02) - ((mu_11)**2))/((mu_00)**4)
    I2 = ((-1*((mu_30*mu_03)**2))+6*mu_30*mu_21*mu_12*mu_03 - 4*mu_30*((mu_12)**3) - 4*((mu_21)**3)*mu_03 + 3*((mu_21*mu_12)**2))/((mu_00)**10)
    I3 = (mu_20*mu_21*mu_03 - (mu_20*((mu_12)**2)) - (mu_11*mu_30*mu_03) + (mu_11*mu_21*mu_12) + (mu_02*mu_30*mu_12) - mu_02*((mu_21)**2))/((mu_00)**7)
    I4 = (-((mu_20)**3) * ((mu_03)**2) + 6 * ((mu_20)**2) * mu_11 *mu_12 *mu_03 - 3 * ((mu_20)**2) * mu_02 * ((mu_12)**2) - 6 * mu_20 * ((mu_11)**2) * mu_21 * mu_03 - 6 * mu_20 * ((mu_11 * mu_12)**2) + 12 * mu_20 * mu_11 * mu_02 * mu_21 * mu_12 - 3 * mu_20 * ((mu_02)**2) *((mu_21)**2) + 2*((mu_11)**3) * mu_30 * mu_03 + 6 * ((mu_11)**3) * mu_21 * mu_12 - 6 * ((mu_11)**2) * mu_02 * mu_30 * mu_12 - 6 * ((mu_11)**2) * mu_02 *((mu_21)**2) + 6 * mu_11 *((mu_02)**2) * mu_30 * mu_21 - ((mu_02)**3)*((mu_30)**2))/((mu_00)**11)
    I5 = ((((mu_20)**3)*mu_30*((mu_03)**3)) - (3*((mu_20)**3)*mu_21*mu_12*((mu_03)**2)) + (2*((mu_20)**3)*((mu_12)**3)*mu_03) - (6*((mu_20)**2)*mu_11*mu_30*mu_12*((mu_03)**2)) + (6*((mu_20)**2)*mu_11*((mu_21*mu_03)**2)) + (6*((mu_20*mu_12)**2)*mu_11*mu_21*mu_03) - (6*((mu_20*((mu_12)**2))**2)*mu_11) + (3*((mu_20*mu_12)**2)*mu_02*mu_30*mu_03) - (6*((mu_20*mu_21)**2)*mu_02*mu_12*mu_03) + (3*((mu_20)**2)*((mu_12)**3)*mu_02*mu_21) + (12*mu_20*mu_30*mu_03*((mu_11*mu_12)**2)) - (24*mu_20*mu_12*mu_03*((mu_11*mu_21)**2)) + (12*mu_20*mu_21*((mu_11*mu_12)**2)*mu_12) - (12*mu_20*mu_11*mu_02*mu_30*((mu_12)**3)) + (12*mu_20*mu_11*mu_02*mu_03*((mu_21)**3)) - (3*mu_20*mu_30*mu_03*((mu_02*mu_21)**2)) + (6*mu_20*mu_30*mu_21*((mu_02*mu_12)**2)) - (3*mu_20*mu_03*((mu_02*mu_21)**2)*mu_21) - (8*mu_30*((mu_11*mu_12)**3)) + (8*mu_03*((mu_11*mu_21)**3)) - (12*mu_02*mu_30*mu_03*((mu_11*mu_21)**2)) + (24*mu_02*mu_30*mu_21*((mu_11*mu_12)**2)) - (12*mu_02*mu_12*mu_21*((mu_21*mu_11)**2)) + (6*mu_11*mu_21*mu_03*((mu_02*mu_30)**2)) - (6*mu_11*((mu_02*mu_30*mu_12)**2)) - (6*mu_11*mu_30*mu_12*((mu_02*mu_21)**2)) + (6*mu_11*((mu_02*((mu_21)**2))**2)) - (mu_03*((mu_02*mu_30)**3)) + (3*mu_02*mu_21*mu_12*((mu_02*mu_30)**2)) - (2*mu_30*((mu_02*mu_21)**3)))/((mu_00)**16)
    I6 = (mu_40*mu_04 - 4*mu_31*mu_13 + 3 * ((mu_22)**2))/((mu_00)**6)
    I7 = ((mu_40*mu_22*mu_04)-(mu_40*((mu_13)**2)) - (((mu_31)**2)*mu_04) + (2*mu_31*mu_22*mu_13) - ((mu_22)**3))/((mu_00)**9)
    I8 = ((mu_04*((mu_20)**2)) - (4*mu_20*mu_11*mu_13) + (2*mu_20*mu_02*mu_22) + (4*mu_22*mu_11*mu_11) - (4*mu_11*mu_02*mu_31) + (mu_40*((mu_02)**2)))/((mu_00)**7)
    I9 = ((mu_22*mu_04*((mu_20)**2)) - ((mu_20*mu_13)**2) - (2*mu_20*mu_11*mu_22*mu_13) + (mu_20*mu_02*mu_40*mu_04) - (2*mu_20*mu_02*mu_31*mu_13) + (mu_20*mu_02*((mu_22)**2)) + (4*mu_31*mu_13*((mu_11)**2)) - (4*((mu_11*mu_22)**2)) - (2*mu_11*mu_02*mu_40*mu_13) + (2*mu_11*mu_02*mu_31*mu_22) + (mu_40*mu_22*((mu_02)**2)) - ((mu_02*mu_31)**2))/((mu_00)**10)
    I10 = ((mu_31*mu_20*((mu_20*mu_04)**2)) - (4*mu_22*mu_13*mu_04*((mu_20)**3)) + (2*((mu_20*mu_13)**3)) - (mu_11*mu_40*((mu_20*mu_04)**2)) - (2*mu_11*mu_31*mu_13*mu_04*((mu_20)**2)) + (9*mu_11*mu_04*((mu_20*mu_22)**2)) - (6*mu_11*mu_22*((mu_20*mu_13)**2)) + (mu_02*mu_40*mu_13*mu_04*((mu_20)**2)) - (3*mu_02*mu_31*mu_22*mu_04*((mu_20)**2)) + (2*mu_02*mu_31*((mu_20*mu_13)**2)) + (4*mu_20*mu_40*mu_13*mu_04*((mu_11)**2)) - (12*mu_20*mu_31*mu_22*mu_04*((mu_11)**2)) + (8*mu_20*mu_31*((mu_11*mu_13)**2)) - (6*mu_20*mu_11*mu_02*mu_40*((mu_13)**2)) + (6*mu_20*mu_11*mu_02*mu_04*((mu_31)**2)) - (mu_20*mu_40*mu_31*mu_04*((mu_02)**2)) + (3*mu_20*mu_40*mu_22*mu_13*((mu_02)**2)) - (2*mu_20*mu_13*((mu_02*mu_31)**2)) - (4*mu_11*mu_40*((mu_11*mu_13)**2)) + (4*mu_11*mu_04*((mu_11*mu_31)**2)) - (4*mu_02*mu_40*mu_31*mu_04*((mu_11)**2)) + (12*mu_02*mu_40*mu_22*mu_13*((mu_11)**2)) - (8*mu_02*mu_13*((mu_11*mu_31)**2)) + (mu_11*mu_04*((mu_02*mu_40)**2)) + (2*mu_11*mu_31*mu_40*mu_13*((mu_02)**2)) - (9*mu_11*mu_40*((mu_02*mu_22)**2)) + (6*mu_11*mu_22*((mu_02*mu_31)**2)) - (mu_02*mu_13*((mu_02*mu_40)**2)) + (3*mu_40*mu_31*mu_22*((mu_02)**3)) - (2*((mu_02*mu_31)**3)))/((mu_00)**15)

    affine_moments = [I1,I2,I3,I4,I5,I6,I7,I8,I9,I10]
    return affine_moments
