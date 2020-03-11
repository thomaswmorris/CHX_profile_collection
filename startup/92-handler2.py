import numpy as np
import h5py
from pims import FramesSequence, Frame


class EigerImages2(FramesSequence):
    def __init__(self, master_filepath, images_per_file, *, md=None):
        self._md = md
        self.master_filepath = master_filepath
        self.images_per_file = images_per_file
        self._handle = h5py.File(master_filepath, 'r')
        try:
            self._entry = self._handle['entry']['data']  # Eiger firmware v1.3.0 and onwards
        except KeyError:
            self._entry = self._handle['entry']          # Older firmwares

    @property
    def md(self):
        return self._md

    @property
    def valid_keys(self):
        valid_keys = []
        for key in sorted(self._entry.keys()):
            try:
                self._entry[key]
            except KeyError:
                pass  # This is a link that leads nowhere.
            else:
                valid_keys.append(key)
        return valid_keys

    def get_frame(self, i):
        dataset = self._entry['data_{:06d}'.format(1 + (i // self.images_per_file))]
        img = dataset[i % self.images_per_file]
        return Frame(img, frame_no=i)

    def __len__(self):
        return sum(self._entry[k].shape[0] for k in self.valid_keys)

    @property
    def frame_shape(self):
        return self[0].shape

    @property
    def pixel_type(self):
        return self[0].dtype

    @property
    def dtype(self):
        return self.pixel_type

    @property
    def shape(self):
        return self.frame_shape

    def close(self):
        self._handle.close()
