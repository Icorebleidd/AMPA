from PyQt5 import QtWidgets
import sys
import math
import matplotlib.pyplot as plt

def calculate_airmass(hour_angle_rad, declination_rad, latitude_rad):
    cos_z = (math.sin(declination_rad) * math.sin(latitude_rad)) + (math.cos(declination_rad) * math.cos(latitude_rad) * math.cos(hour_angle_rad))
    z = math.acos(cos_z)
    return 1 / math.cos(z)

def parse_angle(angle_str):
    try:
        parts = angle_str.replace('°', ' ').replace("'", ' ').replace('"', ' ').split()
        return math.radians(float(parts[0]) + float(parts[1]) / 60 + float(parts[2]) / 3600)
    except:
        return None

class AirMassApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Air Mass Calculator")
        self.setGeometry(100, 100, 600, 400)
        
        layout = QtWidgets.QVBoxLayout()
        
        self.hour_angle_input = QtWidgets.QLineEdit()
        self.hour_angle_input.setPlaceholderText("Hour Angles")
        layout.addWidget(self.hour_angle_input)
        
        self.declination_input = QtWidgets.QLineEdit()
        self.declination_input.setPlaceholderText("Declination")
        layout.addWidget(self.declination_input)
        
        self.latitude_input = QtWidgets.QLineEdit()
        self.latitude_input.setPlaceholderText("Latitude")
        layout.addWidget(self.latitude_input)
        
        self.calc_button = QtWidgets.QPushButton("Calculate")
        self.calc_button.clicked.connect(self.calculate)
        layout.addWidget(self.calc_button)
        
        self.export_button = QtWidgets.QPushButton("Export Table")
        self.export_button.clicked.connect(self.export_table)
        layout.addWidget(self.export_button)
        
        self.table = QtWidgets.QTableWidget()
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def calculate(self):
        try:
            hour_angles = self.hour_angle_input.text().split(',')
            declinations = self.declination_input.text().split(',')
            latitude = parse_angle(self.latitude_input.text())
            
            if latitude is None:
                QtWidgets.QMessageBox.critical(self, "Error", "Invalid latitude format!")
                return
            
            hour_angles_rad = []
            hour_labels = []
            for ha in hour_angles:
                h, m, s = map(float, ha.replace('h', ' ').replace('m', ' ').replace('s', ' ').split())
                total_hours = h + m / 60 + s / 3600
                hour_angles_rad.append(math.radians(total_hours * 15))
                hour_labels.append(f"{total_hours:.1f}h")
            
            declinations_rad = [parse_angle(d) for d in declinations]
            if None in declinations_rad:
                QtWidgets.QMessageBox.critical(self, "Error", "Invalid declination format!")
                return
            declination_labels = [d.strip() for d in declinations]
            
            air_mass_values = [[calculate_airmass(ha, dec, latitude) for ha in hour_angles_rad] for dec in declinations_rad]
            
            self.table.setRowCount(len(declinations))
            self.table.setColumnCount(len(hour_angles))
            self.table.setHorizontalHeaderLabels(hour_labels)
            self.table.setVerticalHeaderLabels(declination_labels)
            
            for i, row in enumerate(air_mass_values):
                for j, value in enumerate(row):
                    self.table.setItem(i, j, QtWidgets.QTableWidgetItem(f"{round(value, 2)}"))
        
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")
    
    def export_table(self):
        try:
            if not hasattr(self, 'table') or self.table.rowCount() == 0:
                QtWidgets.QMessageBox.critical(self, "Error", "No data available. Calculate first!")
                return
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.axis('tight')
            ax.axis('off')
            
            table_data = [[self.table.item(i, j).text() for j in range(self.table.columnCount())] for i in range(self.table.rowCount())]
            col_labels = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
            row_labels = [self.table.verticalHeaderItem(i).text() for i in range(self.table.rowCount())]
            
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
    window = AirMassApp()
    window.show()
    sys.exit(app.exec_())

# TODO: If i put the same latitude in the declination input, the program crashes causing a division by zero. Fix this.
# TODO: Accept input with and without symbols, same as in SkyRefrax. Fix this.
