import math
import matplotlib.pyplot as plt

def calcoloZenitale(hAngles, declination, latitude):
    cos_z = (math.sin(declination) * math.sin(latitude)) + (math.cos(declination) * math.cos(latitude) * math.cos(hAngles))
    z = math.acos(cos_z)
    sec_z = 1 / math.cos(z)
    return sec_z

def main():
    angoli_lst = input("Hour angles: ")
    angoli = angoli_lst.split(",")
    angoli_resolved = []
    angoli_hours = []
    for ang_non_res in angoli:
        hour = ang_non_res.index("h")
        minute = ang_non_res.index("m")
        ang_act_hour = float(ang_non_res[0:hour])
        ang_act_minuto = float(ang_non_res[hour + 1 : minute]) / 60
        ang_act_secondo = float(ang_non_res[minute + 1 : -1]) / 3600
        total_hour_angle = (ang_act_hour + ang_act_minuto + ang_act_secondo) * 15
        angolo_radianti = math.radians(total_hour_angle)
        angoli_resolved.append(angolo_radianti)
        angoli_hours.append(ang_act_hour + ang_act_minuto + ang_act_secondo)

    declination_lst = input("Declination range: ")
    declination = declination_lst.split(",")
    declination_resolved = []
    declination_degrees = []
    for dec_non_res in declination:
        grado = dec_non_res.index("°")
        minuto = dec_non_res.index("'")
        dec_act_grado = float(dec_non_res[0:grado])
        dec_act_minuto = float(dec_non_res[grado + 1 : minuto]) / 60
        dec_act_secondo = float(dec_non_res[minuto + 1 : -1]) / 3600
        declination_gradi = dec_act_grado + dec_act_minuto + dec_act_secondo
        declination_radianti = math.radians(declination_gradi)
        declination_resolved.append(declination_radianti)
        declination_degrees.append(declination_gradi)

    latitude_lst = input("Latitude of the place: ")
    grado = latitude_lst.index("°")
    minuto = latitude_lst.index("'")
    lat_act_grado = float(latitude_lst[0:grado])
    lat_act_minuto = float(latitude_lst[grado + 1 : minuto]) / 60
    lat_act_secondo = float(latitude_lst[minuto + 1 : -1]) / 3600
    lat_gradi = lat_act_grado + lat_act_minuto + lat_act_secondo
    lat_radianti = math.radians(lat_gradi)

    z_values = [[calcoloZenitale(ang, dec, lat_radianti) for ang in angoli_resolved] for dec in declination_resolved]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('tight')
    ax.axis('off')
    col_labels = [f"{h:.1f}h" for h in angoli_hours]
    row_labels = [f"{d:.1f}°" for d in declination_degrees]
    table_data = [[round(value, 2) for value in row] for row in z_values]
    table = ax.table(cellText=table_data, colLabels=col_labels, rowLabels=row_labels, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(angoli_hours))))
    ax.set_title("Parallactic Angle Table", fontsize=14, pad=20)
    plt.show()

if __name__ == "__main__":
    main()
