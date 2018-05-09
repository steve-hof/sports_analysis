#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib as mpl
import matplotlib.animation as animation
import json


# Animation function / loop
def draw_court(ax):
    img = mpimg.imread('scraped_data/nba_court_T.png')  # read image. I got this image from gmf05's github.
    # didn't get very far today, haha
    pass


def main():
    json_data = open('/Users/stevehof/school/comp/fun/Winning_in_Sports_with_Data/'
                     'NBA/scraped_data/sports_vu_2016.json')
    data = json.load(json_data)


if __name__ == '__main__':
    main()
