
import time
import numpy as np
import psutil
import torch

# Import customized libraries
from src.VFBLS_v110.VFBLS_realtime import vfbls_demo_new
from src.VFBLS_v110.BLS_realtime import bls_demo_train_test_new
from src.modelOcean.gru_2layer_demo import gru2_demo_new
import new_utils

def real_defense(file_path):
    models = ['VFBLS', 'BLS', 'GRU']
    # models = ['VFBLS','BLS']
    num_reg, num_ano = 0, 0
    t_utc = ''
    web_results = ''
    for ALGO in models:
        num_reg, num_ano = 0, 0
        if ALGO == 'VFBLS':
            # VFBLS
            predicted_labels, test_hour_chart, test_min_chart, web_results = vfbls_demo_new(file_path, "low")
            # predicted_labels, test_hour_chart, test_min_chart, web_results = vfbls_demo_train_test()
            # print("predicted", predicted_labels)  # type: [2.0, 1.0, ...]
            # print("test_hour", test_hour_chart)  # type: ['01', '01', ...]
            # print("web_results", web_results)
        elif ALGO == 'BLS':
            # BLS
            predicted_labels, test_hour_chart, test_min_chart, web_results = bls_demo_train_test_new(file_path, "all",
                                                                                                     "low")
        elif ALGO == 'GRU':
            # GRU
            if torch.cuda.is_available():
                predicted_labels, test_hour_chart, test_min_chart, web_results = gru2_demo_new(file_path)
            else:
                predicted_labels, test_hour_chart, test_min_chart, web_results = vfbls_demo_new(file_path, "low")
                print("No GPU available, use VFBLS instead.")
        else:
            print("Invalid algorithm. Please re-enter.")
            exit()

        t_utc = time.strftime('%a, %d %b %Y %H:%M:%S', time.gmtime())

        # Prepare uct time, features
        t_ann = []  # t_ann = ['01:45', '01:46', ...]
        for i in range(len(test_hour_chart)):
            t_ann.append(test_hour_chart[i] + ':' + test_min_chart[i])

        path_app = '../'
        data_for_plot = np.loadtxt(file_path)
        data_for_plot_ann = data_for_plot[:, 4]
        data_for_plot_ann = data_for_plot_ann.tolist()
        data_for_plot_wdrl = data_for_plot[:, 5]
        data_for_plot_wdrl = data_for_plot_wdrl.tolist()
        # print(t_ann)
        # print(data_for_plot_ann)

        # Prepare labels, uct time
        for i in range(len(predicted_labels)):
            if predicted_labels[i] == 2:
                predicted_labels[i] = 0

        # Prepare multi-core cpu usage, uct time
        t_cpu = time.strftime('%H:%M:%S', time.gmtime())
        cpus = psutil.cpu_percent(interval=None, percpu=True)  # percentages for each core, 10 elements
        cpus_avg = round(sum(cpus) / len(cpus), 2)  # %.2f
        cpus_avg = [cpus_avg]
        t_cpu = 1 * [t_cpu]  # element type: string

        for regAno in predicted_labels:
            if regAno == 1:
                num_ano += 1
            else:
                num_reg += 1
        json_req = {ALGO:
            {
                "prediction": {
                    # "desc": "Prediction vs. time",
                    "times": t_ann,
                    "values": predicted_labels,
                },
                "feature": {
                    # "desc": "Volume features vs. time",
                    "times": t_ann,
                    "announcementValue": data_for_plot_ann,
                    "withdrawalValue": data_for_plot_wdrl
                },
                "cpu": {
                    # "desc": "Multi-core CPU usage vs. time",
                    "time": t_cpu[0],
                    "value": cpus_avg[0]
                }
            }
        }
        new_utils.pushOutput(json_req)

    time.sleep(5)  #
    json_req = {
        "statistics": {
            "regularValue": num_reg,
            "anomalyValue": num_ano,
            "results": web_results,
            "tutc": t_utc,
        }
    }
    new_utils.pushOutput(json_req)


# java_defense("E:/project870/20230901/20230901.0000.txt")
