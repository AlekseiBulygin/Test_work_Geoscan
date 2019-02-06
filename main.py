import sys
from PyQt4.QtGui import *


class MainWindow(QMainWindow):
    def __init__(self, args):
        QMainWindow.__init__(self)
        self.towers = args
        self.setupUi()
        self.cups = []
        print(args)

    def setupUi(self):
        self.setGeometry(350, 200, 420, 430)
        self.setWindowTitle('Towers')
        self.show()

    def paintEvent(self, *args, **kwargs):
        qp = QPainter()
        qp.begin(self)
        self.build_towers(qp)
        self.pour_water(qp)
        qp.end()

    def build_towers(self, qp):
        color = QColor(0, 0, 0)
        qp.setPen(color)

        for j in range(len(self.towers)):
            for i in range(self.towers[j]):
                qp.setBrush(QColor(153, 153, 102))
                qp.drawRect(10 + j*40, 380 - 40*i, 40, 40)

    def find_border(self):
        left_side = 0
        left_index = 0
        right_side = 0
        right_index = 0
        bottom = 10

        for i in range(len(self.towers)):
            if self.towers[i] != 0:
                if self.towers[i] > 1 and self.towers[i] > left_side and bottom == 10:
                    left_side = self.towers[i]
                    left_index = i
                elif self.towers[i] < left_side and self.towers[i] < bottom:
                    bottom = self.towers[i]
                elif self.towers[i] > bottom and self.towers[i] >= right_side:
                    right_side = self.towers[i]
                    right_index = i

                if left_side != 0 and right_side != 0 and bottom != 10 and right_side >= left_side:
                    tup = (min(left_side, right_side), left_index, right_index, bottom)
                    if tup not in self.cups:
                        self.cups.append(tup)
                        left_side, right_side = right_side, 0
                        left_index, right_index = right_index, 0
                        bottom = 10
            elif self.towers[i] == 0:
                if left_side != 0 and right_side != 0 and bottom != 10:
                    tup = (min(left_side, right_side), left_index, right_index, bottom)
                    if tup not in self.cups:
                        self.cups.append(tup)
                left_side = 0
                left_index = 0
                right_side = 0
                right_index = 0
                bottom = 10

        if left_side != 0 and right_side != 0 and bottom != 10:
            tup = (min(left_side, right_side), left_index, right_index, bottom)
            if tup not in self.cups:
                self.cups.append(tup)

    def pour_water(self, qp):
        cups = self.cups
        color = QColor(51, 204, 255)
        qp.setPen(color)
        self.find_border()
        print(cups)
        for result in cups:
            deep = result[0]
            start = result[1]
            finish = result[2]
            for j in range(len(self.towers))[start+1:finish+1]:
                for i in range(deep)[self.towers[j]:]:
                    qp.setBrush(QColor(51, 204, 255))
                    qp.drawRect(10 + j*40, 380 - 40*i, 40, 40)


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
