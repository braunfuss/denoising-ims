# Denoising Autoencoder for waveform data

This packages contains python scripts to train a neural network for the denoising of waveform data, as used in the publication "Denoising DPRK".
This package is based on the work by  
 * Heuel, J. & Friederich, W. Suppression of wind turbine noise from seismological data using nonlinear thresholding and denoising autoencoder Journal of Seismology, 2022 (https://github.com/JanisHe/seismic_denoiser)
 and also on:
 * Zhu, W.; Mousavi, S. M. & Beroza, G. C. Seismic signal denoising and decomposition using deep neural networks IEEE Transactions on Geoscience and Remote Sensing, IEEE, 2019, 57, 9476-9488
 * Tibi, R.; Hammond, P.; Brogan, R.; Young, C. J. & Koper, K. Deep Learning Denoising Applied to Regional Distance Seismic Data in Utah Bulletin of the Seismological Society of America, 2021


# Installation Requirements

 Before using the package, ensure that the following dependencies are installed:

 * Numpy
 * Matplotlib
 * Scipy
 * Tensorflow >= 2.0
 * Obspy
 * Joblib
 * Pandas
 * tqdm

#### Training of own model

Create your own training dataset, that contains earthquake data with an high SNR and noise data. Both datasets
are in two different directories, have the same length and sampling frequency. For the length and sampling frequency
60 s windows and 100 Hz are recommended.
For earthquake data, the STanford EArthquake Dataset (STEAD) is recommended starting point (https://github.com/smousavi05/STEAD).
Note, each waveform is saved as a `.npz` file. If available, the earthquake data contain onsets of P- and S-arrivals
in samples (`itp` and `its`). This only used for validation and in case of waveform records longer then configured sample length to cut the waveform accordingly. Save your data e.g. by the folllowing commands for earthquakes and noise, repectively:
```
np.savez(data=earthquake_data, file=filename, its=0, itp=0, starttime=str(trace.stats.starttime))
np.savez(data=noise_data, file=filename)
```

Afterwards, adjust the parfile and start your training.

```
python run_model_from_parfile.py
```

The training of the example dataset will take a while. It depends whether you run it on CPU or GPU.
The trained model is saved in the directory `./Models` and is named `model.h5`. The config file is saved
in `./config` und `model.config`.


#### Denoise data
Run the function `predict` from file `prediction_*.py` with your created model and
config file. The parameter data_list is a list with numpy arrays for denoising.
Using `prediction.py` only denoises time windows of the same length as for the training dataset,
but in many cases it is necessary to denoise longer time series (see next section).



#### Denoise seismograms
If your waveform record is longer than your waveform record from the training dataset, the longer time series is split into
overlapping segments, e.g. 60 s segments. Each of these segments is denoised and the overlapping segments are
merged to get one denoises time series.
The script `./denoiser/denoiser_utils.py` contains the function `denoising_stream` that removes the noise
from all traces in a obspy stream object. For more details please read the function description.
You can use the pretrained model and config-file to suppress noise from your data. Try to run the following code:
```
from obspy import read, UTCDateTime
from denoiser.denoise_utils import denoising_stream

st = read(your data)  # Read your waveform data here
st_de = st.copy()  # Create a copy of your obspy stream
st_de = denoising_stream(stream=st, model_filename="Models/gr_mixed_stft.h5",
                         config_filename="config/gr_mixed_stft.config")
```
st_de will then be a list of signal and noise, in this order, for each trace in the stream. Therefore e.g. std_de[0][0] is the predicted signal of the first data in stream.
Compare your original stream and the denoised stream whether some noise is removed from the data.
The pretrained model is trained with noise samples from several stations of the seismic network GR and
with high signal-to-ratio events from the Stanford Earthquake Dataset
(STEAD, https://github.com/smousavi05/STEAD).

#### Automatic denoiser
In many cases one needs real time denoising to analyse the denoised traces e.g. with Seiscomp.
The function `auto_denoiser` in `./denoiser.denoiser_utils.py` reads a list with all required parameters
from a csv file (`./denoiser/autp_denoiser.csv`).
