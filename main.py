from datetime import datetime
from ionoplot import MapType, plot_maps, plot_distance_time

EPICENTERS = {'01:17': {'lat': 37.220,
                        'lon': 37.019,
                        'time': datetime(2023, 2, 6, 1, 17, 34)},
              '10:24': {'lat': 38.016,
                        'lon': 37.206,
                        'time': datetime(2023, 2, 6, 10, 24, 50)}
             }

times = [datetime(2023, 2, 6, 10, 25),
                 datetime(2023, 2, 6, 10, 40),
                 datetime(2023, 2, 6, 10, 45)]

plot_maps(["notebook/roti_10_24.h5", "notebook/tnpgn_roti_10_24.h5"], MapType.ROTI, times, EPICENTERS['10:24'], save_path="./out/time3.png")
plot_distance_time("notebook/dtec_10_20_10_24.h5", MapType.TEC_10_20, EPICENTERS['10:24'], save_path="./out/time2.png")
