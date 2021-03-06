#!/usr/bin/python
print('freight - plotting')

import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys
import urllib
import urllib.request

cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"
charts_folder = "5_charts"

try:
    # World Container Index screenshot to pdf / original url = 'https://infogram.com/world-container-index-1h17493095xl4zj'
    api_screenshot_url = 'https://shot.screenshotapi.net/screenshot?token=GYKY2BQ-FQ6MG94-MYYYVY0-G2HPWPG&url=https%3A%2F%2Finfogram.com%2Fworld-container-index-1h17493095xl4zj&fresh=true&output=image&file_type=png&wait_for_event=load'
    png = '002_WCI.png'
    path_png = os.path.join(cwd,input_folder,charts_folder,png)
    urllib.request.urlretrieve(api_screenshot_url, path_png)
    plt.rcParams["figure.figsize"] = (11.69, 8.27) # pdf dimensions
    img = mpimg.imread(path_png)
    g = plt.imshow(img)
    plt.xticks([])
    plt.yticks([])
    plt.box(False)
    #plt.show()
    plt.tight_layout()
    pdf = '002_WCI.pdf'
    path_pdf = os.path.join(cwd,input_folder,charts_folder,pdf)
    plt.savefig(path_pdf
                    , facecolor='#00224B')
    mpl.rc_file_defaults()
    plt.close('all')
except:
    pass


try:
    # Shanghai Containerized Freight Index
    url = 'https://www.sse.net.cn/index/indexImg?name=scfi&type=english'
    png = '003_SCFI.png'
    path_png = os.path.join(cwd,input_folder,charts_folder,png)
    urllib.request.urlretrieve(url, path_png)
    plt.rcParams["figure.figsize"] = (11.69, 8.27) # pdf dimensions
    img = mpimg.imread(path_png)
    g = plt.imshow(img)
    plt.xticks([])
    plt.yticks([])
    plt.box(False)
    #plt.show()
    plt.tight_layout()
    pdf = '002_SCFI.pdf'
    path_pdf = os.path.join(cwd,input_folder,charts_folder,pdf)
    plt.savefig(path_pdf
                    , facecolor='#00224B')
    mpl.rc_file_defaults()
    plt.close('all')
except:
    pass