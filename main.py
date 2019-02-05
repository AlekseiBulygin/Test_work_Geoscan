import sys
from PyQt4.QtGui import *


class MainWindow(QMainWindow):
    def __init__(self, args):
        QMainWindow.__init__(self)
        self.towers = args
        self.setupUi()

        print(args)

    def setupUi(self):
        self.setGeometry(350, 200, 420, 430)
        self.setWindowTitle('Towers')
        self.show()

    def paintEvent(self, *args, **kwargs):
        qp = QPainter()
        qp.begin(self)
        self.build_towers(qp)
        qp.end()

    def build_towers(self, qp):
        color = QColor(0, 0, 0)
        qp.setPen(color)

        for j in range(len(self.towers)):
            for i in range(self.towers[j]):
                qp.setBrush(QColor(153, 153, 102))
                qp.drawRect(10 + j*40, 380 - 40*i, 40, 40)

    def pour_water(self):
        pass


def main(args):
    app = QApplication(sys.argv)
    window = MainWindow(args)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    args = []
    try:
        assert len(sys.argv) - 1 < 11
        for param in sys.argv[1:]:
            if int(param) > 10:
                raise RuntimeError
            else:
                args.append(int(param))
    except AssertionError:
        print("Количество башен не должно превышать 10.")
    except RuntimeError:
        print("Некорректный ввод. Высота башни не более 10.")
    except ValueError:
        print("Некорректный ввод. Введите целые числовые значения.")
    else:
        main(args)
