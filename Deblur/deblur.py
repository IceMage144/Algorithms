# Questao 3 - MAC0417
# Nome: João Gabriel Basi
# NUSP: 9793801

import os
import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Plots two images, side by side
def plot_pair(name1, img1, name2, img2):
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

    ax[0].set_title(name1)
    ax[0].imshow(img1, cmap='gray', vmin=0, vmax=255)

    ax[1].set_title(name2)
    ax[1].imshow(img2, cmap='gray', vmin=0, vmax=255)

    ax[0].axis('off')
    ax[1].axis('off')
    plt.tight_layout()
    plt.show()

# Rescale the values of a matrix to fit into an unsigned 8-bit integer
def fit_into_uint8(img):
    img_max = img.max()
    img_min = img.min()
    img_i = np.floor(255.0 * ((img - img_min) / (img_max - img_min)))
    return img_i

# Calculates the spectrum of a DFT and normalizes it
def fourier_spectrum(fourier_img):
    spectrum = np.log(1 + np.abs(fourier_img))
    return fit_into_uint8(spectrum)

def create_kernel(kernel_size, kernel_std):
    kernel = cv2.getGaussianKernel(kernel_size, kernel_std)
    kernel = kernel @ kernel.reshape((1, kernel_size))
    return kernel

def resize_image(img, new_size):
    res = np.zeros(new_size)
    m, n = img.shape
    i, j = new_size
    res[(i - m)//2:(i + m)//2, (j - n)//2:(j + n)//2] = img
    return res

def cut_borders(img, border_size):
    m, n = img.shape
    res = img[border_size:m - border_size, border_size:n - border_size]
    return res

def add_blured_borders(img, kernel, border_size):
    m, n = img.shape
    i, j = (m + 2 * border_size, n + 2 * border_size)
    res = np.zeros((i, j))
    res[border_size:i - border_size, border_size:j - border_size] = img
    res = cv2.filter2D(res, -1, kernel)
    res[border_size:i - border_size, border_size:j - border_size] = img
    return res

def test_deblur(img, kernel_size, kernel_std):
    m, n = img.shape
    img_f = resize_image(img, (m + 2 * kernel_size, n + 2 * kernel_size))

    # Blur image
    kernel = create_kernel(kernel_size, kernel_std)
    expanded_kernel = resize_image(kernel, img_f.shape)

    filtered_img = cv2.filter2D(img_f, -1, expanded_kernel)

    # Change these lines and see what happens
    filtered_img_2 = cut_borders(filtered_img, kernel_size//2)
    # filtered_img = cut_borders(filtered_img, kernel_size//2 + 1)

    # Deblur image
    recovered_img = deblur(filtered_img_2, kernel_size, kernel_std)

    plot_pair("Original Image", filtered_img,
              "Recovered image", recovered_img)

def deblur(img, kernel_size, kernel_std):
    m, n = img.shape
    blured_img = resize_image(img, (m + 2 * kernel_size, n + 2 * kernel_size))

    kernel = create_kernel(kernel_size, kernel_std)
    expanded_kernel = resize_image(kernel, blured_img.shape)
    kernel_ft = np.fft.fft2(expanded_kernel)

    blured_img_fft = np.fft.fft2(blured_img)
    recovered_img_fft = blured_img_fft / kernel_ft
    recovered_img = np.real(np.fft.ifft2(recovered_img_fft))
    recovered_img = np.fft.ifftshift(recovered_img)
    recovered_img = cut_borders(recovered_img, kernel_size + 2)

    return recovered_img

def main():
    default_img_path = "leopard.png"
    img_path = ""
    try:
        img_path = sys.argv[1]
    except:
        if not os.path.isfile(default_img_path):
            print("Error: Please put leopard.png in the same directory as this script or pass in a path as first argument".format(img_path))
            return
        img_path = default_img_path
    if not os.path.isfile(img_path):
        print("Error: '{}' does not exists or is not a file".format(img_path))
        return

    img_i = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img_f = img_i.astype(np.float64)

    test_deblur(img_f, 41, 20)
    return
    
    recovered_img = deblur(img_f, 41, 20)

    plot_pair("Original Image", img_f,
              "Recovered image", recovered_img)

if __name__ == "__main__":
    main()
