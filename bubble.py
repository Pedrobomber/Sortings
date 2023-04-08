#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import time
import random
from tqdm import tqdm
import matplotlib.pyplot as plt

sort_name = 'Bubble Sort'

# In[17]:


imgs_dir = 'images'
os.makedirs(imgs_dir, exist_ok=True)
os.system(f'rm -rf {imgs_dir}/*.jpg')

def make_frame(arr, i=0, time=0, last_swap=None):
	dpi = 300
	fig, ax = plt.subplots(figsize=(1920/dpi, 1080/dpi), dpi=dpi)
	ax.set_xlim(0, 100)
	ax.set_ylim(0, 100)
	ax.set_title(sort_name)
	ax.set_xticks([])
	ax.set_yticks([])
	barlist = ax.bar(range(len(arr)), arr)
	if last_swap:
		barlist[last_swap[0]].set_color('black')
		barlist[last_swap[1]].set_color('red')
	txt_str = f'Swap #{i}\nElapsed time: {time:.5f} s'
	ax.text(1, 103, txt_str, fontsize=10, bbox=dict(facecolor='white'))

	fig.savefig(f'{imgs_dir}/frame_{i}.jpg')
	plt.close('all')
    

# In[ ]:


arr = list(range(100))
random.shuffle(arr)

frame_num = 0
n = len(arr)
# optimize code, so if the array is already sorted, it doesn't need
# to go through the entire process
swapped = False
# Traverse through all array elements

save_time = 0
elapsed_time = 0
start_time = time.time()

for i in tqdm(range(n-1)):
	# range(n) also work but outer loop will
	# repeat one time more than needed.
	# Last i elements are already in place
	for j in tqdm(range(0, n-i-1), leave=False):
		# traverse the array from 0 to n-i-1
		# Swap if the element found is greater
		# than the next element
		if arr[j] > arr[j + 1]:
			start_save = time.time()
			elapsed_time = time.time() - start_time - save_time
			make_frame(arr, frame_num, elapsed_time, last_swap=(j, j+1))
			save_time += time.time() - start_save
			frame_num += 1
			swapped = True
			arr[j], arr[j + 1] = arr[j + 1], arr[j]


# In[5]:


os.makedirs('videos', exist_ok=True)
os.system(f"ffmpeg -f image2 -r 60 -i ./images/frame_%d.jpg -vcodec mpeg4 -y -b:v 12M ./videos/\"{sort_name}\".mp4")

