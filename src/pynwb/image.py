from .base import TimeSeries, _default_resolution, _default_conversion
from .core import docval, popargs, NWBContainer

import numpy as np
from collections import Iterable


class ImageSeries(TimeSeries):
    '''
    General image data that is common between acquisition and stimulus time series.
    The image data can be stored in the HDF5 file or it will be stored as an external image file.
    '''

    __nwbfields__ = ('bits_per_pixel',
                     'dimension',
                     'external_file',
                     'starting_frame',
                     'format')

    _ancestry = "TimeSeries,ImageSeries"
    _help = "Storage object for time-series 2-D image data"

    @docval({'name': 'name', 'type': str, 'doc': 'The name of this TimeSeries dataset'},
            {'name': 'source', 'type': str, 'doc': ('Name of TimeSeries or Modules that serve as the source for the data '
                                                   'contained here. It can also be the name of a device, for stimulus or '
                                                   'acquisition data')},
            {'name': 'data', 'type': (list, np.ndarray, TimeSeries), 'doc': 'The data this TimeSeries dataset stores. Can also store binary data e.g. image frames'},
            {'name': 'unit', 'type': str, 'doc': 'The base unit of measurement (should be SI unit)'},

            {'name': 'external_file', 'type': Iterable, 'doc': 'Path or URL to one or more external file(s). Field only present if format=external. Either external_file or data must be specified, but not both.'},
            {'name': 'starting_frame', 'type': Iterable, 'doc': 'Each entry is the frame number in the corresponding external_file variable. This serves as an index to what frames each file contains.'},
            {'name': 'format', 'type': str, 'doc': 'Format of image. Three types: 1) Image format; tiff, png, jpg, etc. 2) external 3) raw.'},
            {'name': 'bits_per_pixel', 'type': float, 'doc': 'Number of bit per image pixel', 'default': np.nan},
            {'name': 'dimension', 'type': Iterable, 'doc': 'Number of pixels on x, y, (and z) axes.', 'default': [np.nan]},

            {'name': 'resolution', 'type': float, 'doc': 'The smallest meaningful difference (in specified unit) between values in data', 'default': _default_resolution},
            {'name': 'conversion', 'type': float, 'doc': 'Scalar to multiply each element by to conver to volts', 'default': _default_conversion},

            {'name': 'timestamps', 'type': (list, np.ndarray, TimeSeries), 'doc': 'Timestamps for samples stored in data', 'default': None},
            {'name': 'starting_time', 'type': float, 'doc': 'The timestamp of the first sample', 'default': None},
            {'name': 'rate', 'type': float, 'doc': 'Sampling rate in Hz', 'default': None},

            {'name': 'comments', 'type': str, 'doc': 'Human-readable comments about this TimeSeries dataset', 'default':None},
            {'name': 'description', 'type': str, 'doc': 'Description of this TimeSeries dataset', 'default':None},
            {'name': 'control', 'type': Iterable, 'doc': 'Numerical labels that apply to each element in data', 'default': None},
            {'name': 'control_description', 'type': Iterable, 'doc': 'Description of each control value', 'default': None},
            {'name': 'parent', 'type': 'NWBContainer', 'doc': 'The parent NWBContainer for this NWBContainer', 'default': None},
    )
    def __init__(self, **kwargs):
        name, source, data, unit = popargs('name', 'source', 'data', 'unit', kwargs)
        bits_per_pixel, dimension, external_file, starting_frame, format = popargs('bits_per_pixel', 'dimension', 'external_file', 'starting_frame', 'format', kwargs)
        super(ImageSeries, self).__init__(name, source, data, unit, **kwargs)
        self.bits_per_pixel = bits_per_pixel
        self.dimension = dimension
        self.external_file = external_file
        self.starting_frame = starting_frame
        self.format = format


class IndexSeries(TimeSeries):
    '''
    Stores indices to image frames stored in an ImageSeries. The purpose of the ImageIndexSeries is to allow
    a static image stack to be stored somewhere, and the images in the stack to be referenced out-of-order.
    This can be for the display of individual images, or of movie segments (as a movie is simply a series of
    images). The data field stores the index of the frame in the referenced ImageSeries, and the timestamps 
    array indicates when that image was displayed.
    '''

    __nwbfields__ = ('index_timeseries',
                     'index_timeseries_path')

    _ancestry = "TimeSeries,IndexSeries"
    _help = "A sequence that is generated from an existing image stack. Frames can be presented in an arbitrary order. The data[] field stores frame number in reference stack."

    @docval({'name': 'name', 'type': str, 'doc': 'The name of this TimeSeries dataset'},
            {'name': 'source', 'type': str, 'doc': ('Name of TimeSeries or Modules that serve as the source for the data '
                                                   'contained here. It can also be the name of a device, for stimulus or '
                                                   'acquisition data')},
            {'name': 'data', 'type': (list, np.ndarray, TimeSeries), 'doc': 'The data this TimeSeries dataset stores. Can also store binary data e.g. image frames'},
            {'name': 'unit', 'type': str, 'doc': 'The base unit of measurement (should be SI unit)'},

            {'name': 'index_timeseries', 'type': TimeSeries, 'doc': 'HDF5 link to TimeSeries containing images that are indexed.'},
            {'name': 'index_timeseries_path', 'type': str, 'doc': 'Path to linked TimerSeries.'},

            {'name': 'resolution', 'type': float, 'doc': 'The smallest meaningful difference (in specified unit) between values in data', 'default': _default_resolution},
            {'name': 'conversion', 'type': float, 'doc': 'Scalar to multiply each element by to conver to volts', 'default': _default_conversion},

            {'name': 'timestamps', 'type': (list, np.ndarray, TimeSeries), 'doc': 'Timestamps for samples stored in data', 'default': None},
            {'name': 'starting_time', 'type': float, 'doc': 'The timestamp of the first sample', 'default': None},
            {'name': 'rate', 'type': float, 'doc': 'Sampling rate in Hz', 'default': None},

            {'name': 'comments', 'type': str, 'doc': 'Human-readable comments about this TimeSeries dataset', 'default':None},
            {'name': 'description', 'type': str, 'doc': 'Description of this TimeSeries dataset', 'default':None},
            {'name': 'control', 'type': Iterable, 'doc': 'Numerical labels that apply to each element in data', 'default': None},
            {'name': 'control_description', 'type': Iterable, 'doc': 'Description of each control value', 'default': None},
            {'name': 'parent', 'type': 'NWBContainer', 'doc': 'The parent NWBContainer for this NWBContainer', 'default': None},
    )
    def __init__(self, **kwargs):
        name, source, data, unit = popargs('name', 'source', 'data', 'unit', kwargs)
        index_timeseries, index_timeseries_path = popargs('index_timeseries', 'index_timeseries_path', kwargs)
        super(IndexSeries, self).__init__(name, source, data, unit, **kwargs)
        self.index_timeseries = index_timeseries
        self.index_timeseries_path = index_timeseries_path

class ImageMaskSeries(ImageSeries):
    '''
    An alpha mask that is applied to a presented visual stimulus. The data[] array contains an array
    of mask values that are applied to the displayed image. Mask values are stored as RGBA. Mask 
    can vary with time. The timestamps array indicates the starting time of a mask, and that mask
    pattern continues until it's explicitly changed.
    '''

    __nwbfields__ = ('masked_imageseries',
                     'masked_imageseries_path')

    _ancestry = "TimeSeries,ImageSeries,ImageMaskSeries"
    _help = "An alpha mask that is applied to a presented visual stimulus."

    @docval({'name': 'name', 'type': str, 'doc': 'The name of this TimeSeries dataset'},
            {'name': 'source', 'type': str, 'doc': ('Name of TimeSeries or Modules that serve as the source for the data '
                                                   'contained here. It can also be the name of a device, for stimulus or '
                                                   'acquisition data')},
            {'name': 'data', 'type': (list, np.ndarray, TimeSeries), 'doc': 'The data this TimeSeries dataset stores. Can also store binary data e.g. image frames'},
            {'name': 'unit', 'type': str, 'doc': 'The base unit of measurement (should be SI unit)'},

            {'name': 'masked_imageseries', 'type': ImageSeries, 'doc': 'Link to ImageSeries that mask is applied to.'},
            {'name': 'masked_imageseries_path', 'type': str, 'doc': 'Path to linked ImageSeries.'},

            {'name': 'external_file', 'type': Iterable, 'doc': 'Path or URL to one or more external file(s). Field only present if format=external. Either external_file or data must be specified, but not both.'},
            {'name': 'starting_frame', 'type': Iterable, 'doc': 'Each entry is the frame number in the corresponding external_file variable. This serves as an index to what frames each file contains.'},
            {'name': 'format', 'type': str, 'doc': 'Format of image. Three types: 1) Image format; tiff, png, jpg, etc. 2) external 3) raw.'},
            {'name': 'bits_per_pixel', 'type': float, 'doc': 'Number of bit per image pixel', 'default': np.nan},
            {'name': 'dimension', 'type': Iterable, 'doc': 'Number of pixels on x, y, (and z) axes.', 'default': [np.nan]},

            {'name': 'resolution', 'type': float, 'doc': 'The smallest meaningful difference (in specified unit) between values in data', 'default': _default_resolution},
            {'name': 'conversion', 'type': float, 'doc': 'Scalar to multiply each element by to conver to volts', 'default': _default_conversion},

            {'name': 'timestamps', 'type': (list, np.ndarray, TimeSeries), 'doc': 'Timestamps for samples stored in data', 'default': None},
            {'name': 'starting_time', 'type': float, 'doc': 'The timestamp of the first sample', 'default': None},
            {'name': 'rate', 'type': float, 'doc': 'Sampling rate in Hz', 'default': None},

            {'name': 'comments', 'type': str, 'doc': 'Human-readable comments about this TimeSeries dataset', 'default':None},
            {'name': 'description', 'type': str, 'doc': 'Description of this TimeSeries dataset', 'default':None},
            {'name': 'control', 'type': Iterable, 'doc': 'Numerical labels that apply to each element in data', 'default': None},
            {'name': 'control_description', 'type': Iterable, 'doc': 'Description of each control value', 'default': None},
            {'name': 'parent', 'type': 'NWBContainer', 'doc': 'The parent NWBContainer for this NWBContainer', 'default': None},
    )
    def __init__(self, **kwargs):
        name, source, data, unit, external_file, starting_frame, format = popargs('name', 'source', 'data', 'unit', 'external_file', 'starting_frame', 'format', kwargs)
        masked_imageseries, masked_imageseries_path = popargs('masked_imageseries', 'masked_imageseries_path', kwargs)
        super(ImageMaskSeries, self).__init__(name, source, data, unit, external_file, starting_frame, format, **kwargs)
        self.masked_imageseries = masked_imageseries
        self.masked_imageseries_path = masked_imageseries_path

class OpticalSeries(ImageSeries):
    '''
    Image data that is presented or recorded. A stimulus template movie will be stored only as an 
    image. When the image is presented as stimulus, additional data is required, such as field of
    view (eg, how much of the visual field the image covers, or how what is the area of the target 
    being imaged). If the OpticalSeries represents acquired imaging data, orientation is also
    important.
    '''

    __nwbfields__ = ('distance',
                     'field_of_view',
                     'orientation')

    _ancestry = "TimeSeries,ImageSeries,OpticalSeries"
    _help = "Time-series image stack for optical recording or stimulus."

    @docval({'name': 'name', 'type': str, 'doc': 'The name of this TimeSeries dataset'},
            {'name': 'source', 'type': str, 'doc': ('Name of TimeSeries or Modules that serve as the source for the data '
                                                   'contained here. It can also be the name of a device, for stimulus or '
                                                   'acquisition data')},
            {'name': 'data', 'type': (list, np.ndarray, TimeSeries), 'doc': 'The data this TimeSeries dataset stores. Can also store binary data e.g. image frames'},
            {'name': 'unit', 'type': str, 'doc': 'The base unit of measurement (should be SI unit)'},

            {'name': 'distance', 'type': float, 'doc': 'Distance from camera/monitor to target/eye.'},
            {'name': 'field_of_view', 'type': (list, np.ndarray, 'TimeSeries'), 'doc': 'Width, height and depth of image, or imaged area (meters).'},
            {'name': 'orientation', 'type': str, 'doc': 'Description of image relative to some reference frame (e.g., which way is up). Must also specify frame of reference.'},

            {'name': 'external_file', 'type': Iterable, 'doc': 'Path or URL to one or more external file(s). Field only present if format=external. Either external_file or data must be specified, but not both.'},
            {'name': 'starting_frame', 'type': Iterable, 'doc': 'Each entry is the frame number in the corresponding external_file variable. This serves as an index to what frames each file contains.'},
            {'name': 'format', 'type': str, 'doc': 'Format of image. Three types: 1) Image format; tiff, png, jpg, etc. 2) external 3) raw.'},
            {'name': 'bits_per_pixel', 'type': float, 'doc': 'Number of bit per image pixel', 'default': np.nan},
            {'name': 'dimension', 'type': Iterable, 'doc': 'Number of pixels on x, y, (and z) axes.', 'default': [np.nan]},

            {'name': 'resolution', 'type': float, 'doc': 'The smallest meaningful difference (in specified unit) between values in data', 'default': _default_resolution},
            {'name': 'conversion', 'type': float, 'doc': 'Scalar to multiply each element by to conver to volts', 'default': _default_conversion},

            {'name': 'timestamps', 'type': (list, np.ndarray, TimeSeries), 'doc': 'Timestamps for samples stored in data', 'default': None},
            {'name': 'starting_time', 'type': float, 'doc': 'The timestamp of the first sample', 'default': None},
            {'name': 'rate', 'type': float, 'doc': 'Sampling rate in Hz', 'default': None},

            {'name': 'comments', 'type': str, 'doc': 'Human-readable comments about this TimeSeries dataset', 'default':None},
            {'name': 'description', 'type': str, 'doc': 'Description of this TimeSeries dataset', 'default':None},
            {'name': 'control', 'type': Iterable, 'doc': 'Numerical labels that apply to each element in data', 'default': None},
            {'name': 'control_description', 'type': Iterable, 'doc': 'Description of each control value', 'default': None},
            {'name': 'parent', 'type': 'NWBContainer', 'doc': 'The parent NWBContainer for this NWBContainer', 'default': None},
    )
    def __init__(self, **kwargs):
        name, source, data, unit, external_file, starting_frame, format = popargs('name', 'source', 'data', 'unit', 'external_file', 'starting_frame', 'format', kwargs)
        distance, field_of_view, orientation = popargs('distance', 'field_of_view', 'orientation', kwargs)
        super(OpticalSeries, self).__init__(name, source, data, unit, external_file, starting_frame, format, **kwargs)
        self.distance = distance
        self.field_of_view = field_of_view
        self.orientation = orientation

class RoiResponseSeries(TimeSeries):
    '''
    ROI responses over an imaging plane. Each row in data[] should correspond to the signal from one ROI.
    '''

    __nwbfields__ = ('roi_names',
                     'segmenttation_interface',
                     'segmenttation_interface_path')

    _ancestry = "TimeSeries,ImageSeries,ImageMaskSeries"
    _help = "ROI responses over an imaging plane. Each row in data[] should correspond to the signal from one no ROI."

    @docval({'name': 'name', 'type': str, 'doc': 'The name of this TimeSeries dataset'},
            {'name': 'source', 'type': str, 'doc': ('Name of TimeSeries or Modules that serve as the source for the data '
                                                   'contained here. It can also be the name of a device, for stimulus or '
                                                   'acquisition data')},
            {'name': 'data', 'type': (list, np.ndarray, TimeSeries), 'doc': 'The data this TimeSeries dataset stores. Can also store binary data e.g. image frames'},
            {'name': 'unit', 'type': str, 'doc': 'The base unit of measurement (should be SI unit)'},

            {'name': 'roi_names', 'type': Iterable, 'doc': 'List of ROIs represented, one name for each row of data[].'},
            {'name': 'segmenttation_interface', 'type': ImageSeries, 'doc': 'Link to ImageSeries that mask is applied to.'},
            {'name': 'segmenttation_interface_path', 'type': str, 'doc': 'Path to linked ImageSeries.'},

            {'name': 'resolution', 'type': float, 'doc': 'The smallest meaningful difference (in specified unit) between values in data', 'default': _default_resolution},
            {'name': 'conversion', 'type': float, 'doc': 'Scalar to multiply each element by to conver to volts', 'default': _default_conversion},

            {'name': 'timestamps', 'type': (list, np.ndarray, TimeSeries), 'doc': 'Timestamps for samples stored in data', 'default': None},
            {'name': 'starting_time', 'type': float, 'doc': 'The timestamp of the first sample', 'default': None},
            {'name': 'rate', 'type': float, 'doc': 'Sampling rate in Hz', 'default': None},

            {'name': 'comments', 'type': str, 'doc': 'Human-readable comments about this TimeSeries dataset', 'default':None},
            {'name': 'description', 'type': str, 'doc': 'Description of this TimeSeries dataset', 'default':None},
            {'name': 'control', 'type': Iterable, 'doc': 'Numerical labels that apply to each element in data', 'default': None},
            {'name': 'control_description', 'type': Iterable, 'doc': 'Description of each control value', 'default': None},
            {'name': 'parent', 'type': 'NWBContainer', 'doc': 'The parent NWBContainer for this NWBContainer', 'default': None},
    )
    def __init__(self, **kwargs):
        name, source, data, unit = popargs('name', 'source', 'data', 'unit', kwargs)
        roi_names, segmenttation_interface, segmenttation_interface_path = popargs('roi_names', 'segmenttation_interface', 'segmenttation_interface_path', kwargs)
        super(RoiResponseSeries, self).__init__(name, source, data, unit, **kwargs)
        self.roi_names = roi_names
        self.segmenttation_interface = segmenttation_interface
        self.segmenttation_interface_path = segmenttation_interface_path

