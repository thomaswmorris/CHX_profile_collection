from pathlib import PurePath
from datetime import datetime

import numpy as np

from ophyd.areadetector.detectors import AreaDetector
from ophyd.areadetector.cam import AreaDetectorCam
from ophyd.areadetector.paths import EpicsPathSignal
from ophyd.areadetector.base import EpicsSignalWithRBV
from ophyd.areadetector.plugins import StatsPlugin_V34, ROIPlugin_V34
from ophyd.areadetector.filestore_mixins import new_short_uid, FileStoreBase
from ophyd.signal import EpicsSignal
from ophyd import Component as Cpt, Device

from nslsii.ad33 import SingleTriggerV33

class PreciseDtypeSignal(Signal):
    def describe(self):
        ret = super().describe()
        ret[self.name].setdefault('dtype_str',
                                  str(np.asarray(self.get()).dtype)

        )
        return ret

class Tpx3Files(Device):
    # The other PVs only take affect after this is set
    set_settings = Cpt(EpicsSignal, "WriteData", kind="omitted")

    raw_filepath = Cpt(
        EpicsPathSignal,
        "RawFilePath",
        string=True,
        kind="config",
        path_semantics="posix",
    )
    raw_file_template = Cpt(
        EpicsSignalWithRBV, "RawFileTemplate", string=True, kind="config"
    )
    raw_write_enable = Cpt(EpicsSignalWithRBV, "WriteRaw", string=True, kind="omitted")

    img_filepath = Cpt(EpicsSignalWithRBV, "ImgFilePath", kind="config")
    img_file_template = Cpt(EpicsSignalWithRBV, "ImgFileTemplate", kind="config")
    img_write_enable = Cpt(EpicsSignalWithRBV, "WriteImg", kind="omitted")

    prv_filepath = Cpt(EpicsSignal, "PrvImgFilePath", kind="config")
    prv_file_template = Cpt(EpicsSignal, "PrvImgFileTemplate", kind="config")

    prv1_filepath = Cpt(EpicsSignal, "PrvImg1FilePath", kind="config")

    # HACK UNTIL WE GET HANDLERS SET UP
    raw_filepaths = Cpt(PreciseDtypeSignal, kind="normal")

    def __init__(self, *args, **kwargs):
        self.sequence_id_offset = 1
        # This is changed for when a datum is a slice
        # also used by ophyd
        self.filestore_spec = "TPX3_RAW"
        self.frame_num = None
        super().__init__(*args, **kwargs)
        self._datum_kwargs_map = dict()  # store kwargs for each uid
        self._n = 0

    def stage(self):
        # TODO also do the images

        self._res_uid = res_uid = new_short_uid()
        write_path_template = '/nsls2/data/chx/legacy/data/%Y/%m/%d/'
        self._write_path = write_path = datetime.now().strftime(write_path_template)
        self.raw_filepath.set(write_path).wait()

        # TODO check what the % formatting means to the server
        self.raw_file_template.set(f"{res_uid}_0").wait()

        # because we need to flush setting to actual server from IOC
        self.set_settings.set(1).wait()

        # fill in first guess, this ill increment self._n but we really do not want to!
        self.update_file_template()
        # reset this back to 0!  
        self._n = 0

        super().stage()

    def update_file_template(self):
        # The server generates files with in a trigger that are formatted as
        # filepath/template{datetime only}_{j:d6}.tpx3
        # however the counting is only within the trigger and because we want to be able to predict the file names we can not
        # rely on the date formatting, this we need to set this template on every trigger

        
        # TODO check what the % formatting means to the server
        self.raw_file_template.set(f"{self._res_uid}_{self._n}_").wait()
        # because we need to flush setting to actual server from IOC
        self.set_settings.set(1).wait()

        filenames = [f'{self._write_path}{self._res_uid}_{self._n}_{j:06d}.tpx3' for j in range(self.parent.cam.num_images.get())]
        self._n += 1
        self.raw_filepaths.set(filenames).wait()


class TimePixDetector(SingleTriggerV33, AreaDetector):
    _default_configuration_attrs = None
    _default_read_attrs = None

    files = Cpt(Tpx3Files, "cam1:")

    stats1 = Cpt(StatsPlugin_V34, "Stats1:")
    stats2 = Cpt(StatsPlugin_V34, "Stats2:")
    stats3 = Cpt(StatsPlugin_V34, "Stats3:")
    stats4 = Cpt(StatsPlugin_V34, "Stats4:")

    roi1 = Cpt(ROIPlugin_V34, "ROI1:")
    roi2 = Cpt(ROIPlugin_V34, "ROI2:")
    roi3 = Cpt(ROIPlugin_V34, "ROI3:")
    roi4 = Cpt(ROIPlugin_V34, "ROI4:")
    
    def trigger(self):
        self.files.update_file_template()
        return super().trigger()


tpx3 = TimePixDetector("TPX3-TEST:", name="tpx3")

tpx3.stats1.kind = 'normal'
tpx3.stats1.total.kind = 'hinted'

# for j in [1, 2, 3, 4]:
#     getattr(tpx3, f'stats{j}').nd_array_port.set(f'ROI{j}')
