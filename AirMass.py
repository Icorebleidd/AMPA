import sys
import math
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets

def calculate_airmass(hour_angle_rad, declination_rad, latitude_rad):
    cos_z = (math.sin(declination_rad) * math.sin(latitude_rad)) + (math.cos(declination_rad) * math.cos(latitude_rad) * math.cos(hour_angle_rad))
    z = math.acos(cos_z)
    return 1 / math.cos(z)

def parse_angle(angle_str):
    try:
        parts = angle_str.replace('h', ' ').replace('m', ' ').replace('s', ' ').split()
        total_hours = float(parts[0]) + float(parts[1]) / 60 + float(parts[2]) / 3600
        return math.radians(total_hours * 15), total_hours
    except:
        return None, None

def parse_declination(dec_str):
    try:
        parts = dec_str.replace('°', ' ').replace("'", ' ').replace('"', ' ').split()
        dec_degree = float(parts[0]) + float(parts[1]) / 60 + float(parts[2]) / 3600
        return math.radians(dec_degree), dec_degree
    except:
        return None, None

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Air Mass Calculator")
        self.setGeometry(100, 100, 600, 400)
        
        layout = QtWidgets.QVBoxLayout()
        
        self.hour_angles_input = QtWidgets.QLineEdit()
        self.hour_angles_input.setPlaceholderText("Hour Angles")
        layout.addWidget(self.hour_angles_input)
        
        self.declination_input = QtWidgets.QLineEdit()
        self.declination_input.setPlaceholderText("Declination")
        layout.addWidget(self.declination_input)
        
        self.latitude_input = QtWidgets.QLineEdit()
        self.latitude_input.setPlaceholderText("Latitude")
        layout.addWidget(self.latitude_input)
        
        self.calculate_button = QtWidgets.QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_button)
        
        self.export_button = QtWidgets.QPushButton("Export Table")
        self.export_button.clicked.connect(self.export_table)
        layout.addWidget(self.export_button)
        
        self.table = QtWidgets.QTableWidget()
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def calculate(self):
        try:
            hour_angle_strings = self.hour_angles_input.text().split(',')
            declination_strings = self.declination_input.text().split(',')
            latitude_string = self.latitude_input.text()
            
            self.hour_angles, self.hour_angle_hours = zip(*[parse_angle(ha) for ha in hour_angle_strings])
            self.declinations, self.declination_degrees = zip(*[parse_declination(dec) for dec in declination_strings])
            
            if None in self.hour_angles or None in self.declinations:
                QtWidgets.QMessageBox.critical(self, "Error", "Invalid format for angles!")
                return
            
            lat_radians, _ = parse_declination(latitude_string)
            
            self.nu_matrix = [[calculate_airmass(ha, dec, lat_radians) for ha in self.hour_angles] for dec in self.declinations]
            
            self.table.setRowCount(len(self.declinations))
            self.table.setColumnCount(len(self.hour_angles))
            self.table.setHorizontalHeaderLabels([f"{h:.1f}h" for h in self.hour_angle_hours])
            self.table.setVerticalHeaderLabels([f"{d:.1f}°" for d in self.declination_degrees])
            
            for i, row in enumerate(self.nu_matrix):
                for j, value in enumerate(row):
                    self.table.setItem(i, j, QtWidgets.QTableWidgetItem(f"{round(value, 2)}"))
        
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")
    
    def export_table(self):
        try:
            if not hasattr(self, 'nu_matrix'):
                QtWidgets.QMessageBox.critical(self, "Error", "No data available. Calculate first!")
                return
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.axis('tight')
            ax.axis('off')
            
            table_data = [[round(value, 2) for value in row] for row in self.nu_matrix]
            col_labels = [f"{h:.1f}h" for h in self.hour_angle_hours]
            row_labels = [f"{d:.1f}°" for d in self.declination_degrees]
            
            table = ax.table(cellText=table_data, colLabels=col_labels, rowLabels=row_labels, cellLoc='center', loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1.2, 1.2)
            
            options = QtWidgets.QFileDialog.Options()
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Table", "", "PNG Files (*.png);;PDF Files (*.pdf)", options=options)
            
            if file_path:
                plt.savefig(file_path, bbox_inches='tight')
                QtWidgets.QMessageBox.information(self, "Success", f"Table saved to {file_path}")
            plt.close()
        
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
