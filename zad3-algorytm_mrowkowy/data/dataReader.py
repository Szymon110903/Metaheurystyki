import os

def read_data_from_file(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    file_path = os.path.join(current_dir, filename)
    
    data = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip() and not line.startswith('#'):
                    values = line.strip().split()
                    if len(values) == 3:
                        try:
                            id_num = int(values[0])
                            x = float(values[1])
                            y = float(values[2])
                            data.append((id_num, x, y))
                        except ValueError:
                            continue 
                            
    except FileNotFoundError:
        print(f"[BŁĄD] Nie znaleziono pliku: {file_path}")
        return []
    except Exception as e:
        print(f"[BŁĄD] Problem z odczytem pliku: {str(e)}")
        return []
    
    return data