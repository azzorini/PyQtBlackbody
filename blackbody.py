import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

from PyQt5 import QtWidgets, uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from scipy.constants import h, c, k, Wien
import numpy as np

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()

        # Configuramos la UI
        uic.loadUi("blackbody.ui", self)
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.plotGraph(self.SliderTemp.value())
        self.VLayout.insertWidget(0, self.canvas)

        self.stars_dict = {"Betelgeuse": 3300, "Sol": 5778, "Rigel": 11500}
        self.load_stars("stars.txt")

        self.starsAction = {}
        for star in self.stars_dict:
            newStarAction = QtWidgets.QAction(self)
            newStarAction.setText(star)
            newStarAction.setObjectName(f"actionStar{star.replace(' ', '')}")
            self.menuEstrellas.addAction(newStarAction)
            self.starsAction[star] = newStarAction

        # Conexiones
        self.actionCerrar.triggered.connect(self.close)
        self.actionInformacion.triggered.connect(self.showAbout)

        self.SliderTemp.valueChanged[int].connect(self.changeTemp)

        for (star, temp) in self.stars_dict.items():
            self.starsAction[star].triggered.connect(lambda state, x=temp: self.changeTemp(x))

        # Mostramos
        self.show()

    def load_stars(self, filename):
        try:
            f = open(filename, "r")
        except FileNotFoundError:
            return

        self.stars_dict = {}
        line = f.readline()

        while line != "":
            star, temp = line.split(",")
            self.stars_dict[star] = int(temp)
            line = f.readline()

        f.close()

    def showAbout(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Sobre el programa")
        msg.setText("Este programa ha sido creado por David Ortiz del Campo usando PyQt5")
        msg.setIcon(QtWidgets.QMessageBox.Information)

        x = msg.exec_()

    def blackbody_I(self, landa_nm, T):
        landa = landa_nm*1e-9
        return 2*h*c**2/landa**5/(np.exp(h*c/landa/k/T) - 1)

    # Aproximación muy cutre que se podría mejorar bastante
    def blackbody_rgb_string(self, T):
        colors = np.array([self.blackbody_I(660, T), self.blackbody_I(560, T), self.blackbody_I(500, T)])
        colors *= 255/max(colors)

        # Convertimos el resultado a string
        s = ""
        for v in colors:
            s += hex(int(v))[2:]
        return s

    def rect(self, x,y,w,h,c):
        polygon = plt.Rectangle((x,y),w,h,color=c)
        self.canvas.axes.add_patch(polygon)

    def rainbow_fill(self, X, Y, cmap=plt.get_cmap("gist_rainbow")):
        dx = X[1]-X[0]
        N  = float(X.size)

        for n, (x,y) in enumerate(zip(X,Y)):
            color = cmap(1-n/N)
            self.rect(x, 0, dx, y, color)

    def plotGraph(self, T):
        landa_max = Wien/T*1e9
        Dlanda = 1010
        landa = np.linspace(10, landa_max + Dlanda, 1000)
        landa_vis = np.linspace(380, 750, 100)

        I_landa = self.blackbody_I(landa, T)*1e-12
        I_landa_vis = self.blackbody_I(landa_vis, T)*1e-12
        self.canvas.axes.set_xlim(landa[0], landa[-1])
        self.canvas.axes.set(xlabel="Longitud de onda (nm)", ylabel="Intensidad por longitud de onda (10¹² W/m³)", title=f"Longitud de onda del máximo a {landa_max:.0f} nm")
        self.canvas.axes.plot(landa_vis, I_landa_vis, linewidth=2, color="black")
        self.rainbow_fill(landa_vis, I_landa_vis)
        self.canvas.axes.plot(landa, I_landa, linewidth=2, color="black")
    
    def changeTemp(self, T):
        if T != self.SliderTemp.value():
            self.SliderTemp.setValue(T)

        self.LabelTemp.setText(f"{T} K")
        self.canvas.axes.cla()
        self.plotGraph(T)
        self.canvas.draw()

        self.labelColor.setStyleSheet(f"height: 160px; width:  160px; background-color: #{self.blackbody_rgb_string(T)}; border-radius: 80px;")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Ui()
    sys.exit(app.exec_())
