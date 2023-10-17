"""Use FlanT5 segmentor to segment all of the USPTO database."""

import pickle

from sklearn.utils import gen_batches
from tqdm import tqdm
import torch

from syn2act.segment import SegFlanT5

bs = 64
backup_freq = 250  # backup every 200 epochs (~every hour)

# Load database
with open("data/DATASET_PARAGRAPH_Q2_Q3.pickle", "rb") as f:
    data = list(pickle.load(f))

segment_model = SegFlanT5()

batches = gen_batches(len(data), batch_size=bs)
len_batch = len(data) // bs

try:
    with open("data/uspto_segmented.bin", "rb") as f:
        segm_map = pickle.load(f)
except:
    segm_map = dict()

with open("data/uspto_segmented.bin", "wb") as f:
    for i, batch in enumerate(tqdm(batches, total=len_batch)):
        b = data[batch]
        seg_b = segment_model(b)
        segm_map.update(zip(range(i * bs, (i + 1) * bs), seg_b))

        if i % backup_freq == 0:
            pickle.dump(segm_map, f)
            print(f"Last backup: {i}th epoch. Processed {len(segm_map)} samples so far")
