# NetAIOasis
Advanced version of CyberDefense with real-time training, CI/CD


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

