# Denoising Autoencoder for waveform data

This packages contains python scripts to train a neural network for the denoising of waveform data, as used in the publication "Deep neural network based denoising of regional seismic waveforms and impact on analysis of North Korean nuclear tests".
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


#### Denoise seismograms

The example script "example_denoise.py" denoises all waveforms in an folder "input" using a IMS network trained P-phase denoiser from REB catalog data for events around North Korea. 
If you want to use other trained models you have to change the model filename (*h5) and the config filename (*config).

Models delivered here are:

IMS_P = General IMS data trained P-phase denoiser model; trained with 60s duration time windows at 20 Hz
IMS_LP = General IMS data trained long period model for surface and S-waves; trained with 360s duration time windows at 20Hz
hydro_IMS = Hydroacustic P-phase denoiser, trained with 60s windows at 100 Hz


Furthermore station specific trained models, each trained with 60s windows at 20 Hz sampling rate are available:
```
IMS_model_bjt = BJT station specific P-phase denoiser
IMS_model_jnu = JNU station specific P-phase denoiser
IMS_model_jow = JOW station specific P-phase denoiser
IMS_model_KLR = KLR station specific P-phase denoiser
IMS_model_mja = MJA station specific P-phase denoiser
IMS_model_usa = USA0B station specific P-phase denoiser
IMS_model_ks31 = KS31 station specific P-phase denoiser
```


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
st_de = denoising_stream(stream=st, model_filename="Models/IMS_P.h5",
                         config_filename="config/IMS_P.config")
```
st_de will then be a list of signal and noise, in this order, for each trace in the stream. Therefore e.g. std_de[0][0] is the predicted signal of the first data in stream.
Compare your original stream and the denoised stream whether some noise is removed from the data.

"denoise_hydro.py" is set to denoise IMS hydroacustic data. 


#### Training of own model

Create your own training dataset, that contains earthquake data with an high SNR and noise data. Both datasets
are in two different directories, have the same length and sampling frequency. For the length and sampling frequency of a P-wave denoiser
60 s windows and 20 or 100 Hz are recommended.
For earthquake data, the STanford EArthquake Dataset (STEAD) is a recommended starting point (https://github.com/smousavi05/STEAD), however in this publication the IMS network and REB catalog was used.
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




