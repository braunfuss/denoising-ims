from denoiser.denoise_utils import denoising_stream
from obspy import read


st = read("../input/*") # read all data (mseed) in folder

st.merge(method=-1) # merge gaps and overlaps
st.filter("highpass", freq=0.01, corners=4) # higpass filter for raw data recommended

st_de = st.copy()  # Create a copy of the stream
st_de = denoising_stream(stream=st, model_filename="Models/IMS_P.h5",
                         config_filename="config/IMS_P.config")


# write out predicted noises
for tr in st_de[1]:
        tr.write("../output_noise/test_%s_%s_%s_%s_%s_IMS.mseed" % (tr.stats.station, tr.stats.location, tr.stats.channel, tr.stats.starttime, tr.stats.endtime))

# write out predicted signals
for tr in st_de[0]:
        tr.write("../output_signal/%s_%s_%s_%s__%s.mseed" % (tr.stats.station, tr.stats.location, tr.stats.channel, tr.stats.starttime, tr.stats.endtime))
