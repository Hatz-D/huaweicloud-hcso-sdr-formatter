import csv
import os
import zipfile
import tarfile
import sys

# Funciton to decompress all of the zip files 
def decompress_zip_files(path):
    # Walks through all the files and directories of given path
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.zip'):
                zip_file_path = os.path.join(root, file)
                try:
                    # Calls the function to decompress a single file
                    decompress_zip(zip_file_path, root)
                except Exception as e:
                    print(f"Erro ao descompactar {zip_file_path}: {e}")


# Funciton to decompress a single zip file
def decompress_zip(zip_file_path, destination_folder):
    # Checks whether the absolute path is bigger than 100 characters to avoid decompression errors
    if(len(zip_file_path) > 100):
        os.rename(zip_file_path, os.path.join(destination_folder, 'a.zip'))
        zip_file_path = os.path.join(destination_folder, 'a.zip')

    # Extracts the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(destination_folder)

        # Upon decompression, checks for other compressed files recursevely 
        for file_name in zip_ref.namelist():
            decompressed_file_path = os.path.join(destination_folder, file_name)
            if file_name.endswith('.zip'):
                # Recursevely decompresses zip files
                decompress_zip(decompressed_file_path, destination_folder)


# Function to format the resources usage CSV files into an easier to read CSV file 
def csv_formatter(file, directory):
    array = []
    final = []
    dict = {}

    with open(file, newline='') as file:
        csvfile = csv.reader(file)

        # Parses the CSV file and filters the header and tail. Also splits the data into several columns 
        for line in csvfile:
            if(line[0][0:2] == '10' or line[0][0:2] == '90'):
                array.append(line.pop().split('|'))

            else:
                array.append(line.pop().split(' | '))


    # Appends the filtered data to a new CSV file called 'output.csv'
    with open(os.path.join(directory, 'output.csv'), 'a', newline='') as csvoutput:
        fieldnames = ['RecordType', 'TimeStamp', 'UserID', 'RegionCode', 'AZCode', 'CloudServiceType', 'ResourceType', 'ResourceSpec', 'ResourceID', 'CSBParams', 'BeginTime', 'EndTime', 'FactorName', 'FactorValue(seconds)', 'ExtendedParams', 'Tags', 'EnterpriseProjectID', 'ChargeMode']
        final.append(fieldnames)

        for line in array:
            if len(line) <= 4:
                continue

            else:
                final.append(line)

                if(dict.get((line[5], line[7])) is None):
                    dict.update({(line[5], line[7]): (line[1], 0)})


                qnt = dict.get((line[5], line[7]))[1]    
                dict.update({(line[5], line[7]): (line[1], qnt+1)})


        writer = csv.writer(csvoutput)
        writer.writerows(final)


    # Appends the saved data to a new CSV file called 'report' in order to generate the report
    with open(os.path.join(directory, 'report.csv'), 'a', newline='') as report:
        fieldnames = ['ResourceType', 'Flavor', 'TimeStamp', 'Amount']
        writer = csv.writer(report)
        writer.writerow(fieldnames)
        
        for key, value in dict.items():
            writer.writerow([key[0], key[1], value[0], value[1]])


# Function to parse through all CSV files and format them all
def format_all_csv(destination_path):
    # Recursevely walks through all directories, subdirectories and files
    for root, _, files in os.walk(destination_path):
        for file in files:
            if file.endswith('.csv'):
                csv_file_path = os.path.join(root, file)
                csv_formatter(csv_file_path, root)


# Function to delete the temporary CSV and ZIP files 
def delete_temporary_files(destination_path):
    # Recursevely walks through all directories, subdirectories and files
    for root, _, files in os.walk(destination_path):
        for file in files:
            if file.startswith('HWS') or file.endswith('.zip'):
                file_path = os.path.join(root, file)
                os.remove(file_path) 


# Function to delete the duplicate headers of the 'output' CSV file generated 
def remove_duplicate_headers(destination_path):
    # Recursevely walks through all directories, subdirectories and files
    for root, _, files in os.walk(destination_path):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                lines = []
                    
                # Opens the CSV file and saves all the data, filtering duplicate headers
                with open(file_path, mode='r', newline='') as file:
                    csvfile = csv.reader(file)
                    
                    counter = 0

                    for line in csvfile:
                        if(counter == 0 or (counter != 0 and (line[0] != 'RecordType' and line[0] != 'ResourceType'))):
                            lines.append(line)
                        
                        counter += 1

                # Opens the CSV files and writes the data saved to the 'lines' array
                with open(file_path, mode='w', newline='') as file:
                    csvfile = csv.writer(file)
                    csvfile.writerows(lines)


# Main function to call the auxiliary functions
def main():
    destination_path = './SDR_Formatted'
    file_name = sys.argv[1]
    
    file = tarfile.open(file_name)
    file.extractall(destination_path)
    file.close()

    decompress_zip_files(destination_path)

    print("Decompression succeeded.")

    format_all_csv(destination_path)

    print("CSV files formatted.")

    delete_temporary_files(destination_path)

    print("Temporary files deleted.")

    remove_duplicate_headers(destination_path)

    print("Exiting script...")


main()
