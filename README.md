# huaweicloud-hcso-sdr-formatter
This repository contains a Python script to format the resources utilization CSV files generated from the SDR service on Huawei Cloud HCSO.

## What kind of formatting is performed?
The aforementioned script will automatically extract the raw, compressed tar file stored on the OBS SDR bucket and then recursively extract the compressed zip files on each HCSO service directory. Besides that, the script will also parse through all the CSV files and compile the timestamps into a daily CSV file. e.g.: For the ECS service, in the raw SDR file there will be 24 CSV files, each one corresponding to a given timestamp. In the formatted CSV file, all of the timestamped CSV files will be compiled into a single, daily CSV file. Furthermore, all of the information in the CSV file has been segregated into multiple columns instead of a single column with data separate by a pipe, and a header containing the information present in each column has also been added.

## How to run the script
In order to run the script, simply type on the terminal <code>python3 script.py <name_of_the_tar_gz_file></code>, as depicted below:
<br>
<img src="https://github.com/user-attachments/assets/61a6740b-8b15-48d2-a46d-e8f3ae0b0e1a" alt='Image'>
