import os
import time
import random
from tqdm import tqdm
import matplotlib.pyplot as plt

sort_name = 'Merge Sort'


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

def merge(arr, l, m, r):
	n1 = m - l + 1
	n2 = r - m

	# create temp arrays
	L = [0] * (n1)
	R = [0] * (n2)

	# Copy data to temp arrays L[] and R[]
	for i in range(0, n1):
		L[i] = arr[l + i]

	for j in range(0, n2):
		R[j] = arr[m + 1 + j]

	# Merge the temp arrays back into arr[l..r]
	i = 0	 # Initial index of first subarray
	j = 0	 # Initial index of second subarray
	k = l	 # Initial index of merged subarray

	while i < n1 and j < n2:
		if L[i] <= R[j]:
			arr[k] = L[i]
			i += 1
		else:
			arr[k] = R[j]
			j += 1
		k += 1
		

	# Copy the remaining elements of L[], if there
	# are any
	while i < n1:
		arr[k] = L[i]
		i += 1
		k += 1

	# Copy the remaining elements of R[], if there
	# are any
	while j < n2:
		arr[k] = R[j]
		j += 1
		k += 1

# l is for left index and r is right index of the
# sub-array of arr to be sorted


def mergeSort(arr, l, r, bar):
	global frame
	global save_time
	global elapsed_time

	if l < r:
		# Same as (l+r)//2, but avoids overflow for
		# large l and h
		m = l+(r-l)//2

		# Sort first and second halves
		mergeSort(arr, l, m, bar)
		mergeSort(arr, m+1, r, bar)
		merge(arr, l, m, r)
		bar.update(1)

	start_save = time.time()
	elapsed_time = time.time() - start_time - save_time
	make_frame(arr, frame, elapsed_time, last_swap=(l, r))
	frame += 1
	save_time += time.time() - start_save


# Driver code to test above
arr = list(range(100))
random.shuffle(arr)
n = len(arr)
bar = tqdm(total=n)

start_time = time.time()
save_time = 0
elapsed_time = 0
frame = 0

mergeSort(arr, 0, n-1, bar)


os.makedirs('videos', exist_ok=True)
os.system(f"ffmpeg -loglevel panic -f image2 -r 60 -i ./images/frame_%d.jpg -vcodec mpeg4 -y -b:v 12M ./videos/\"{sort_name}\".mp4")

