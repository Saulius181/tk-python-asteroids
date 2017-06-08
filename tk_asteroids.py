#!/usr/bin/env python

__author__ = "Saulius Bartkus"
__copyright__ = "Copyright 2017"

__license__ = "GPL"
__version__ = "2.0.1"
__maintainer__ = "Saulius Bartkus"
__email__ = "saulius181@yahoo.com"
__status__ = "Production"

from tkinter import *
import random
import math
import time
#import winsound
from threading import *
from tkinter.font import Font

_bangSmall = "sounds/bangSmall.wav"
_bangMedium = "sounds/bangMedium.wav"
_bangLarge = "sounds/bangLarge.wav"
_fire = "sounds/fire.wav"
_rotationValues = { "Left": 1, "Right": -1 }
_asteroidTypes = {
	"big": [0, 14, 6, 31, 1, 60, 16, 64, 26, 78, 63, 73, 77, 46, 72, 24, 77, 8, 55, 0, 35, 5, 23, 0],
	"medium": [12, 0, 0, 4, 7, 14, 0, 19, 0, 32, 10, 38, 31, 35, 37, 30, 32, 25, 38, 18, 35, 2],
	"small": [1, 1, 4, 8, 1, 12, 9, 18, 17, 13, 17, 4, 10, 0]
 }
_frameRate = 20
_acc_rate = 0.1
_max_max = 4
_shipCoordinates = [200, 189, 193, 211, 197, 207, 203, 207, 207, 211]

_carrierCoordinates = [163.688,129.903,163.688,126.19,161.54399999999998,120.997,158.13699999999997,117.886,155.41099999999997,101.227,149.44499999999996,89.37400000000001,143.34599999999998,101.69500000000001,142.85599999999997,103.933,137.02699999999996,98.611,133.76899999999995,75.37400000000001,127.80399999999995,63.55200000000001,121.70399999999995,75.82600000000001,120.24499999999995,83.287,107.93,72.041,102.572,46.82299999999999,94.292,14.989999999999995,86.688,0,78.87,14.982,70.604,46.828,65.294,72.18,54.723,81.83300000000001,53.393,75.37500000000001,47.428,63.55300000000001,41.32899999999999,75.82700000000001,38.31499999999999,96.81400000000001,31.19499999999999,103.31500000000001,30.72299999999999,101.22600000000001,24.756999999999987,89.37300000000002,18.657999999999987,101.69400000000002,16.139999999999986,117.06100000000002,11.832999999999986,120.99300000000002,9.686999999999987,126.18800000000002,9.686999999999987,129.901,13.585999999999988,134.28500000000003,12.497999999999987,135.598,11.508999999999986,139.292,11.944999999999986,141.959,15.572999999999986,145.024,33.94,145.024,37.567,141.941,38.003,139.243,36.991,135.569,35.229,133.446,67.688,132.10999999999999,67.688,146.21699999999998,57.977000000000004,155.41,56.635000000000005,159.297,58.294000000000004,170.509,61.511,173.30599999999998,62.777,172.99599999999998,87.176,163.02399999999997,87.32600000000001,163.02399999999997,111.72800000000001,173.003,112.99900000000001,173.37599999999998,113.00000000000001,173.37599999999998,116.21100000000001,170.55899999999997,117.87000000000002,159.34699999999998,116.53300000000002,155.42299999999997,105.68600000000002,145.15099999999998,105.68600000000002,132.111,138.94100000000003,133.482,137.18500000000003,135.6,136.19600000000003,139.29399999999998,136.63200000000003,141.96099999999998,140.26000000000005,145.02599999999998,158.62700000000004,145.02599999999998,162.25400000000005,141.94299999999998,162.69000000000005,139.24499999999998,161.67800000000005,135.57099999999997,160.51400000000007,134.16899999999998,163.688,129.903]

_spaceCraftCoordinates = [18.1685, 8.7498, 15.959000000000001, 0.0008000000000009778, 13.970600000000003, 8.7498, 12.777600000000001, 8.7498, 12.777600000000001, 15.112700000000002, 11.938200000000002, 17.2779, 10.789200000000001, 13.300799999999999, 10.0379, 19.266199999999998, 4.514900000000001, 25.4085, 6.149600000000001, 27.1758, 13.351800000000004, 21.4757, 13.660900000000005, 26.2479, 8.888800000000003, 31.108600000000003, 10.744600000000004, 32.125, 14.235200000000004, 30.313200000000002, 15.958500000000004, 32.125, 17.792000000000005, 30.313200000000002, 21.392900000000004, 32.125, 23.248200000000004, 31.108600000000003, 18.476100000000002, 26.247900000000005, 18.783600000000003, 21.475700000000003, 25.982200000000002, 27.175800000000006, 27.6102, 25.408500000000004, 22.072699999999998, 19.266200000000005, 21.293899999999997, 13.300800000000004, 20.09, 17.277900000000006, 19.140399999999996, 15.112700000000007, 19.140399999999996, 8.7498, 18.1685, 8.7498]

_sputnikCoordinates = [25.5334, 25.064300000000003, 18.97615, 3.8497500000000002, 17.713900000000002, 2.5594, 17.115050000000004, 2.35955, 12.775100000000002, 0.00010000000000012222, 8.435150000000002, 2.35955, 7.836450000000003, 2.5593500000000002, 6.574050000000003, 3.8498000000000006, 0.016800000000000006, 25.064300000000003, 0.26435000000000003, 25.5333, 0.3752000000000001, 25.5501, 0.7333500000000002, 25.285750000000004, 6.8335, 5.550050000000001, 7.61375, 5.550050000000001, 12.40005, 10.336400000000001, 12.40005, 25.175050000000002, 12.77505, 25.550050000000002, 13.15005, 25.175050000000002, 13.15005, 10.336400000000001, 17.93635, 5.550050000000001, 18.7166, 5.550050000000001, 24.81675, 25.285800000000002, 25.1749, 25.550150000000002, 25.28575, 25.53335, 25.5334, 25.064300000000003]

_sateliteCoordinates = [21.93411982579839, 36.652137755454376, 22.153817902713055, 37.18239713066616, 22.68414798860296, 37.40202449690271, 23.434176151407527, 36.65199633409813, 23.434176151407534, 36.27949248176906, 28.984115855584513, 36.27949248176907, 29.514445941474428, 36.05986511553252, 29.734073307710965, 35.5295350296426, 25.857360379855717, 29.237062494541636, 25.857360379855713, 27.553299827180236, 28.52598137205375, 27.55329982718024, 29.2759388241802, 26.80334237505378, 29.27593882418021, 19.97947909389112, 31.970722767282137, 19.97947909389111, 31.970722767282133, 23.329468180440507, 32.19035013351867, 23.859798266330415, 32.72068021940859, 24.079425632566956, 46.52100042511392, 24.079425632566952, 47.05133051100389, 23.859798266330426, 47.27095787724041, 23.329468180440497, 47.271170009274776, 15.129504392410709, 47.05154264303823, 14.5991743065208, 46.52121255714832, 14.37954694028427, 32.72089235144294, 14.379546940284255, 32.190562265553034, 14.599174306520787, 31.97093489931649, 15.129504392410706, 31.970934899316482, 18.479493478960094, 29.276150956214554, 18.47949347896009, 29.276150956214558, 13.33260464005945, 25.85721895849948, 9.232587390705499, 25.85714824782136, 6.829484994843005, 25.10719079569491, 6.079527542716566, 20.261105181511013, 6.0795275427165585, 19.730775095621098, 6.299154908953103, 19.51114772938456, 6.829484994843014, 19.51121844006269, 9.231738862568072, 17.313318432100544, 10.384676469292728, 16.092286442347614, 13.332604640059463, 16.09228644234761, 18.479493478960094, 13.397502499245682, 18.47949347896011, 13.397502499245677, 15.129504392410714, 12.647545047119227, 14.379546940284262, -1.1529165799424064, 14.37954694028426, -1.9028740320688406, 15.129504392410709, -1.9028740320688442, 23.32953889111863, -1.6832466658322893, 23.859868977008542, -1.1529165799423922, 24.0794963432451, 12.647403625762987, 24.07949634324508, 13.39736107788944, 23.329538891118624, 13.397361077889444, 19.979549804569242, 16.09214502099138, 19.97954980456923, 16.09214502099139, 26.8034130857319, 16.311772387227926, 27.33374317162181, 16.84210247311783, 27.553370537858353, 19.511289150740808, 27.553370537858353, 19.511289150740815, 29.23685036250728, 15.634010537460615, 35.52960574032072, 15.853637903697155, 36.05993582621063, 16.383967989587063, 36.279563192447185, 21.933907693764045, 36.27956319244717, 21.93411982579839, 36.652137755454376]

_spaceStationCoordinates = [198.647, 82.0705, 200.647, 80.0705, 200.647, 44.6075, 198.647, 42.6075, 182.0375, 42.6075, 180.0375, 44.6075, 180.0375, 80.07050000000001, 182.0375, 82.07050000000001, 188.3425, 82.07050000000001, 188.3425, 86.57000000000001, 170.24, 86.57000000000001, 159.747, 83.02300000000001, 142.55900000000003, 98.376, 140.84850000000003, 98.376, 140.84850000000003, 93.48100000000001, 138.84850000000003, 91.48100000000001, 124.35200000000003, 91.48100000000001, 121.26550000000003, 85.91850000000001, 119.51650000000004, 84.88900000000001, 99.76000000000003, 84.88900000000001, 99.76000000000003, 81.62700000000001, 107.85800000000003, 81.62700000000001, 109.85800000000003, 79.62700000000001, 109.85800000000003, 36.6405, 107.85800000000003, 34.6405, 87.72500000000004, 34.6405, 85.72500000000004, 36.6405, 85.72500000000004, 79.6265, 87.72500000000004, 81.6265, 95.75950000000003, 81.6265, 95.75950000000003, 84.8885, 76.52550000000002, 84.8885, 74.52550000000002, 86.8885, 74.52550000000002, 98.37549999999999, 72.26550000000002, 98.37549999999999, 57.04550000000002, 85.023, 44.38250000000002, 91.68849999999999, 31.71950000000002, 85.023, 22.3265, 85.023, 22.3265, 82.0705, 25.4885, 82.0705, 27.4885, 80.0705, 27.4885, 44.6075, 25.4885, 42.6075, 8.879, 42.6075, 6.879, 44.6075, 6.879, 80.07050000000001, 8.879, 82.07050000000001, 12.0415, 82.07050000000001, 12.0415, 85.02300000000001, 2.0, 85.02300000000001, 0.0, 87.02300000000001, 0.0, 113.73250000000002, 2.0, 115.73250000000002, 12.0415, 115.73250000000002, 12.0415, 118.68500000000002, 8.879, 118.68500000000002, 6.879, 120.68500000000002, 6.879, 156.1485, 8.879, 158.1485, 25.488500000000002, 158.1485, 27.488500000000002, 156.1485, 27.488500000000002, 120.685, 25.488500000000002, 118.685, 22.326, 118.685, 22.326, 115.7325, 31.7205, 115.7325, 44.3835, 109.06700000000001, 57.046499999999995, 115.7325, 72.267, 102.3755, 74.526, 102.3755, 74.526, 113.75800000000001, 76.526, 115.75800000000001, 95.75999999999999, 115.75800000000001, 95.75999999999999, 119.02000000000001, 87.7255, 119.02000000000001, 85.7255, 121.02000000000001, 85.7255, 164.006, 87.7255, 166.006, 107.85849999999999, 166.006, 109.85849999999999, 164.006, 109.85849999999999, 121.02, 107.85849999999999, 119.02, 99.7605, 119.02, 99.7605, 115.758, 119.517, 115.758, 121.26599999999999, 114.7285, 124.35249999999999, 109.166, 138.849, 109.166, 140.849, 107.166, 140.849, 102.3755, 142.5725, 102.3755, 159.7475, 117.624, 170.2365, 114.0805, 188.3435, 114.0805, 188.3435, 118.685, 182.0385, 118.685, 180.0385, 120.685, 180.0385, 156.1485, 182.0385, 158.1485, 198.648, 158.1485, 200.648, 156.1485, 200.648, 120.685, 198.648, 118.685, 192.3435, 118.685, 192.3435, 114.0805, 198.561, 114.0805, 200.561, 112.0805, 200.561, 88.57, 198.561, 86.57, 192.3435, 86.57, 192.3435, 82.0705, 198.647, 82.0705]

_dreadnoughtCoordinates = [93.6228, 24.8686, 93.6228, 63.741600000000005, 84.84559999999999, 62.57140000000001, 84.84559999999999, 33.6458, 76.06839999999998, 33.6458, 76.06839999999998, 61.401199999999996, 62.902599999999985, 59.6458, 62.902599999999985, 18.485200000000003, 51.2, 1.4628, 39.4972, 18.4852, 39.4972, 59.64600000000001, 26.3314, 61.4014, 26.3314, 33.6458, 17.5542, 33.6458, 17.5542, 62.5714, 8.777, 63.7416, 8.777, 24.8686, 0.0, 24.8686, 0.0, 92.16000000000001, 8.7772, 92.16000000000001, 8.7772, 83.3828, 33.6458, 83.3828, 33.6458, 92.16000000000001, 41.5812, 92.16000000000001, 51.2, 100.9372, 60.8188, 92.16, 68.75420000000001, 92.16, 68.75420000000001, 83.38279999999999, 93.62280000000001, 83.38279999999999, 93.62280000000001, 92.16000000000001, 102.4, 92.16000000000001, 102.4, 24.8686, 93.6228, 24.8686]

_battleshipCoordinates = [14.397590187582834, -10.551559513471368, 12.962163421774134, -9.4869395437169, 8.648104949755012, 11.265654534614605, 6.218061785529324, 13.593874322349436, -2.0033273379704344, 24.376121364594383, -1.7197775187146238, 28.159566908011133, 0.42714009032397193, 29.94557721593211, 0.4271400903239666, 32.727618135832465, 1.9271964159331159, 34.22767446144161, 2.987856587712935, 33.788136886256055, 3.427394162898496, 32.72747671447623, 3.4273941628984943, 31.038622878290276, 5.330218511071491, 31.43163282727376, 5.330218511071488, 34.76974251989921, 6.830274836680632, 36.26951600279588, 7.890793587104216, 35.83011984896656, 8.330189740933534, 34.7693182558305, 8.330189740933534, 31.788721751772965, 9.53849380862511, 31.861978014303894, 9.723331521227273, 32.99207607199624, 11.200053323057256, 34.22753304008536, 17.594985630752156, 34.22767446144161, 18.655928645244455, 33.787854043543575, 19.07142458986966, 32.99193465063999, 19.25696940925302, 31.85745253090431, 20.46484921287588, 31.780095049042494, 20.464707791519633, 34.769601098542985, 21.964481274416315, 36.269657424152115, 23.025282867552363, 35.8302612703228, 23.464679021381684, 34.76974251989921, 23.464679021381688, 31.41777353436251, 25.367503369554694, 31.025894956228914, 25.367503369554683, 32.72747671447622, 26.86755969516383, 34.22753304008537, 27.92821986694365, 33.78799546489981, 28.36775744212921, 32.72733529311999, 28.36775744212921, 29.948122800344386, 29.96086902014251, 28.829904136575976, 30.798366291779857, 24.375979943238168, 20.14665116134193, 11.264947427833425, 15.832734110679048, -9.4869395437169, 14.397590187582834, -10.551559513471368]

_fighterCoordinates = [31.12795283374629, 2.4842840808379485, 30.059090223304715, 2.9190133299114436, 30.05456473990511, 2.9235388133110334, 29.615168586075786, 3.984057563734627, 29.615310007432026, 14.962456027080716, 27.088817478252498, 16.6749272297583, 26.43035964361158, 17.916606737521878, 26.43021822225534, 22.728468383496335, 24.405912929074496, 22.72846838349633, 23.510432901379854, 20.87584861678758, 21.292097507441422, 19.956892643957538, 19.073903534859216, 20.87570719543134, 18.178282085808345, 22.72846838349633, 16.15397679262749, 22.728468383496327, 16.15397679262749, 17.916748158878114, 15.49537753663034, 16.674927229758296, 12.969026428807043, 14.962597448436956, 12.969026428807048, 3.9843404064470818, 11.453130911299318, 2.484284080837952, 8.672504204961342, 3.6363024487470703, 7.877009076126466, 4.781956855625516, 1.4164572591374593, 18.920274102738066, 1.2806927571496338, 19.543659441032126, 1.280551335793401, 28.891469666962053, 1.5025828650859765, 29.676923879504063, 7.2399058662773825, 39.01426892507243, 8.517930662593951, 39.72887103813956, 11.468970103197899, 39.729012459495785, 12.529630274977709, 39.289757727022696, 12.969026428807041, 38.229238976599135, 12.969026428807043, 32.87389505860469, 18.380656046583923, 32.87389505860468, 21.292238928797644, 34.84926856252743, 23.510432901379843, 33.93045401105361, 24.20608455271117, 32.873895058604695, 29.61545142878826, 32.87389505860469, 29.61531000743202, 38.22909755524288, 31.115366333041163, 39.72915388085204, 34.06626435228886, 39.729153880852024, 35.126783102712444, 39.28975772702271, 35.344147727249194, 39.01441034642866, 41.08147072844061, 29.67678245814784, 41.30350225773317, 28.891611088318285, 41.303502257733186, 19.543659441032126, 41.167737755745364, 18.919991260025597, 34.70718593875634, 4.781956855625523, 31.12795283374629, 2.4842840808379485]

_destroyerCoordinates = [100.692, 166.3875, 103.5606, 163.5189, 116.00519999999999, 163.5189, 118.33469999999998, 162.32519999999997, 118.72799999999998, 159.74069999999998, 101.45219999999998, 108.05159999999997, 98.49479999999997, 29.123699999999968, 98.41409999999998, 28.541399999999967, 91.87619999999997, 2.180399999999966, 89.0937, 0.0, 89.0739, 0.0, 86.29979999999999, 2.2176, 79.74749999999999, 30.314099999999996, 79.6758, 30.850499999999997, 76.629, 105.8856, 76.2243, 107.7243, 59.129400000000004, 159.7578, 59.534099999999995, 162.3339, 61.8579, 163.5216, 74.2938, 163.5216, 75.0915, 165.5067, 77.16, 166.3875, 80.25839999999998, 166.3875, 79.75049999999999, 166.76879999999997, 75.64259999999999, 175.86569999999998, 75.76589999999999, 177.21989999999997, 76.96499999999999, 177.86249999999998, 76.96499999999999, 177.86249999999998, 84.9861, 177.86249999999998, 84.9861, 177.86249999999998, 86.17649999999999, 177.3489, 86.3142, 176.13, 85.7778, 174.8478, 86.3544, 174.9939, 86.3544, 174.9939, 86.3544, 174.9939, 92.6139, 174.9939, 93.4257, 174.61260000000001, 92.8605, 175.8633, 92.9838, 177.2175, 94.17990000000002, 177.8628, 94.17990000000002, 177.8628, 94.17990000000002, 177.8628, 102.19830000000002, 177.8628, 102.19830000000002, 177.8628, 102.19830000000002, 177.8628, 103.38900000000001, 177.35219999999998, 103.52670000000002, 176.133, 99.61650000000002, 166.7895, 99.07410000000002, 166.3878, 100.63770000000001, 166.3878, 100.692, 166.3875]

_cruiserCoordinates = [7.538200000000001, 82.84020000000001, 8.9536, 75.62460000000002, 30.826800000000006, 73.42880000000001, 26.168000000000003, 83.97260000000001, 26.074200000000005, 84.22500000000002, 26.617400000000004, 88.43820000000001, 29.679400000000005, 89.8418, 32.466, 89.2758, 39.257400000000004, 87.61220000000002, 39.257400000000004, 92.12540000000001, 41.16980000000001, 94.0378, 52.64480000000001, 94.0378, 54.557200000000016, 92.12540000000001, 54.557200000000016, 86.2808, 58.189000000000014, 86.25220000000002, 60.29460000000002, 86.298, 60.29460000000002, 92.12540000000001, 62.20700000000002, 94.0378, 73.68200000000002, 94.0378, 75.59440000000002, 92.12540000000001, 75.59440000000002, 87.70580000000001, 81.56520000000002, 89.2702, 84.33620000000002, 89.8382, 87.34860000000003, 88.4264, 87.74060000000003, 84.1522, 87.66980000000002, 83.9686, 82.97080000000003, 73.333, 105.47320000000002, 75.5842, 106.88080000000002, 82.77139999999999, 108.79160000000002, 83.62059999999998, 109.62740000000002, 83.47879999999998, 111.34080000000002, 82.55539999999998, 114.40660000000001, 56.948799999999984, 114.397, 56.00779999999999, 108.08760000000001, 36.24199999999998, 104.99700000000001, 37.63619999999999, 102.9086, 46.50819999999999, 69.8472, 42.139999999999986, 68.0284, 37.47359999999999, 58.65520000000001, 20.82899999999999, 57.037400000000005, 20.39099999999999, 55.81720000000001, 20.545999999999992, 55.4654, 20.674199999999992, 45.8112, 37.47159999999999, 43.9598, 42.22039999999999, 11.522, 46.5084, 9.466, 37.952, 6.3428, 36.544399999999996, 0.03159999999999954, 56.15899999999999, 0.022000000000000006, 57.098000000000006, 3.0858000000000003, 82.628, 4.8128, 83.55720000000001, 7.538200000000001, 82.84020000000001]

_flameCoordinates = [ 198, 207, 200, 212, 202, 207, 198, 207 ]

_rocketCoordinates = [8.6196, 8.0908, 8.6196, 6.5120000000000005, 6.506399999999999, 0.1264000000000003, 6.2364, 0.0, 5.9648, 0.12400000000000003, 3.8111999999999995, 6.5120000000000005, 3.8111999999999995, 8.0912, 3.5196, 8.287600000000001, 2.6204, 9.9792, 2.6204, 11.8636, 2.7804, 12.1316, 3.0915999999999997, 12.116, 4.0388, 11.4852, 4.9364, 11.213600000000001, 5.6328, 11.213600000000001, 5.6328, 12.126800000000003, 5.9364, 12.430800000000003, 6.494, 12.430800000000003, 6.7976, 12.126800000000003, 6.7976, 11.213600000000001, 7.493600000000001, 11.213600000000001, 8.392000000000001, 11.485600000000002, 9.3384, 12.116000000000001, 9.6496, 12.131600000000002, 9.8096, 11.863600000000002, 9.8096, 9.9792, 8.9104, 8.287600000000001, 8.6196, 8.0908]

class Board():
	score = 0
	
	objectList = {}
	
	gameState = None
	
	def __init__( self, coordinates, outline, fill, tag, state ):	
		self.coordinates = coordinates
		self.outline = outline
		self.fill = fill
		self.tag = tag
		self.state = state

	def move(self):
		Board.canvas.move(self.reference, self.dx, self.dy )	
		
	def hide(self):
		Board.canvas.itemconfig(self.reference, state=HIDDEN)

	def show(self):
		Board.canvas.itemconfig(self.reference, state=NORMAL)

	def set_outline(self, color):
		Board.canvas.itemconfig(self.reference, outline=color)

	def set_fill(self, color):
		Board.canvas.itemconfig(self.reference, fill=color)
		
	def get_color_by_timer(self, timer):
		if timer <= 16:
			color = "#" + '0{0:x}'.format(int(timer))*3
		else:
			color = "#" + '{0:x}'.format(int(timer))*3
		return color

	def get_target_angle(self, target):
		if target:
			x1, y1  = self.get_center()
			x2, y2  = target.get_center()
			
			x = x2 - x1
			y = y2 - y1
			
			return math.atan2(-y, x)
		
	def destroy(self):
		Board.canvas.delete(self.reference)	

	def get_asteroid_list():
		list = []
		for id, object in Board.objectList.copy().items():
			if Board.canvas.gettags(id) and Board.canvas.gettags(id)[0] == 'asteroid':
				list.append(object)
		return list
		
	def generate_asteroids(num=2, offsetX=0, offsetY=0, size="big"):
		for i in range(num):
			Asteroid(
				coordinates=Board.set_asteroid_coords(size, offsetX, offsetY), 
				direction=random.uniform(0, 2 * math.pi), 
				size=size
				)
	
	def min_x(self):
		return min(Board.canvas.coords(self.reference)[0::2]) 
	def min_y(self):
		return min(Board.canvas.coords(self.reference)[1::2]) 
	def max_x(self):
		return max(Board.canvas.coords(self.reference)[0::2]) 
	def max_y(self):
		return max(Board.canvas.coords(self.reference)[1::2]) 
		
	def set_asteroid_coords( type, offsetX=0, offsetY=0):
		coords = []
		
		for coord1, coord2 in zip(_asteroidTypes[type][0::2], _asteroidTypes[type][1::2]):
			coords.extend([coord1 + random.uniform(0, 10) + offsetX, coord2 + random.uniform(0, 10) + offsetY])
		
		if not offsetX and not offsetY:
			loop = True
			
			while ( loop ):
				loop = False
				
				offsetX = random.uniform(0, _boardWidth)
				offsetY = random.uniform(0, _boardHeight)
				
				for item in Board.canvas.find_overlapping( 
							offsetX -min(coords[0::2]) -100, 
							offsetY -min(coords[1::2]) -100, 
							offsetX +max(coords[0::2]) +100, 
							offsetY +max(coords[1::2]) +100
					):
						if Board.canvas.gettags(item) and Board.canvas.gettags(item)[0] == 'ship':
							loop = True
							break
				if loop:
					continue
				
				coords[0::2] = [x + offsetX for x in coords[0::2]]
				coords[1::2] = [y + offsetY for y in coords[1::2]]
			
		return coords
	
	def get_overlapping(self):
		return Board.canvas.find_overlapping( 
			Board.canvas.coords(self.reference)[0], 
			Board.canvas.coords(self.reference)[1], 
			Board.canvas.coords(self.reference)[2], 
			Board.canvas.coords(self.reference)[3] 
		)
	def get_center(self):
		x_center = 0
		y_center = 0
		
		for coord1, coord2 in zip( Board.canvas.coords(self.reference)[0::2], Board.canvas.coords(self.reference)[1::2] ):
			x_center += coord1
			y_center += coord2
		
		x_center /= (len(Board.canvas.coords(self.reference)) / 2 )
		y_center /= (len(Board.canvas.coords(self.reference)) / 2 )

		return x_center, y_center

	def offset_coordinates(self, coordinates, offset):
		new_coords = []		
		for coord1, coord2 in zip(coordinates[0::2], coordinates[1::2]):
			new_coords.extend([coord1+ offset[0], coord2 + offset[1] ])
		return new_coords

	def rot_coordinate(self, x, y, x_center, y_center, turn):
		x -= x_center
		y -= y_center
		_x = x * math.cos(turn) + y * math.sin(turn)
		_y = -x * math.sin(turn) + y * math.cos(turn)
		return _x + x_center, _y + y_center		
		
	def rotate_coordinates(self, x_center, y_center, turn):
		new_coords = []		
		
		for coord1, coord2 in zip(Board.canvas.coords(self.reference )[0::2], Board.canvas.coords(self.reference)[1::2]):
			new_coords.extend(self.rot_coordinate(coord1, coord2, x_center, y_center, turn))
			
		return new_coords
	
	def is_outbound(self):
		return Board.canvas.coords(self.reference)[0] < 0 or Board.canvas.coords(self.reference)[2] > _boardWidth or Board.canvas.coords(self.reference)[1] < 0 or Board.canvas.coords(self.reference)[3] > _boardHeight
	
	def outbound_reset(self):
		x_center, y_center = self.get_center()
		
		new_coords = []
		
		_x = 0
		_y = 0
		
		if (x_center < 0): _x = _boardWidth
		elif (x_center > _boardWidth): _x  = -_boardWidth
		
		if (y_center < 0): _y = _boardHeight
		elif (y_center > _boardHeight): _y = -_boardHeight

		for coord1, coord2 in zip(Board.canvas.coords(self.reference)[0::2], Board.canvas.coords(self.reference)[1::2]):
			new_coords.extend([coord1+_x, coord2+_y])
		Board.canvas.coords(self.reference, new_coords)
	
	def get_scaled_coordinates_by_center(self, scale):
		x_center, y_center = self.get_center()	
		return [ x_center - scale, y_center - scale, x_center + scale, y_center + scale	]
	
	def get_scaled_coordinates_by_reference(self, scale):
		return [
			Board.canvas.coords(self.reference)[0] - scale,
			Board.canvas.coords(self.reference)[1] - scale,
			Board.canvas.coords(self.reference)[2] + scale,
			Board.canvas.coords(self.reference)[3] + scale,
		]
	
	def expand(self, scale=1):
		Board.canvas.coords(self.reference, 
			self.get_scaled_coordinates_by_reference(scale)
		)	
	
	def update(self, rate=10):
		if self.timer <= 0:
			self.hide()
		else:			
			self.set_outline(self.get_color_by_timer(self.timer))
			self.timer -= random.uniform(0,rate)
	
class Nuke(Board):
	def __init__(
		self,
		coordinates, 
		direction,
		outline="white", 
		fill="", 
		tag="nuke",
		state=NORMAL
		):
		
		super().__init__(coordinates, outline, fill, tag, state)
		self.dx = math.cos(direction) * 10
		self.dy = math.sin(direction) * 10
		
		self.reference = Board.canvas.create_oval( self.coordinates, outline=self.outline, fill=self.fill, tag=self.tag, state=self.state )
		
		Board.objectList[self.reference] = self
		
	def destroy(self):
		super().destroy()
		del self.objectList[self.reference]
	
class Bullet(Board):
	def __init__(
		self,
		coordinates, 
		direction,
		outline="white", 
		fill="", 
		tag="bullet",
		state=NORMAL
		):
		
		super().__init__(coordinates, outline, fill, tag, state)
		self.dx = math.cos(direction) * 10
		self.dy = math.sin(direction) * 10
		
		self.reference = Board.canvas.create_oval( self.coordinates, outline=self.outline, fill=self.fill, tag=self.tag, state=self.state )
		
		Board.objectList[self.reference] = self
		
	def destroy(self):
		super().destroy()
		del self.objectList[self.reference]
		
class ClusterBomb(Board):
	def __init__(
		self,
		coordinates, 
		direction,
		outline="white", 
		fill="", 
		tag="clusterbomb",
		state=NORMAL
		):
		
		super().__init__(coordinates, outline, fill, tag, state)
		self.dx = math.cos(direction) * 10
		self.dy = math.sin(direction) * 10
		
		self.reference = Board.canvas.create_oval( self.coordinates, outline=self.outline, fill=self.fill, tag=self.tag, state=self.state )
		
		Board.objectList[self.reference] = self
		
	def destroy(self):
		super().destroy()
		del self.objectList[self.reference]		

class GravityBomb(Board):
	def __init__(
		self,
		coordinates, 
		outline="white", 
		fill="", 
		tag="gravity",
		state=NORMAL
		):
		
		super().__init__(coordinates, outline, fill, tag, state)
		self.timer = 1000
		self.reference = Board.canvas.create_oval( self.coordinates, outline=self.outline, fill=self.fill, tag=self.tag, state=self.state, width=10)
		
		Board.objectList[self.reference] = self
		
	def destroy(self):
		super().destroy()
		del self.objectList[self.reference]			
		
class Plague(Board):
	def __init__(
		self,
		coordinates, 
		direction,
		outline="white", 
		fill="", 
		tag="plague",
		state=NORMAL
		):
		
		super().__init__(coordinates, outline, fill, tag, state)
		self.dx = math.cos(direction) * 10
		self.dy = math.sin(direction) * 10
		
		self.reference = Board.canvas.create_oval( self.coordinates, outline=self.outline, fill=self.fill, tag=self.tag, state=self.state )
		
		Board.objectList[self.reference] = self
		
	def destroy(self):
		super().destroy()
		del self.objectList[self.reference]				

class ChargedBullet(Board):
	def __init__(
		self,
		coordinates, 
		direction,
		charge,
		outline="white", 
		fill="", 
		tag="chargedbullet",
		state=NORMAL,
		width=1
		):
		
		super().__init__(coordinates, outline, fill, tag, state)
		self.dx = math.cos(direction) * 15
		self.dy = math.sin(direction) * 15
		self.charge = charge
		self.reference = Board.canvas.create_oval( self.coordinates, outline=self.outline, fill=self.fill, tag=self.tag, state=self.state, width=width )
		
		Board.objectList[self.reference] = self
		
	def destroy(self):
		super().destroy()
		del self.objectList[self.reference]
		
class Asteroid(Board):
	def __init__(
		self,
		coordinates, 
		direction,
		outline="white", 
		fill="", 
		size="big",
		tag="asteroid",
		state=NORMAL
		):
		
		super().__init__(coordinates, outline, fill, tag, state)
		self.size = size
		
		if size == "big": _speed = 1
		elif size == "medium": _speed = 2
		elif size == "small": _speed = 3
		
		self.dx = math.cos(direction) * _speed
		self.dy = math.sin(direction) * _speed
		
		self.reference = Board.canvas.create_polygon( self.coordinates, outline=self.outline, fill=self.fill, tag=self.tag, state=self.state )
		Board.objectList[self.reference] = self
		
	def destroy(self, type="bullet"):	
		Debris.create( Board.canvas.coords(self.reference) )	
		
		if self.size == "big":
			Board.score+=100
#			winsound.PlaySound(_bangLarge, winsound.SND_ALIAS|winsound.SND_ASYNC|winsound.SND_NOWAIT)
			if type == "bullet":
				Board.generate_asteroids(2, Board.canvas.coords(self.reference)[0], Board.canvas.coords(self.reference)[1], "medium")

		elif self.size == "medium":
			Board.score+=200
#			winsound.PlaySound(_bangMedium, winsound.SND_ALIAS|winsound.SND_ASYNC|winsound.SND_NOWAIT)
			if type == "bullet":
				Board.generate_asteroids(2, Board.canvas.coords(self.reference)[0], Board.canvas.coords(self.reference)[1], "small")
		elif self.size == "small":
			Board.score+=300
#			winsound.PlaySound(_bangSmall, winsound.SND_ALIAS|winsound.SND_ASYNC|winsound.SND_NOWAIT)
		
		del self.objectList[self.reference]
		super().destroy()

class Vehicle(Board):
	def __init__(
		self,
		coordinates=_shipCoordinates, 
		outline="white", 
		fill="", 
		tag="ship",
		state=NORMAL,
		shieldRange=20
		):
		
		super().__init__(coordinates, outline, fill, tag, state)
		self.reference = Board.canvas.create_polygon( self.coordinates, outline=self.outline, fill=self.fill, tag=self.tag, state=self.state )
		
		self.acc = False
		self.rot = False
		self.rotationDir = None
		
		x_center, y_center = self.get_center()
		
		self.flame = Flame()	
		self.shield = Shield(coordinates=[ x_center - shieldRange, y_center - shieldRange, x_center + shieldRange, y_center + shieldRange ], range = shieldRange, vehicle=self)	

	def destroy(self):
		x_center, y_center = self.get_center()
		
		coordinates=self.get_scaled_coordinates_by_center(5)
		
		Debris.create( Board.canvas.coords(self.reference) )		
		
		self.flame.destroy()
		self.shield.destroy()
		super().destroy()	
	
	def move(self):
		Board.canvas.move(self.reference, self.dx, self.dy )
		Board.canvas.move(self.flame.reference, self.dx, self.dy )
	
	def rotate(self, t):
		x_center, y_center = self.get_center()
		Board.canvas.coords(self.reference, self.rotate_coordinates(x_center, y_center, t))
		Board.canvas.coords(self.flame.reference, self.flame.rotate_coordinates(x_center, y_center, t))
	
	def outbound_reset(self):
		x_center, y_center = self.get_center()
		
		if (x_center < 0): _x = _boardWidth
		elif (x_center > _boardWidth): _x  = -_boardWidth
		else: _x = 0
		
		if (y_center < 0): _y = _boardHeight
		elif (y_center > _boardHeight): _y = -_boardHeight
		else: _y = 0

		Board.canvas.coords(self.reference, self.offset_coordinates(Board.canvas.coords(self.reference), [_x, _y] ))
		Board.canvas.coords(self.flame.reference, self.offset_coordinates(Board.canvas.coords(self.flame.reference), [_x, _y] ))
		
	def acc_on(self):
		if not self.acc:
			self.acc = True
			self.flame.show()
	def acc_off(self):
		self.acc = False
		self.flame.hide()
		
	def rot_on(self):
		if not self.rot: self.rot = True
	def rot_off(self):
		self.rot = False
		
class Ship(Vehicle):
	exist = False
	respawn = False
	shot = False
	
	def __init__(
		self,
		coordinates=_shipCoordinates, 
		outline="white", 
		fill="", 
		tag="ship",
		state=NORMAL
		):
		
		Ship.exist = True
		super().__init__(coordinates, outline, fill, tag, state, 20)
		
		self.face = -math.pi / 2
		self.dx = 0
		self.dy = 0
		
		self.charge = 0
		
		self.charging = False
	
	def rotate(self, direction):
		t = math.pi / 180 * 5 * _rotationValues[direction]
		self.face -= t
		super().rotate(t)
		
	def destroy(self):
		Ship.exist = False
#		winsound.PlaySound(_bangSmall, winsound.SND_ALIAS|winsound.SND_ASYNC|winsound.SND_NOWAIT)
		
		super().destroy()

class Rocket(Vehicle):
	def __init__(
		self, 
		direction,
		coordinates=_rocketCoordinates, 
		outline="white", 
		fill="", 
		tag="rocket", 
		state=NORMAL,
		offset=[0,0],
		
		):
		
		super().__init__(self.offset_coordinates(coordinates, offset), outline, fill, tag, state, 10)
		
		Board.objectList[self.reference] = self
		
		self.ammo = 5
		self.reload = 0		
		self.face = -math.pi / 2
		self.dx = math.cos(direction)
		self.dy = math.sin(direction)
		self.target = random.choice(Board.get_asteroid_list())
		
		self.rotate(direction + math.pi*0.5)
	
	def rotate(self, face):
		self.face = (self.face + face) % (2*math.pi)
		super().rotate(-face)
	
	def board(self):
		x_center, y_center = self.get_center()		
		
		self.flame.destroy()
		self.shield.destroy()
		Board.destroy(self)
		
		del self.objectList[self.reference]
		
	def destroy(self):
#		winsound.PlaySound(_bangSmall, winsound.SND_ALIAS|winsound.SND_ASYNC|winsound.SND_NOWAIT)
		super().destroy()		
		del self.objectList[self.reference]
		
class Flame(Board):
	exist = False
	def __init__(
		self, 
		coordinates=_flameCoordinates, 
		outline="white", 
		fill="", 
		tag="flame", 
		state=HIDDEN
		):
		
		super().__init__(coordinates, outline, fill, tag, state)
		self.reference = Board.canvas.create_polygon( self.coordinates, outline=self.outline, fill=self.fill, tag=self.tag, state=self.state )

class Lazer(Board):
	def __init__(
		self,
		coordinates, 
		direction,
		outline="white", 
		fill="", 
		tag="lazer",
		state=NORMAL,
		width=2
		):
		
		super().__init__(coordinates, outline, fill, tag, state)
		self.dx = math.cos(direction) * 20
		self.dy = math.sin(direction) * 20
		
		self.reference = Board.canvas.create_line( self.coordinates, fill=self.outline, tag=self.tag, state=self.state, width=width )
		Board.objectList[self.reference] = self
		
	def destroy(self):
		super().destroy()
		del self.objectList[self.reference]		
		
class Beam(Board):
	def __init__(
		self,
		coordinates, 
		direction,
		outline="white", 
		fill="", 
		tag="beam",
		state=NORMAL,
		width=10
		):
		
		super().__init__(coordinates, outline, fill, tag, state)
		self.dx = math.cos(direction) * 20
		self.dy = math.sin(direction) * 20
		
		self.timer = random.uniform(200, 255)
		
		self.reference = Board.canvas.create_line( self.coordinates, fill=self.outline, tag=self.tag, state=self.state, width=width )
		Board.objectList[self.reference] = self
		
	def destroy(self):
		super().destroy()
		del self.objectList[self.reference]		

class Debris(Board):		
	def __init__(
		self, 
		coordinates, 
		direction=random.uniform(0, 2*math.pi),
		speed=2,
		dx=None,
		dy=None,
		outline="white", 
		fill="", 
		tag="debris", 
		state=NORMAL
		):
		
		if (dx and dy): 
			self.dx = dx * random.uniform(0,speed)
			self.dy = dy * random.uniform(0,speed)
		else:
			self.dx = math.cos(direction) * random.uniform(0,speed)
			self.dy = math.sin(direction) * random.uniform(0,speed)
		
		

		self.timer = random.uniform(20, 255)
		
		super().__init__(coordinates, outline, fill, tag, state)
		self.reference = Board.canvas.create_line( self.coordinates, fill=self.outline, tag=self.tag, state=self.state )
		Board.objectList[self.reference] = self
	
	@staticmethod
	def create(coords):
		for x in range(-2, len( coords ) - 2, 2 ):
			Debris( coordinates=[ coords[x], coords[x+1], coords[x+2], coords[x+3] ], direction=random.uniform(0, 2 * math.pi)	)	
			
	def destroy(self):
		super().destroy()
		del self.objectList[self.reference]
		
class Fume(Board):		
	def __init__(
		self, 
		coordinates, 
		direction=random.uniform(0, 2*math.pi),
		speed=2,
		dx=None,
		dy=None,
		outline="white", 
		fill="", 
		tag="fume", 
		state=NORMAL
		):
		
		if (dx and dy): 
			self.dx = dx * random.uniform(0,speed)
			self.dy = dy * random.uniform(0,speed)
		else:
			self.dx = math.cos(direction) * random.uniform(0,speed)
			self.dy = math.sin(direction) * random.uniform(0,speed)
		
		self.timer = random.uniform(20, 255)
		
		super().__init__(coordinates, outline, fill, tag, state)
		self.reference = Board.canvas.create_oval( self.coordinates, outline=self.outline, fill=self.fill, tag=self.tag, state=self.state )
		Board.objectList[self.reference] = self
			
	def destroy(self):
		super().destroy()
		del self.objectList[self.reference]		

class Explosion(Board):		
	def __init__(
		self, 
		coordinates, 
		expansionRate=1,
		outline="white", 
		fill="", 
		tag="explosion", 
		state=NORMAL,
		width=1
		):
		
		super().__init__(coordinates, outline, fill, tag, state)
		self.reference = Board.canvas.create_oval( self.coordinates, outline=self.outline, fill=self.fill, tag=self.tag, state=self.state, width=width )
		
		Board.objectList[self.reference] = self

		self.expansionRate = expansionRate
		self.timer = random.uniform(200, 255)
	
	def destroy(self):
		super().destroy()
		del self.objectList[self.reference]
	def update(self):
		super().update(10)
		self.expand(self.expansionRate)

class NuklearExplosion(Explosion):
	def __init__(
		self, 
		coordinates, 
		expansionRate=1,
		outline="white", 
		fill="", 
		tag="nuklear", 
		state=NORMAL,
		width=1
		):
		
		super().__init__(coordinates, expansionRate, outline, fill, tag, state, width )		
		
class Shield(Board):		
	def __init__(
		self, 
		coordinates, 
		vehicle,		
		outline="", 
		fill="", 
		tag="shield", 
		state=HIDDEN, 
		range = 20
		):
		
		super().__init__(coordinates, outline, fill, tag, state)
		self.reference = Board.canvas.create_oval( self.coordinates, outline=self.outline, fill=self.fill, tag=self.tag, state=self.state, width=3 )
		
		self.vehicle = vehicle
		self.shieldRange = range
		self.timer = 0
		self.cap = 100
		
	def update(self):
		scale = math.sin(random.uniform(0, 2*math.pi) )
		Board.canvas.coords( self.reference, self.vehicle.get_scaled_coordinates_by_center( self.shieldRange + scale ) )
		super().update(10)
		
class game_controller(object):
	def next_level(self):
		self.currentAsteroidNum += 1
		Thread(target=Board.generate_asteroids(self.currentAsteroidNum) ).start()
		self.nextLevelBool = True

	def set_respawn(self):
		Ship.respawn = True
	
	def update_dashboard(self):
		self.update_life()
		self.update_score()
		self.update_energy()
		self.update_fleet()
		self.update_nuke()
		self.update_cluster()
	
	def update_life(self):
		Board.canvas.itemconfig(self.lifeCounter, text="\U00002661" + " {}".format(self.currentLives), state=NORMAL)
	def update_score(self):
		Board.canvas.itemconfig(self.scoreLabel, text="Score: {}".format(Board.score), state=NORMAL )
	def update_energy(self):
		Board.canvas.itemconfig(self.energyCounter, text="\U0000269B" + " {}\U00002105".format(math.floor(self.currentEnergy)), state=NORMAL)	
	def update_fleet(self):
		Board.canvas.itemconfig(self.fleetCounter, text="\U00002693" + " {}".format(self.currentFleet), state=NORMAL)
	def update_nuke(self):
		Board.canvas.itemconfig(self.nukeCounter, text="\U00002622" + " {}".format(self.currentNukes), state=NORMAL)		
	def update_cluster(self):
		Board.canvas.itemconfig(self.clusterCounter, text="\U00002650" + " {}".format(self.currentCluster), state=NORMAL)	
		
	def game_over(self):
		Board.canvas.itemconfig(self.title, state=NORMAL, text="Game over")
		Board.canvas.itemconfig(self.instructions, state=NORMAL, text="Press Enter to play again")		
	
	def moveit(self):
		
		if Ship.respawn:
			loop = False
		
			for item in Board.canvas.find_overlapping( 
				min(_shipCoordinates[0::2]) -50, 
				min(_shipCoordinates[1::2]) -50, 
				max(_shipCoordinates[0::2]) +50, 
				max(_shipCoordinates[1::2]) +50
			):
				if Board.canvas.gettags(item) and Board.canvas.gettags(item)[0] == 'asteroid':
					loop = True
					break
			
			if not loop:
				Ship.respawn = False
				self.ship = Ship()
				Ship.shot = False
				
				self.currentEnergy = 100	
				self.currentFleet = 20		
				self.currentLives -= 1
				
				self.update_dashboard()
			
		if not Board.get_asteroid_list() and self.nextLevelBool:
			self.nextLevelBool = False
			Timer(3, self.next_level ).start()
		
		for id, object in Board.objectList.copy().items():
			if Board.canvas.gettags(id):
				if Board.canvas.gettags(id)[0] == 'bullet':
					if object.is_outbound():
						object.destroy()
					else:
						for item in object.get_overlapping():
							if Board.canvas.gettags(item)[0] == 'bullet' or Board.canvas.gettags(item)[0] == 'ship':
								continue
							elif Board.canvas.gettags(item)[0] == 'asteroid':
								Explosion( coordinates=object.get_scaled_coordinates_by_center(5) )
								Board.objectList[item].destroy()
								object.destroy()
								self.update_score()
								break
						object.move()
						
				elif Board.canvas.gettags(id)[0] == 'clusterbomb':
					if object.is_outbound():
						object.destroy()
					else:
						for item in object.get_overlapping():
							if Board.canvas.gettags(item)[0] == 'clusterbomb' or Board.canvas.gettags(item)[0] == 'ship':
								continue
							elif Board.canvas.gettags(item)[0] == 'asteroid':
								Explosion( coordinates=object.get_scaled_coordinates_by_center(5) )
								Board.objectList[item].destroy()
								
								for i in range(150):
									Bullet(
									[
										Board.canvas.coords(object.reference)[0]-1, 
										Board.canvas.coords(object.reference)[1]-1, 
										Board.canvas.coords(object.reference)[0]+1, 
										Board.canvas.coords(object.reference)[1]+1
									], random.uniform(0,2*math.pi))
								
								object.destroy()
								self.update_score()
								break
						object.move()						

				elif Board.canvas.gettags(id)[0] == 'plague':
					if object.is_outbound():
						object.destroy()
					else:
						for item in object.get_overlapping():
							if Board.canvas.gettags(item)[0] == 'clusterbomb' or Board.canvas.gettags(item)[0] == 'ship':
								continue
							elif Board.canvas.gettags(item)[0] == 'asteroid':
								Explosion( coordinates=object.get_scaled_coordinates_by_center(5) )
								Board.objectList[item].destroy()
								
								for i in range(5):
									Plague(
									[
										Board.canvas.coords(object.reference)[0]-3, 
										Board.canvas.coords(object.reference)[1]-3, 
										Board.canvas.coords(object.reference)[0]+3, 
										Board.canvas.coords(object.reference)[1]+3
									], random.uniform(0,2*math.pi))
								
								object.destroy()
								self.update_score()
								break
						object.move()
						Board.canvas.itemconfig(object.reference, 
							fill=object.get_color_by_timer(math.floor(random.uniform(0, 255))), 
							outline=object.get_color_by_timer(math.floor(random.uniform(0, 255)))
						)						
				elif Board.canvas.gettags(id)[0] == 'chargedbullet':
					if object.is_outbound():
						object.destroy()
					else:
						for item in object.get_overlapping():
							if Board.canvas.gettags(item)[0] == 'chargedbullet' or Board.canvas.gettags(item)[0] == 'ship':
								continue
							elif Board.canvas.gettags(item)[0] == 'asteroid':
								Explosion( coordinates=object.get_scaled_coordinates_by_center(5) )
								Board.objectList[item].destroy()
								
								self.update_score()
								break
						object.move()						
						Board.canvas.itemconfig(object.reference, 
							fill="#" + '{0:x}{0:x}{0:x}'.format( 
							math.floor(random.uniform(0, object.charge )) ), 
							
							outline="#" + '{0:x}{0:x}{0:x}'.format( 
							math.floor(random.uniform(13, 13 + object.charge )) )
						)						

				elif Board.canvas.gettags(id)[0] == 'gravity':
					if object.timer == 0:
						object.destroy()
					else:
						for item in object.get_overlapping():
							if Board.canvas.gettags(item)[0] == 'gravity' or Board.canvas.gettags(item)[0] == 'ship':
								continue
							elif Board.canvas.gettags(item)[0] not in ['ship', 'gravity', 'explosion', 'flame', 'shield', 'nuklear']:
								Explosion( coordinates=object.get_scaled_coordinates_by_center(5) )
								Board.objectList[item].destroy()
								
								self.update_score()
								break
								
						for _id, _object in Board.objectList.copy().items():
							if Board.canvas.gettags(_id) and Board.canvas.gettags(_id)[0] not in ['ship', 'gravity', 'explosion', 'flame', 'shield', 'nuklear']:
								
								face = _object.get_target_angle(object)
								
								x1, y1 = _object.get_center()
								x2, y2 =  object.get_center()
								
								dist = 5 / ( abs(math.hypot(x2 - x1, y2 - y1)) / 5)
								if dist > 15: dist = 15
								
								if _object.dx + math.cos(face) > -3 and _object.dx + math.cos(face) < 3 :
									_object.dx += math.cos(face) * dist
								elif (_object.dx < -3 and math.cos(face) > 0) or (_object.dx > 3 and math.cos(face) < 0):
									_object.dx += math.cos(face) * dist
									
								if _object.dy + math.sin(face)*-1 > -3 and _object.dy + math.sin(face)*-1 < 3 :	
									_object.dy += math.sin(face)*-1 * dist
								elif (_object.dy < -3 and math.sin(face)*-1 > 0) or (_object.dy > 3 and math.sin(face)*-1 < 0):
									_object.dy += math.sin(face)*-1 * dist
									
#								print(face, math.cos(face), math.sin(face))
								
						Board.canvas.itemconfig(object.reference, 
							fill="#" + '{0:x}{0:x}{0:x}'.format( 
							math.floor(random.uniform(16, 50 )) ), 
							
							outline="#" + '{0:x}{0:x}{0:x}'.format( 
							math.floor(random.uniform(16, 50 )) ),
							
							width=math.floor(random.uniform(16, 50 ))
						)
						object.timer -=1

				elif Board.canvas.gettags(id)[0] == 'nuke':
					if object.is_outbound():
						object.destroy()
					else:
						for item in object.get_overlapping():
							if Board.canvas.gettags(item)[0] in ['nuke', 'ship', 'debris']:
								continue
							elif Board.canvas.gettags(item)[0] == 'asteroid':
								NuklearExplosion( coordinates=object.get_scaled_coordinates_by_center(15), expansionRate=15, width=100 )
								Board.objectList[item].destroy()							
								object.destroy()
								self.update_score()
								break
						object.move()		
				elif Board.canvas.gettags(id)[0] =='lazer':
					if object.is_outbound():
						object.destroy()
					else:
						for item in object.get_overlapping():
							if Board.canvas.gettags(item)[0] == 'lazer' or Board.canvas.gettags(item)[0] == 'ship':
								continue
							elif Board.canvas.gettags(item)[0] == 'asteroid':
								Explosion( coordinates=object.get_scaled_coordinates_by_center(5) )
								Board.objectList[item].destroy()
								self.update_score()
								break
						object.move()
				
				elif Board.canvas.gettags(id)[0] =='beam':
					if object.timer < 0:
						object.destroy()
					else:	
						for item in object.get_overlapping():
							if Board.canvas.gettags(item)[0] == 'beam' or Board.canvas.gettags(item)[0] == 'ship':
								continue
							elif Board.canvas.gettags(item)[0] == 'asteroid':
								Explosion( coordinates=object.get_scaled_coordinates_by_center(5) )
								Board.objectList[item].destroy()
								self.update_score()
								break
						Board.canvas.itemconfig(object.reference, fill=object.get_color_by_timer(object.timer))
						object.timer -= random.uniform(10,20)
						
				elif Board.canvas.gettags(id)[0] == 'explosion':
					if object.timer < 0:
						object.destroy()
					else:				
						object.update()
						object.timer -= random.uniform(0,10)
				elif Board.canvas.gettags(id)[0] == 'nuklear':
					if object.timer < 0:
						object.destroy()
					else:				
						object.update()
						object.timer -= random.uniform(0,1)
						for item in object.get_overlapping():
							if Board.canvas.gettags(item) and Board.canvas.gettags(item)[0] in [ 'asteroid', 'rocket' ]:
								Explosion( coordinates=Board.objectList[item].get_scaled_coordinates_by_center(5) )
								Board.objectList[item].destroy()
								self.update_score()		
				elif Board.canvas.gettags(id)[0] == 'asteroid':			
					for item in Board.canvas.find_overlapping( object.min_x() + 5, object.min_y() + 5, object.max_x() - 5, object.max_y() - 5 ):
						if Board.canvas.gettags(item) and Board.canvas.gettags(item)[0] == 'ship':
							if self.currentEnergy > 0:
								self.currentEnergy -= 1
								self.ship.shield.timer = 255
								self.update_energy()		
								self.ship.shield.show()
								self.ship.shield.update()
							else:
								self.ship.destroy()
								if self.currentLives >= 1:
									Timer(3, self.set_respawn ).start()
								else:
									self.game_over()
					object.outbound_reset()
					object.move()
				elif Board.canvas.gettags(id)[0] == 'debris':
					if object.timer < 0:
						object.destroy()
					else:
						Board.canvas.itemconfig(object.reference, fill="#" + '{0:x}'.format(int(object.timer))*3)
						object.move()
						object.timer -= random.uniform(0,3)	
						
				elif Board.canvas.gettags(id)[0] == 'fume':
					if object.timer < 0:
						object.destroy()
					else:
						Board.canvas.itemconfig(object.reference, outline="#" + '{0:x}'.format(int(object.timer))*3)
						object.move()
						object.timer -= random.uniform(0,3)	
						
				elif Board.canvas.gettags(id)[0] == 'rocket':
					object.outbound_reset()
					x_center, y_center = object.get_center()
					if object.target == None:
						if Ship.exist:
							object.target = self.ship
					if not Ship.exist:
						object.target = None
					if object.reload != 0:
						object.reload -= 1
					if object.ammo == 0:
						if Ship.exist:
							object.target = self.ship
						else:
							object.target = None
					if object.reload == 0 and object.ammo != 0:
						for item in Board.canvas.find_overlapping(x_center, y_center, x_center + object.dx * 30, y_center + object.dy * 30):
							if Board.canvas.gettags(item)[0] == 'asteroid':
								Bullet( object.get_scaled_coordinates_by_reference(1), object.face)
								object.reload = 20
								object.ammo -= 1
					for item in object.get_overlapping():
						if Board.canvas.gettags(item):
							if Board.canvas.gettags(item)[0] == 'ship' and object.target == self.ship:
								object.target = None
								object.board()
								self.currentFleet += 1
								self.update_fleet()
							elif Board.canvas.gettags(item)[0] == 'asteroid':
								if object.shield.cap > 0:
									object.shield.cap -= 10
									object.shield.timer = 255
									Board.canvas.itemconfig(object.shield.reference, outline="white", state=NORMAL )
								else:
									Explosion( coordinates=object.get_scaled_coordinates_by_center(5) )
									Board.objectList[item].destroy("rocket")
									object.target = None
									object.destroy()
									self.update_score()
									break
					if id in Board.objectList:
						if object.target not in Board.get_asteroid_list():
							if Ship.exist:
								object.target = self.ship
							else:
								object.target = None
						if object.target:
							rotation = ( 2*math.pi - object.face - object.get_target_angle(object.target) ) % ( 2 * math.pi)
							if rotation > 1 and rotation < math.pi - 1:
								object.rotate( 0.1 )
							elif rotation > math.pi + 1 and rotation < 2*math.pi - 1:
								object.rotate( -0.1 )
							else:
								object.rotate( 0.1 )
							object.dx = math.cos(object.face) * 5
							object.dy = math.sin(object.face) * 5
						object.move()	
						object.shield.update()						
						
		if Ship.exist:
			
			if self.currentEnergy < 100 and not self.ship.charging:
				self.currentEnergy += 0.01
				self.update_energy()
			
			if self.ship.charging:
				if self.ship.charge < 20:
					self.ship.charge += 0.1
					self.currentEnergy -= 0.1
					
					
					
				Board.canvas.itemconfig(self.ship.reference, 
					fill="#" + '{0:x}{0:x}{0:x}'.format( 
					math.floor(random.uniform(0, self.ship.charge )) ), 
					
					outline="#" + '{0:x}{0:x}{0:x}'.format( 
					math.floor(random.uniform(13, 13 + self.ship.charge )) ), 
					
					width=math.floor(random.uniform(1, self.ship.charge ))
					)
				self.update_energy()
				
			self.ship.shield.update()
			self.ship.outbound_reset()
			
			if self.ship.acc:
				if self.ship.dx + _acc_rate * math.cos(self.ship.face) < _max_max and self.ship.dx + _acc_rate * math.cos(self.ship.face) > -_max_max:
					self.ship.dx += _acc_rate * math.cos(self.ship.face) 
				if self.ship.dy + _acc_rate * math.sin(self.ship.face) < _max_max and self.ship.dy + _acc_rate * math.sin(self.ship.face) > -_max_max:
					self.ship.dy += _acc_rate * math.sin(self.ship.face) 
					
				x, y = self.ship.flame.get_center()	
					
				Fume( coordinates=[ 
					x - 1, 
					y - 1, 
					x + 1 , 
					y + 1 ], dx=math.cos(self.ship.face)*-1, dy=math.sin(self.ship.face)*-1, speed=10	)
					
			if self.ship.rot:
				self.ship.rotate(self.ship.rotationDir)
			
			self.ship.move()
		
		if Board.gameState == False:
			self.new_game()
		else:
			self.root.after(_frameRate, self.moveit)
	
	def fullscreen(self, event=None):
		self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))
	
	def	bullet(self, event=None):
		if Ship.exist:
			if Ship.shot:
				pass
			else:
#				winsound.PlaySound(_fire, winsound.SND_ALIAS|winsound.SND_ASYNC|winsound.SND_NOWAIT)
				
				Bullet(
				[
					Board.canvas.coords(self.ship.reference)[0]-1, 
					Board.canvas.coords(self.ship.reference)[1]-1, 
					Board.canvas.coords(self.ship.reference)[0]+1, 
					Board.canvas.coords(self.ship.reference)[1]+1
				], self.ship.face)
				Ship.shot = True
				
	def unbullet(self, event=None):
		Ship.shot = False

	def	gravity(self, event=None):
		if Ship.exist:
			if Ship.shot:
				pass
			else:
#				winsound.PlaySound(_fire, winsound.SND_ALIAS|winsound.SND_ASYNC|winsound.SND_NOWAIT)
				
				GravityBomb(
				[
					Board.canvas.coords(self.ship.reference)[0]-30, 
					Board.canvas.coords(self.ship.reference)[1]-30, 
					Board.canvas.coords(self.ship.reference)[0]+30, 
					Board.canvas.coords(self.ship.reference)[1]+30
				])
				Ship.shot = True
				
	def ungravity(self, event=None):
		Ship.shot = False
		
	def	cluster(self, event=None):
		if Ship.exist:
			if Ship.shot:
				pass
			elif self.currentCluster > 0:
#				winsound.PlaySound(_fire, winsound.SND_ALIAS|winsound.SND_ASYNC|winsound.SND_NOWAIT)
				
				ClusterBomb(
				[
					Board.canvas.coords(self.ship.reference)[0]-2, 
					Board.canvas.coords(self.ship.reference)[1]-2, 
					Board.canvas.coords(self.ship.reference)[0]+2, 
					Board.canvas.coords(self.ship.reference)[1]+2
				], self.ship.face)
				Ship.shot = True
				self.currentCluster -= 1
				self.update_cluster()
				
	def uncluster(self, event=None):
		Ship.shot = False		

	def	plague(self, event=None):
		if Ship.exist:
			if Ship.shot:
				pass
			else:
#				winsound.PlaySound(_fire, winsound.SND_ALIAS|winsound.SND_ASYNC|winsound.SND_NOWAIT)
				
				Plague(
				[
					Board.canvas.coords(self.ship.reference)[0]-2, 
					Board.canvas.coords(self.ship.reference)[1]-2, 
					Board.canvas.coords(self.ship.reference)[0]+2, 
					Board.canvas.coords(self.ship.reference)[1]+2
				], self.ship.face)
				Ship.shot = True
				
	def unplague(self, event=None):
		Ship.shot = False			
		
	def	lazer(self, event=None):
		if Ship.exist:
			if Ship.shot:
				pass
			elif self.currentEnergy >= 5:
#				winsound.PlaySound(_fire, winsound.SND_ALIAS|winsound.SND_ASYNC|winsound.SND_NOWAIT)
				
				Lazer(
				[
					Board.canvas.coords(self.ship.reference)[0]-(20*math.cos(self.ship.face)), 
					Board.canvas.coords(self.ship.reference)[1]-(20*math.sin(self.ship.face)), 
					Board.canvas.coords(self.ship.reference)[0]+(20*math.cos(self.ship.face)), 
					Board.canvas.coords(self.ship.reference)[1]+(20*math.sin(self.ship.face))
				], self.ship.face)
				Ship.shot = True
				self.currentEnergy -= 5
				self.update_energy()
				
	def unlazer(self, event=None):
		Ship.shot = False	
		
	def	beam(self, event=None):
		if Ship.exist:
			if Ship.shot:
				pass
			elif self.currentEnergy >= 5:
#				winsound.PlaySound(_fire, winsound.SND_ALIAS|winsound.SND_ASYNC|winsound.SND_NOWAIT)
				
				Beam(
				[
					Board.canvas.coords(self.ship.reference)[0]-(math.cos(self.ship.face)), 
					Board.canvas.coords(self.ship.reference)[1]-(math.sin(self.ship.face)), 
					Board.canvas.coords(self.ship.reference)[0]+2*(self.root.winfo_screenwidth()*math.cos(self.ship.face)), 
					Board.canvas.coords(self.ship.reference)[1]+2*(self.root.winfo_screenheight()*math.sin(self.ship.face))
				], self.ship.face)
				Ship.shot = True
				self.currentEnergy -= 1
				self.update_energy()
				
	def unbeam(self, event=None):
		Ship.shot = False			

	def charge(self, event=None):
		self.ship.charging = True	
		
	def uncharge(self, event=None):
		self.ship.charging = False	
		if self.ship.charge >= 5:
#			winsound.PlaySound(_fire, winsound.SND_ALIAS|winsound.SND_ASYNC|winsound.SND_NOWAIT)
			ChargedBullet(
			[
				Board.canvas.coords(self.ship.reference)[0]-self.ship.charge, 
				Board.canvas.coords(self.ship.reference)[1]-self.ship.charge, 
				Board.canvas.coords(self.ship.reference)[0]+self.ship.charge, 
				Board.canvas.coords(self.ship.reference)[1]+self.ship.charge
			], self.ship.face, self.ship.charge, width=self.ship.charge)			
		
		self.ship.charge = 0
		Board.canvas.itemconfig(self.ship.reference, outline="white", fill="", width=1)

	def	rocket(self, event=None):
		if Ship.exist:
			if Ship.shot:
				pass
			elif self.currentFleet > 0:
#				winsound.PlaySound(_fire, winsound.SND_ALIAS|winsound.SND_ASYNC|winsound.SND_NOWAIT)

				Rocket(
					offset=[
						Board.canvas.coords(self.ship.reference)[0], 
						Board.canvas.coords(self.ship.reference)[1]
					], direction=self.ship.face
				)
				
				Ship.shot = True
				self.currentFleet -= 1
				self.update_fleet()
				
	def unrocket(self, event=None):
		Ship.shot = False

	def	nuke(self, event=None):
		if Ship.exist:
			if Ship.shot:
				pass
			elif self.currentNukes > 0:
#				winsound.PlaySound(_fire, winsound.SND_ALIAS|winsound.SND_ASYNC|winsound.SND_NOWAIT)
				
				Nuke(
				[
					Board.canvas.coords(self.ship.reference)[0]-1, 
					Board.canvas.coords(self.ship.reference)[1]-1, 
					Board.canvas.coords(self.ship.reference)[0]+1, 
					Board.canvas.coords(self.ship.reference)[1]+1
				], self.ship.face)
				Ship.shot = True
				self.currentNukes -= 1
				self.update_nuke()
				
	def unnuke(self, event=None):
		Ship.shot = False
		
	def	rotate(self, event=None):
		if Ship.exist:
			self.ship.rotationDir = event.keysym
			self.ship.rot_on()
	def	unrotate(self, event=None):
		self.rotationDir = None
		self.ship.rot_off()
		
	def on(self, event=None):
		if Ship.exist:
			self.ship.acc_on()
	def off(self, event=None):
		if Ship.exist:
			self.ship.acc_off()

	def new_game(self, event=None):
		if Board.gameState == None:
			Board.gameState = False
		elif Board.gameState == False:
			for id, object in Board.objectList.copy().items():
				Board.destroy(object)					
			
			if Ship.exist:
				Board.destroy(self.ship)
			
			Board.score = 0
			self.nextLevelBool = True
			Ship.respawn = False
			
			self.currentLives = 5
			self.currentFleet = 20
			self.currentNukes = 5
			self.currentCluster = 5
			
			self.currentEnergy = 100
			self.ship = Ship()
			
			#Board.canvas.scale(self.ship.reference, 0,0, 0.1,0.1)
			
			#print(Board.canvas.coords(self.ship.reference))
			
			Ship.shot = False
			
			self.currentAsteroidNum = 20
			Board.generate_asteroids(self.currentAsteroidNum)
			
			Board.canvas.itemconfig(self.title, state=HIDDEN)
			Board.canvas.itemconfig(self.instructions, state=HIDDEN)
			
			self.update_dashboard()
			
			Board.gameState = True		
			self.root.after(_frameRate, self.moveit)
		elif Board.gameState:
			Board.gameState = False
			
# 	Quit game		
	def quit(self):
		self.root.destroy()	
		
# 	Setup control bindings
	def set_controls(self):
		self.root.bind('<Left>', self.rotate)
		self.root.bind('<Right>', self.rotate)
		
		self.root.bind('<KeyRelease-Left>', self.unrotate)
		self.root.bind('<KeyRelease-Right>', self.unrotate)
		
		self.root.bind('<Return>', self.new_game)

		self.root.bind('a', self.rocket)
		self.root.bind('<KeyRelease-a>', self.unrocket)

		self.root.bind('q', self.lazer)
		self.root.bind('<KeyRelease-q>', self.unlazer)

		self.root.bind('r', self.cluster)
		self.root.bind('<KeyRelease-r>', self.uncluster)

		self.root.bind('t', self.plague)
		self.root.bind('<KeyRelease-t>', self.unplague)
		
		self.root.bind('e', self.beam)
		self.root.bind('<KeyRelease-e>', self.unbeam)
		
		self.root.bind('w', self.charge)
		self.root.bind('<KeyRelease-w>', self.uncharge)

		self.root.bind('d', self.gravity)
		self.root.bind('<KeyRelease-d>', self.ungravity)
		
		self.root.bind('s', self.nuke)
		self.root.bind('<KeyRelease-s>', self.unnuke)
		
		self.root.bind('<Up>', self.on)
		self.root.bind('<KeyRelease-Up>', self.off)
		self.root.bind('<space>', self.bullet)
		self.root.bind('<KeyRelease-space>', self.unbullet)	

		self.root.bind('<Escape>', self.fullscreen)
		
#	Initialize main game object		
	def __init__(self, root):
		self.root = root
		
		Board.canvas = Canvas(root, width=_boardWidth, height=_boardHeight, bg="black")
		Board.canvas.pack()
		
		self.title = Board.canvas.create_text(_boardWidth*0.5, _boardHeight*0.2, text="Asteroids Tk", font=Font(family="Alien Encounters", size=round(40 * (_boardHeight / 400)) ), fill="white", tag="title")
		self.instructions = Board.canvas.create_text(_boardWidth*0.5, _boardHeight*0.6, text="Press Enter to start", font=Font(family="Alien Encounters", size=round(15 * (_boardHeight / 400))), fill="white", tag="instructions")
		self.lifeCounter = Board.canvas.create_text(_boardWidth*0.1, _boardHeight*0.1, text="\U00002661" + " 0", font=Font(family="Alien Encounters", size=round(10 * (_boardHeight / 400))), fill="white", tag="lives", state=HIDDEN)
		


		self.energyCounter = Board.canvas.create_text(_boardWidth*0.2, _boardHeight*0.1, text="\U0000269B" + " 0", font=Font(family="Alien Encounters", size=round(10 * (_boardHeight / 400))), fill="white", tag="energy", state=HIDDEN)
	
		
		
		self.nukeCounter = Board.canvas.create_text(_boardWidth*0.1, _boardHeight*0.2, text="\U00002622" + " 0", font=Font(family="Alien Encounters", size=round(10 * (_boardHeight / 400))), fill="white", tag="nuke", state=HIDDEN)
		self.fleetCounter = Board.canvas.create_text(_boardWidth*0.1, _boardHeight*0.25, text="\U00002693" + " 0", font=Font(family="Alien Encounters", size=round(10 * (_boardHeight / 400))), fill="white", tag="fleet", state=HIDDEN)			
		self.clusterCounter = Board.canvas.create_text(_boardWidth*0.1, _boardHeight*0.3, text="\U00002694" + " 0", font=Font(family="Alien Encounters", size=round(10 * (_boardHeight / 400))), fill="white", tag="fleet", state=HIDDEN)
		
		
		self.scoreLabel = Board.canvas.create_text(_boardWidth*0.9, _boardHeight*0.1, text="Score: 0", font=Font(family="Alien Encounters", size=round(10 * (_boardHeight / 400))), fill="white", tag="score", state=HIDDEN)
		self.set_controls()
		
		self.tester = Board.canvas.create_text(_boardWidth*0.5, _boardHeight*0.1, text="Tester", font=Font(family="Alien Encounters", size=round(5 * (_boardHeight / 400))), fill="white", tag="score", state=NORMAL)
		
		self.currentAsteroidNum = 4
		Board.generate_asteroids(self.currentAsteroidNum)
		
		self.root.after(_frameRate, self.moveit)
		
if __name__ == "__main__":
	root = Tk()
	
	root.wm_state('zoomed')
	root.attributes('-fullscreen', True)
	
	_boardWidth = root.winfo_screenwidth()
	_boardHeight = root.winfo_screenheight()
	
	root.title("Asteroids Tk")
	game = game_controller(root);
	root.mainloop()
