This project was upgraded under the direction of Professor [Zhida Li](https://zhidali.me/), based on Professor Li's [CyberDefense](https://github.com/zhida-li/cyberDefense) project. Professor Li's project includes complete real-time analysis, prediction, machine learning and other technologies on the Python side. In addition, the Web layer uses Websocket for real-time chart and data presentation.
Under the guidance of Professor Li, the front and back ends of the project are not separated, and there are problems such as limited scalability and difficult maintenance. The team reorganized the business and technology, adopted the current stable and reliable technical architecture, and designed a three-layer technical architecture. Such a design helps to attract more people from different technical backgrounds and provides flexibility and scalability for the development of the system.

The NCS870-Fall2023-Team1 project consists of three sub-projects, which are: 1. The front-end framework is based on VUE, 2. The application server is based on Spring Boot, 3. Background analysis is based on Python.

[NCS870-Fall2023-Team1-Vue](https://github.com/Caixianwang/NCS870-Fall2023-Team1-Vue)

[NCS870-Fall2023-Team1-Spring](https://github.com/Caixianwang/NCS870-Fall2023-Team1-Spring)

[NCS870-Fall2023-Team1-Python](https://github.com/Caixianwang/NCS870-Fall2023-Team1-Python)


## Structure:

``` 
NetAIOasis
├── LICENSE
├── README.md
├── app.py
├── app_offline.py
├── app_realtime.py
├── config.py
├── requirements.txt
├── new_app.py
├── database
│   ├── database.py
│   └── db_files
└── src
    ├── __init__.py
    ├── check_versions.py
    ├── dataDownload.py
    ├── data_partition.py
    ├── data_process.py
    ├── featureExtraction.py
    ├── input_exp.txt
    ├── label_generation.py
    ├── progress.py
    ├── progress_bar.py
    ├── subprocess_cmd.py
    ├── time_tracker.py
    ├── CSharp_Tool_BGP
    ├── STAT
    ├── VFBLS_v110
    ├── data_historical
    ├── data_ripe
    ├── data_routeviews
    ├── data_split
    └── ver870
        ├── __init__.py
        ├── new_down_data.py 
        ├── new_real_time.py
        ├── new_topology.py
        └── new_utils.py

```

```bash
pip install -r requirements.txt
```

Running on:

``` bash
python3 new_app.py
```

