from ophyd.areadetector.detectors import AreaDetector
from ophyd.areadetector.cam import AreaDetectorCam
from ophyd.areadetector.paths import EpicsPathSignal
from ophyd.areadetector.base import EpicsSignalWithRBV
from ophyd.areadetector.plugins import StatsPlugin_V34, ROIPlugin_V34
from ophyd.signal import EpicsSignal
from ophyd import Component as Cpt, Device

from nslsii.ad33 import SingleTriggerV33

class Tpx3Files(Device):

    # The other PVs only take affect after this is set
    set_settings = Cpt(EpicsSignal, 'WriteData', kind='omitted')

    raw_filepath = Cpt(EpicsPathSignal, 'RawFilePath', string=True, kind='config', path_semantics='posix')
    raw_file_template = Cpt(EpicsSignalWithRBV, 'RawFileTemplate', string=True, kind='config')
    raw_write_enable = Cpt(EpicsSignalWithRBV, 'WriteRaw', string=True, kind='omitted') 

    img_filepath = Cpt(EpicsSignalWithRBV, 'ImgFilePath', kind='config')
    img_file_template = Cpt(EpicsSignalWithRBV, 'ImgFileTemplate', kind='config')
    img_write_enable = Cpt(EpicsSignalWithRBV, 'WriteImg', kind='omitted')

    prv_filepath = Cpt(EpicsSignal, 'PrvImgFilePath', kind='config')
    prv_file_template = Cpt(EpicsSignal, 'PrvImgFileTemplate', kind='config')

    prv1_filepath = Cpt(EpicsSignal, 'PrvImg1FilePath', kind='config')

    # def __init__(self, *args, **kwargs):
    #     self.sequence_id_offset = 1
    #     # This is changed for when a datum is a slice
    #     # also used by ophyd
    #     self.filestore_spec = "TPX3_RAW"
    #     self.frame_num = None
    #     super().__init__(*args, **kwargs)
    #     self._datum_kwargs_map = dict()  # store kwargs for each uid

    # def stage(self):
    #     res_uid = new_short_uid()
    #     write_path = datetime.now().strftime(self.write_path_template)
    #     self.img_filepath.set(write_path).wait()
        
    #     set_and_wait(self.file_write_name_pattern, '{}_$id'.format(res_uid))
    #     super().stage()
    #     fn = (PurePath(self.file_path.get()) / res_uid)
    #     ipf = int(self.file_write_images_per_file.get())
    #     # logger.debug("Inserting resource with filename %s", fn)
    #     self._fn = fn
    #     res_kwargs = {'images_per_file' : ipf}
    #     self._generate_resource(res_kwargs)

    # def generate_datum(self, key, timestamp, datum_kwargs):
    #     # The detector keeps its own counter which is uses label HDF5
    #     # sub-files.  We access that counter via the sequence_id
    #     # signal and stash it in the datum.
    #     seq_id = int(self.sequence_id_offset) + int(self.sequence_id.get())  # det writes to the NEXT one
    #     datum_kwargs.update({'seq_id': seq_id})
    #     if self.frame_num is not None:
    #         datum_kwargs.update({'frame_num': self.frame_num})
    #     return super().generate_datum(key, timestamp, datum_kwargs)

    # def describe(self,):
    #     ret = super().describe()
    #     if hasattr(self.parent.cam, 'bit_depth'):
    #         cur_bits = self.parent.cam.bit_depth.get()
    #         dtype_str_map = {8: '|u1', 16: '<u2', 32:'<u4'}
    #         ret[self.parent._image_name]['dtype_str'] = dtype_str_map[cur_bits]
    #     return ret

class TimePixDetector(SingleTriggerV33, AreaDetector):
    _default_configuration_attrs = None
    _default_read_attrs = None 


    files = Cpt(Tpx3Files, 'cam1:')

    stats1 = Cpt(StatsPlugin_V34, 'Stats1:')
    stats2 = Cpt(StatsPlugin_V34, 'Stats2:')
    stats3 = Cpt(StatsPlugin_V34, 'Stats3:')
    stats4 = Cpt(StatsPlugin_V34, 'Stats4:')
    
    roi1 = Cpt(ROIPlugin_V34, 'ROI1:')
    roi2 = Cpt(ROIPlugin_V34, 'ROI2:')
    roi3 = Cpt(ROIPlugin_V34, 'ROI3:')
    roi4 = Cpt(ROIPlugin_V34, 'ROI4:')
    ...

tpx3 = TimePixDetector('TPX3-TEST:', name='tpx3')



# for j in [1, 2, 3, 4]:
#     getattr(tpx3, f'stats{j}').nd_array_port.set(f'ROI{j}')