# For more detail and derivation of the regenerative morphhing method please refer to
# "Regenerative Morphing" https://grail.cs.washington.edu/projects/regenmorph/
# "Summarizing Visual Data with Bidirectional Simiarlty"
# http://www.wisdom.weizmann.ac.il/~vision/VisualSummary/bidirectional_similarity_CVPR2008.pdf

# This file is modified from regenerative_morph.py
# and get rid of the vectorization in some routines

import numpy as np
import matplotlib.pyplot as plt
import cv2

import time
import profile

# This is a helper function to tranform a matrix into smaller patches
# It was originally a Matlab command, and having it in Python would greatly help performance
# Reference: https://stackoverflow.com/questions/30109068/implement-matlabs-im2col-sliding-in-python
def im2col_sliding_strided(A, BSZ, stepsize=1):
    
    m,n = A.shape
    s0, s1 = A.strides    
    nrows = m-BSZ[0]+1
    ncols = n-BSZ[1]+1
    shp = BSZ[0],BSZ[1],nrows,ncols
    strd = s0,s1,s0,s1

    out_view = np.lib.stride_tricks.as_strided(A, shape=shp, strides=strd)

    return out_view.reshape(BSZ[0]*BSZ[1],-1)[:,::stepsize]


# This is a helper function to create patches of a colored image
# It first separately creates patches in each color channel,
# then combines all R/G/B patches into one colored patch
def create_patches(image, w):

    r = im2col_sliding_strided(image[:,:,0], (w,w))
    g = im2col_sliding_strided(image[:,:,1], (w,w))
    b = im2col_sliding_strided(image[:,:,2], (w,w))
    
    h,w = r.shape
    patches = np.zeros((h,w,3))
    patches[:,:,0] = r
    patches[:,:,1] = g
    patches[:,:,2] = b
    
    return patches


# This function is to compare one patch to the other image
# It returns the index of the patch with the least SSD
# This function has been modified
def patch_match(image_patches, patch):

    _, n_patches, _ = image_patches.shape
    min_ssd = np.inf
    ssd_list = []

    for k in range(n_patches):
        image = image_patches[:,k,:]
        ssd = np.sum(np.sum(np.square(image - patch),axis=0))
        ssd_list.append(ssd)
        
    # Find the minimum ssd and the corresponding idx
    min_ssd = min(ssd_list)
    min_idx = list(ssd_list).index(min_ssd)
    min_patch = image_patches[:,min_idx,:]
    
    # Return the minimum ssd, idx and the patch
    return min_patch, min_idx, min_ssd


# This is a helper function that convert coordinate with patch indices
def idx2patch(pos, image, w, n_patches):
    
    x,y = pos
    nnp_idx = []
    
    xx = x-(w-1)
    yy = y-(w-1)
    
    for k in range(w):
        for kk in range(w):
            nnp_idx.append(int((yy+k)*np.sqrt(n_patches)+xx+kk))
    
    return nnp_idx


# This function is to get the pixel value of S(p)
# pixelpos: the position of the pixel q in the target
# target_idx: the index of the target patch that contains q (nnp_idx here)
def pixel_cohere(pixelpos, target_idx, source_coher_dict, nnp_idx, w, N_T):
    
    W = np.sqrt(N_T) # the number of patches per row
    # Find the position of the top-left corner of the target patch (a,b)
    a = target_idx % W
    b = (target_idx-a) / W
    # Convert (i,j) to the relative pos on the target patch (ai,bj)
    ai = pixelpos[0] - a
    bj = pixelpos[1] - b
    
    relative_idx = int(bj*w+ai)# calculate S(p)
    source_cohere = source_coher_dict[nnp_idx][0]
    sp = source_cohere[relative_idx,:]
    
    return sp


# This function is to get the pixel value of S_hat(p)
# pixelpos: the position of the pixel q in the target
# target_idx: the index of the target patch that contains q (nnp_idx here)
def pixel_complete(pixelpos, target_idx, source_complete_dict, target_complete_dict, source_patches, nnp_idx, w, N_T):
    
    W = np.sqrt(N_T) # the number of patches per row
    # Find the position of the top-left corner of the target patch (a,b)
    a = target_idx % W
    b = (target_idx-a) / W
    # Convert (i,j) to the relative pos on the target patch (ai,bj)
    ai = pixelpos[0] - a
    bj = pixelpos[1] - b
    
    relative_idx = int(bj*w+ai)
    # Calculate S_hat(p)    
    try:
        source_complete_idx = list(target_complete_dict.keys())[list(target_complete_dict.values()).index(nnp_idx)]
        source_complete = source_patches[:,source_complete_idx,:]
        sp_hat = source_complete[relative_idx,:]
    except ValueError:
        sp_hat = np.zeros(3)
    
    return sp_hat


# This function implements a simplified version of the regenerative morphing paper
def target2sources(source1, source2, target, w):

    # Step 1: create patches based on patch size
    source1_patches = create_patches(source1, w)
    N_S1 = source1_patches.shape[1]
    source2_patches = create_patches(source2, w)
    N_S2 = source2_patches.shape[1]
    target_patches = create_patches(target, w)
    N_T = target_patches.shape[1]

    _, n_patches, _ = target_patches.shape

    # Step 2: T and S_1
    # Create d_complete
    source1_complete_dict = {}
    target1_complete_dict = {} # this is for calculating the pixel value
    for source1_idx in range(n_patches):
        source1_patch = source1_patches[:,source1_idx,:]
        target_patch, target_idx, ssd = patch_match(target_patches, source1_patch)
        source1_complete_dict[source1_idx] = [target_patch, target_idx, ssd]
        target1_complete_dict[source1_idx] = target_idx

    # Create d_cohere
    source1_coher_dict = {}
    for target_idx in range(n_patches):
        target_patch = target_patches[:,target_idx,:]
        source1_patch, source1_idx, ssd = patch_match(source1_patches, target_patch)
        source1_coher_dict[target_idx] = [source1_patch, source1_idx, ssd]
        
    # Step 3: T and S_2
    # Create d_complete
    source2_complete_dict = {}
    target2_complete_dict = {} # this is for calculating the pixel value
    for source2_idx in range(n_patches):
        source2_patch = source2_patches[:,source2_idx,:]
        target_patch, target_idx, ssd = patch_match(target_patches, source2_patch)
        source2_complete_dict[source2_idx] = [target_patch, target_idx, ssd]
        target2_complete_dict[source2_idx] = target_idx

    # Create d_cohere
    source2_coher_dict = {}
    for target_idx in range(n_patches):
        target_patch = target_patches[:,target_idx,:]
        source2_patch, source2_idx, ssd = patch_match(source2_patches, target_patch)
        source2_coher_dict[target_idx] = [source2_patch, source2_idx, ssd]

    # Step 4: find the neighboring patches index of each pixel
    target_idx2patch_dict = {}
    width,height,_ = target.shape

    # TODO: account for boundary buffer cases
    for j in range(w-1, height-w):
        for i in range(w-1, width-w):
            pos = (i,j)
            nnp_idxs = idx2patch(pos, target, w, n_patches)
            target_idx2patch_dict[j*width+i] = nnp_idxs

    source1_idx2patch_dict = {}
    width,height,_ = source1.shape

    # TODO: account for boundary buffer cases
    for j in range(w-1, height-w):
        for i in range(w-1, width-w):
            pos = (i,j)
            nnp_idxs = idx2patch(pos, source1, w, n_patches)
            source1_idx2patch_dict[j*width+i] = nnp_idxs
            
    source2_idx2patch_dict = {}
    width,height,_ = source2.shape

    # TODO: account for boundary buffer cases
    for j in range(w-1, height-w):
        for i in range(w-1, width-w):
            pos = (i,j)
            nnp_idxs = idx2patch(pos, source2, w, n_patches)
            source2_idx2patch_dict[j*width+i] = nnp_idxs

    # Step 5: update pixel values in target
    # TODO: account for boundary buffer cases
    for j in range(w-1, height-w):
        for i in range(w-1, width-w):
            pixel = target[j,i]
            pixelpos = (i,j)
            # Get nearest neighboring patches id
            nnp_idxs = idx2patch(pixelpos,target, w, n_patches)
            
            n1,n2,m1,m2 = 0,0,0,0
            sp1_hat,sp2_hat,sp1,sp2 = np.zeros(3),np.zeros(3),np.zeros(3),np.zeros(3)
            for nnp_idx in nnp_idxs:
                # Corresponding path in source1 for complete
                ssp1_hat = pixel_complete(pixelpos, nnp_idx, source1_complete_dict, target1_complete_dict, source1_patches, nnp_idx, w, N_T)
                sp1_hat += ssp1_hat
                if np.sum(ssp1_hat) != 0.0:
                    n1 += 1  
                    
                # Corresponding patch in source2 for complete            
                ssp2_hat = pixel_complete(pixelpos, nnp_idx, source2_complete_dict, target2_complete_dict, source2_patches, nnp_idx, w, N_T)
                sp2_hat += ssp2_hat
                if np.sum(ssp2_hat) != 0.0:
                    n2 += 1
                
                # Corresponding patch in source1 for cohere
                ssp1 = pixel_cohere(pixelpos, nnp_idx, source1_coher_dict, nnp_idx, w, N_T)
                ssd1 = source1_coher_dict[nnp_idx][2]
                sp1 += ssp1
                m1 += 1
                
                # Corresponding patch in source2 for cohere
                ssp2 = pixel_cohere(pixelpos, nnp_idx, source2_coher_dict, nnp_idx, w, N_T)
                ssd2 = source2_coher_dict[nnp_idx][2]
                sp2 += ssp2
                m2 += 1
            
            if n1 != 0:
                pixel3 = (sp1_hat/N_S1) / (n1/N_S1)
            else:
                pixel3 = np.array((255.,255.,255.))
            if n2 != 0:
                pixel4 = (sp2_hat/N_S2) / (n2/N_S2)
            else:
                pixel4 = np.array((255.,255.,255.))
            if ssd1<ssd2:
                pixel5 = (sp1/N_T) / (m1/N_T)
            else:
                pixel5 = (sp2/N_T) / (m2/N_T)
                
            _alpha = 0.5
            _beta = 1.25
            w3 = _beta*_alpha
            w4 = _beta - w3
            w5 = _beta
                
            target_q = (w3*pixel3+w4*pixel4+w5*pixel5) / (w3+w4+w5)
            target[j,i,:] = target_q
            
    return target


def regenerative_morph(source1, source2, target, ws, alpha):

    for w in ws:
        newtarget = target2sources(source1, source2, target, w)
        target = newtarget.copy()

    plt.imshow(target.astype('uint8'))
    plt.axis('off')
    plt.savefig('images/outputs/frame55_slow.png')
    plt.close()
    
    return target

print("\nCreating Frame 55")

source1 = cv2.imread('images/inputs/frame50.png')[...,::-1]
source2 = cv2.imread('images/inputs/frame60.png')[...,::-1]
ref = cv2.imread('images/references/frame55.png')[...,::-1]
ws = [3, 5, 7]
target = 0.5*source1 + 0.5*source2

start = time.time()
# morph = regenerative_morph(source1, source2, target, ws, 0.5)
profile.run('morph = regenerative_morph(source1, source2, target, ws, 0.5)')
end = time.time()
print('Time elapsed: %.4f s.' % (end - start))

f, axes = plt.subplots(1,4, figsize=(15,4))


axes[0].imshow(source1.astype('uint8'))
axes[0].title.set_text('Frame 50')
axes[0].axis('off')

axes[1].imshow(source2.astype('uint8'))
axes[1].title.set_text('Frame 60')
axes[1].axis('off')

axes[2].imshow(morph.astype('uint8'))
axes[2].title.set_text('Frame 55 (Morphed)')
axes[2].axis('off')

axes[3].imshow(ref.astype('uint8'))
axes[3].title.set_text('Frame 55 (Reference)')
axes[3].axis('off')

plt.show()
f.savefig('images/outputs/full_output_slow.png')