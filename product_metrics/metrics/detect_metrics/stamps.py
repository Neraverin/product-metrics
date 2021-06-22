from ..base_type import BaseType
from ..base_metric import BaseMetric
from ..metric_helper import MetricHelper
from wallarm_api import WallarmAPI

start_date = int(1617224400)
end_date = int(1622322000)

interval = "01.04-30.05"

BINARY_DATA_STAMPS = [57, 59, 85, 111, 145, 146, 148, 150, 170, 172, 235, 237, 247, 248,
                      293, 294, 300, 307, 308, 321, 322, 323, 340, 341, 342, 343, 344,
                      345, 347, 348, 349, 350, 353, 354, 355, 357, 361, 362, 376, 377,
                      392, 393, 396, 398, 399, 402, 403, 405, 410, 413, 453, 454, 458,
                      469, 472, 473, 474, 476, 477, 491, 515, 517, 527, 529, 539, 541,
                      551, 553, 619, 620, 621, 622, 645, 646, 651, 652, 657, 658, 663,
                      664, 687, 688, 689, 690, 694, 695, 696, 697, 710, 738, 759, 763,
                      767, 768, 769, 770, 772, 776, 777, 778, 781, 782, 784, 788, 789,
                      790, 793, 794, 798, 799, 800, 801, 846, 847, 848, 849, 858, 859,
                      860, 861, 870, 871, 872, 873, 906, 907, 908, 909, 918, 919, 920,
                      921, 940, 984, 985, 992, 995, 1001, 1004, 1007, 1008, 1009, 1014,
                      1015, 1016, 1026, 1028, 1033, 1038, 1062, 1063, 1074, 1157, 1161,
                      1169, 1170, 1171, 1173, 1174, 1175, 1177, 1178, 1179, 1180, 1181,
                      1182, 1183, 1184, 1186, 1187, 1188, 1189, 1190, 1191, 1192, 1195,
                      1196, 1197, 1198, 1199, 1200, 1202, 1215, 1219, 1237, 1251, 1252,
                      1258, 1260, 1263, 1264, 1316, 1317, 1318, 1319, 1340, 1341, 1342,
                      1343, 1376, 1377, 1378, 1379, 1388, 1389, 1390, 1391, 1411, 1412,
                      1414, 1419, 1423, 1425, 1426, 1429, 1431, 1433, 1436, 1437, 1438,
                      1439, 1461, 1556, 1557, 1559, 1560, 1592, 1593, 1595, 1596, 1616,
                      1617, 1619, 1620, 1640, 1641, 1643, 1644, 1652, 1653, 1655, 1656,
                      1664, 1665, 1667, 1668, 1712, 1713, 1715, 1716, 1748, 1749, 1751,
                      1752, 1760, 1761, 1763, 1764, 1772, 1773, 1775, 1776, 1868, 1869,
                      1871, 1872, 1892, 1893, 1895, 1896, 1940, 1941, 1943, 1944, 1952,
                      1953, 1955, 1956, 1995, 2000, 2008, 2010, 2011, 2012, 2014, 2015,
                      2017, 2047, 2049, 2051, 2053, 2055, 2056, 2057, 2061, 2063, 2064,
                      2065, 2070, 2072, 2075, 2076, 2079, 2081, 2083, 2085, 2086, 2087,
                      2091, 2093, 2094, 2095, 2100, 2102, 2105, 2106, 2109, 2110, 2112,
                      2113, 2133, 2134, 2135, 2136, 2155, 2156, 2157, 2158, 2165, 2166,
                      2167, 2168, 2187, 2188, 2189, 2190, 2197, 2198, 2199, 2200, 2219,
                      2220, 2221, 2222, 2229, 2230, 2231, 2232, 2235, 2236, 2237, 2238,
                      2245, 2246, 2247, 2248, 2251, 2252, 2253, 2254, 2261, 2262, 2263,
                      2264, 2601, 2605, 2846, 2857, 2858, 2861, 2875, 2876, 2878, 2881,
                      2883, 2886, 5610, 5681, 5824, 5826, 5827, 5828, 5830, 5831, 5832,
                      5833, 5834, 5835, 5836, 5837, 5838, 5839, 5840, 5841]


STAMPS = {
    # djvu, pdf, ppt pptx, ...
    "docs": [293, 294, 300, 321, 322, 323, 349, 396, 403, 405, 413, 469, 472,
             473, 474, 619, 620, 621, 622, 768, 769, 770, 984, 985, 992, 1004,
             1007, 1009, 1016, 1028, 1038, 1064, 1170, 1173, 1174, 1178, 1189,
             1197, 1198, 1198, 1199, 1214, 1214, 1216, 1218, 1219, 1219],

    # html, css, js
    "html": [57, 59, 145, 146, 148, 170, 172, 237, 247, 293, 294, 300, 341, 344,
             345, 347, 349, 350, 353, 354, 355, 361, 362, 376, 377, 391, 392,
             393, 402, 405, 410, 413, 453, 472, 474, 491, 619, 620, 710, 726,
             738, 761, 767, 985, 1004, 1007, 1008, 1014, 1015, 1026, 1067, 1123,
             1123, 1124, 1124, 1125, 1125, 1178, 1178, 1207, 1209, 1212, 1214,
             1214, 1215, 1215, 1217, 1217, 1218, 1219, 1219, 1232, 1411],

    # jpg, png, tif, ...
    "images": [235, 293, 294, 300, 307, 323, 344, 347, 349, 353, 354, 355, 357,
               361, 376, 377, 393, 396, 402, 403, 405, 413, 453, 469, 472, 473,
               474, 491, 619, 620, 621, 622, 767, 768, 769, 770, 781, 985, 992,
               1004, 1009, 1014, 1016, 1028, 1033, 1038, 1090, 1170, 1173, 1173,
               1174, 1178, 1189, 1190, 1197, 1198, 1199, 1209, 1214, 1214, 1215,
               1216, 1216, 1217, 1219, 1232, 1411],

    # ape, flac, mp3, wv, ...
    "music": [293, 294, 300, 308, 321, 323, 349, 396, 403, 413, 469, 472, 473,
              474, 619, 620, 621, 622, 768, 769, 770, 992, 1004, 1009, 1014,
              1016, 1028, 1033, 1038, 1170, 1173, 1173, 1174, 1178, 1178, 1189,
              1197, 1198, 1199, 1214, 1214, 1216, 1216, 1218, 1218, 1219, 1219],

    # flv, mp4, ...
    "video": [293, 300, 307, 321, 323, 349, 396, 403, 413, 469, 472, 473, 474,
              619, 620, 621, 622, 768, 769, 770, 992, 1004, 1009, 1014, 1016,
              1028, 1033, 1038, 1170, 1173, 1174, 1178, 1189, 1190, 1197, 1198,
              1199, 1214, 1214, 1216, 1216, 1218, 1218, 1219, 1219]}


class StampsMetric(BaseType):
    def count_stamps_by_client(self, hint_type):
        stamps = {}
        clients_id = [client.id for client in MetricHelper().real_clients]

        i = 0
        while True:
            hints = WallarmAPI().hints_api.get_hint_details(
                type=[hint_type], clientid=clients_id, limit=100, offset=i*100, create_time=[[start_date, end_date]])
            for hint in hints:
                if hint.stamp in stamps.keys():
                    stamps[hint.stamp] += 1
                else:
                    stamps[hint.stamp] = 1
            i += 1
            if len(hints) < 100:
                break

        return stamps

    class CountDisableStampsByType(BaseMetric):
        def __init__(self, stamp_id, count, row):
            super().__init__(f"Disable Stamp {stamp_id} {interval}", row)
            self.stamp_id = stamp_id
            self.count = count

        def value(self) -> int:
            return self.count

    class CountExperimentalStampsByType(BaseMetric):
        def __init__(self, stamp_id, count):
            super().__init__(
                f"Experimental Stamp {stamp_id} {interval}", stamp_id+1)
            self.stamp_id = stamp_id
            self.count = count

        def value(self) -> int:
            return self.count

    def count_binary_data_stamps(self, disabled_stamps: dict):
        binary_data_stamps = 0
        for stamp_id, count in disabled_stamps.items():
            if stamp_id in BINARY_DATA_STAMPS:
                binary_data_stamps += count

        print("Binary data stamps ", binary_data_stamps)
        return binary_data_stamps

    def count_uploads_stamps(self, disabled_stamps: dict):
        upload_stamps = {"docs": 0, "html": 0, "images": 0, "music": 0, "video": 0}


    def collect_metrics(self):
        disabled_stamps = self.count_stamps_by_client("disable_stamp")
        self.count_binary_data_stamps(disabled_stamps)
        #experimental_stamps = self.count_stamps_by_client("experimental_stamp")
        f = open('disabled_stamps.txt', 'w')
        f.write(repr(disabled_stamps))
        f.close()


        i = 0
        metrics = []
        # for stamp_id, count in disabled_stamps.items():
        #     i += 1
        #     # + [
        #     metrics.append(self.CountDisableStampsByType(
        #         stamp_id, count, i + 1))
        #     # self.CountExperimentalStampsByType(stamp_id, count) for stamp_id, count in experimental_stamps]
        return metrics
