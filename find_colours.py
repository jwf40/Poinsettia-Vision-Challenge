# Template to grade the submission for colour counting.
# Fill out the blank area below "output_csv" function.
# Graders will simply run this file expecting the participants to call their 
# relevant python module from the "output_csv" function below. Therefore, 
# your submitted zip file must include this template as well. 
# Specifically, the graders will simply run the following command for evaluation: 
# "$ python find_colours.py Evaluation_Img_Dir" and will expect "colour_results.csv" 
# to be produced as output.
#
# PLEASE DO NOT change the file name of this template or anything else than the blank 
# you fill out.

from __future__ import division
from skimage import io
import numpy as np
import cv2
from sklearn.cluster import KMeans
from skimage.io import imread, imsave,imshow
from matplotlib.image import imread
from matplotlib import pyplot as plt
import csv
import glob
import os
import sys

def output_csv(img_paths, csv_path): 

    #declare variables
    count_red = 0
    count_green = 0
    count_i = 0
    n_colors = 2
    kernel = np.ones((5,5),np.uint8)
    result = []


    #process all images
    for img in img_paths:
        count_i = count_i + 1
        n = cv2.imread(img)
        print(count_i)

        sample_img = cv2.imread(img)
        cv_image1 = cv2.imread(img,1)
        cv_image2 = cv2.imread(img,1)
        
        sample_img = cv2.cvtColor(sample_img, cv2.COLOR_BGR2RGB)
        cv_image1 = cv2.cvtColor(cv_image1, cv2.COLOR_BGR2RGB)
        cv_image2 = cv2.cvtColor(cv_image2, cv2.COLOR_BGR2RGB)

        #store image name
        image_name = img

        #K Means Clustering to Classify Colours
        w,h,_ = sample_img.shape
        sample_img = sample_img.reshape(w*h,3)
        
        kmeans = KMeans(n_clusters=n_colors, random_state=0).fit(sample_img)

        # find out which cluster each pixel belongs to.
        labels = kmeans.predict(sample_img)

        # the cluster centroids is our color palette
        identified_palette = np.array(kmeans.cluster_centers_).astype(int)

        # recolor the entire image
        recolored_img = np.copy(sample_img)
        for index in range(len(recolored_img)):
            recolored_img[index] = identified_palette[labels[index]]
            
        # reshape for display
        recolored_img = recolored_img.reshape(w,h,3)

        #red mask
        low_red = np.array([100,0,0]) 
        high_red = np.array([255,70,70])
        red_mask = cv2.inRange(recolored_img, low_red, high_red)

        #green mask
        low_green = np.array([0,0,0]) 
        high_green = np.array([90,90,90])
        green_mask = cv2.inRange(recolored_img, low_green, high_green)
            
        #Process Images with Red and Green Masks
        cv_image1[red_mask>0]=(255,0,0)
        cv_image2[green_mask>0]=(0,255,0)

        #Red and Green Highlighted in the Original Image
        imsave('red_sample.jpg',cv_image1)
        imsave('green_sample.jpg',cv_image2)

        #Count the Number Red and Green of Pixels
        (row, col,depth) = cv_image1.shape

        for r in xrange(row):
            for c in xrange(col):
                if red_mask[r][c] > 0:
                    count_red = count_red+1
                if green_mask[r][c] > 0:
                    count_green = count_green+1


        #Total Number of Pixels
        total_pixel = row * col

        #Percentage of Red Pixels in the Image
        pct_red = count_red/total_pixel

        #Percentage of Green Pixels in the Image
        pct_green = count_green/total_pixel

        #Red Pixels to Green Pixels ratio 9Number of Red Pixels/Number of Green Pixels
        if pct_green !=0:
            rg_ratio = float(pct_red/pct_green)
        else:
            rg_ratio = 'indeterminable'

        #Append the Results to a list
        result.append([image_name,total_pixel,count_red,count_green,'',pct_red,pct_green,rg_ratio])
        print(result)

        #Write into a csv file
        with open(csv_path,'w') as out:
            csv_out=csv.writer(out)
            csv_out.writerow(['image_name','total_pixels','red_pixels','green_pixels','','pct_red','pct_green','rg_ratio'])
            for row in result:
                csv_out.writerow(row)

        #Reset Red and Green Pixel Counters
        count_red = 0
        count_green = 0


def main(in_dir):
    #in_dir = EvaluationImg_Dir
    print(in_dir)
    print('sea-of-plants/images/'.format(in_dir))
    img_paths = glob.glob(os.path.join(in_dir, '*.jpg'))
    img_paths.sort()
    print('sea-of-plants/images/'.format(len(img_paths)))

    output_csv(img_paths, 'colour_results.csv')
    print('Done')


if __name__ == "__main__":
    main(sys.argv[1])

