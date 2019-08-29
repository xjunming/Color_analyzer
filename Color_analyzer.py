# -*- coding: utf-8 -*-

import os
import cv2
import math
import colorsys
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans

class Color_analyzer:
    """A simple color analysis tool"""
    def __init__(self):
        path = './output'
        folder = os.path.exists(path)
        if not folder:os.makedirs(path)
        pass

    def read_file(self, pic_dir, pic_format='tif'):
        file_list = []
        for root, dirs, files in os.walk(pic_dir):
            for file in files:
                if pic_format in file:
                    file_list.append(str(root + '//' + file))
        return file_list

    def hsv2rgb(self, h, s, v):
        h = float(h)
        s = float(s)
        v = float(v)
        h60 = h / 60.0
        h60f = math.floor(h60)
        hi = int(h60f) % 6
        f = h60 - h60f
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        r, g, b = 0, 0, 0
        if hi == 0:
            r, g, b = v, t, p
        elif hi == 1:
            r, g, b = q, v, p
        elif hi == 2:
            r, g, b = p, v, t
        elif hi == 3:
            r, g, b = p, q, v
        elif hi == 4:
            r, g, b = t, p, v
        elif hi == 5:
            r, g, b = v, p, q
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        return r, g, b

    def calculate_means_std(self, img):
        h, s, v = [], [], []
        for raw in range(img.shape[0]):
            for col in range(img.shape[1]):
                r, g, b = self.hsv2rgb(img[raw, col, 0], img[raw, col, 1], img[raw, col, 2])
                if r > 200 and g > 200 and b > 200:  # Skip white pixels
                    continue
                if r < 30 and g < 30 and b < 30: # Skip black pixels
                    continue
                h.append(img[raw, col, 0])
                s.append(img[raw, col, 1])
                v.append(img[raw, col, 2])
        h_means = np.mean(np.array(h))
        h_std = np.std(np.array(h))
        s_means = np.mean(np.array(s))
        s_std = np.std(np.array(s))
        v_means = np.mean(np.array(v))
        v_std = np.std(np.array(v))

        return np.array([h_means, s_means, v_means,
                         h_std, s_std, v_std])

    def mean_std_hsv(self, filename, zoom_in_size):
        img = cv2.imread(filename)
        img = cv2.resize(img, None, fx=1 / zoom_in_size, fy=1 / zoom_in_size)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        return self.calculate_means_std(hsv)

    def feature_extractor(self, pic_dir, pic_format='tif', zoom_in_size=4 , save_npy=False):
        files = self.read_file(pic_dir, pic_format)
        print('There are %s picture(s).'%len(files))

        arr = self.mean_std_hsv(files[0], zoom_in_size=zoom_in_size)
        for img_file in tqdm(files[1:]):
            c = self.mean_std_hsv(img_file, zoom_in_size=zoom_in_size)
            arr = np.vstack((arr, c))
        if save_npy:
            np.save('./output/main_color_array.npy', arr)
        print('Extraction completed.')
        return arr

    def plot_hist(self, feature, savefig=False):
        for i in range(6):
            data = np.array(feature[:, i], dtype=int)
            plt.hist(data, facecolor="blue", edgecolor="black", alpha=0.7)
            plt.ylabel('Frequency')
            if i == 0:
                plt.xlabel('Hue')
                plt.title('Hue means hist')
                if savefig:
                    plt.savefig('./output/Hue_means_hist' + '.png')
                plt.show()
            elif i == 1:
                plt.xlabel('Saturation')
                plt.title('Saturation means hist')
                if savefig:
                    plt.savefig('./output/Saturation_means_hist' + '.png')
                plt.show()
            elif i == 2:
                plt.xlabel('Value')
                plt.title('Value means hist')
                if savefig:
                    plt.savefig('./output/Value_means_hist' + '.png')
                plt.show()
            if i == 3:
                plt.xlabel('Hue std')
                plt.title('Hue std hist')
                if savefig:
                    plt.savefig('./output/Hue_std_hist' + '.png')
                plt.show()
            elif i == 4:
                plt.xlabel('Saturation std')
                plt.title('Saturation std hist')
                if savefig:
                    plt.savefig('./output/Saturation_std_hist' + '.png')
                plt.show()
            elif i == 5:
                plt.xlabel('Value std')
                plt.title('Value std hist')
                if savefig:
                    plt.savefig('./output/Value_std_hist' + '.png')
                plt.show()
            if savefig:
                print('saving in output folder.')

    def plot_3d(self, feature, elev=45, azim=45):
        x, y, z = feature[:, 0], feature[:, 1], feature[:, 2]
        ax = plt.subplot(111, projection='3d')
        ax.scatter(x, y, z)
        ax.view_init(elev=elev, azim=azim)
        ax.set_xlim(0, 180)
        ax.set_ylim(0, 255)
        ax.set_zlim(0, 255)
        plt.show()

class Clustering:
    def __init__(self):
        pass
    def kmeans(self, feature, n_clusters):
        estimator = KMeans(n_clusters=n_clusters)
        estimator.fit(feature)
        label_pred = estimator.labels_
        centroids = estimator.cluster_centers_
        return label_pred


if __name__=='__main__':
    pic_dir = 'E://data//'
    myanalyzer = Color_analyzer()
