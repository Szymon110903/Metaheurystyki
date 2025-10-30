import os

def read_data_from_file(filename):
    file_path = os.path.join("data", filename)
    data = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip() and not line.startswith('#'):
                    values = line.strip().split()
                    if len(values) == 3:
                        id_num = int(values[0])
                        x = float(values[1])
                        y = float(values[2])
                        data.append((id_num, x, y))
                        # print(f"Read data - ID: {id_num}, X: {x}, Y: {y}")
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
    except Exception as e:
        print(f"Error reading file: {str(e)}")
    
    return data

