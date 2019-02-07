import sys
from PyQt4.QtGui import QApplication, QMainWindow, QPainter, QColor
from PyQt4.QtCore import SIGNAL

from design import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, args):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.args = []

        if len(args) - 1 > 0:
            self.lineEdit.setText(' '.join(str(i) for i in args[1:]))
        self.connect(self.pushButton, SIGNAL('clicked()'), self.button_event)

    def button_event(self):
        self.label_2.clear()
        data = self.lineEdit.text().split()
        result_check = check_args(data)
        if result_check != True:
            self.label_2.setText(result_check)
        else:
            args = []
            for i in data:
                args.append(int(i))

            self.window = Towers(args)
            self.window.show()


class Towers(QMainWindow):
    def __init__(self, args):
        QMainWindow.__init__(self)
        self.towers = args
        self.setupUi()
        self.cups = []

    def setupUi(self):
        self.setGeometry(350, 200, 420, 430)
        self.setWindowTitle('Towers')

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

    def find_border(self, cups):
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

                if right_side >= left_side and right_side != 0:
                    tup = (min(left_side, right_side), left_index, right_index, bottom)
                    cups.append(tup)
                    left_side, right_side = right_side, 0
                    left_index, right_index = right_index, 0
                    bottom = 10
                elif right_side < left_side and right_side != 0:
                    tup = (min(left_side, right_side), left_index, right_index, bottom)
                    cups.append(tup)
                    bottom = right_side
                    right_side = 0
                    right_index = 0

            elif self.towers[i] == 0:
                if left_side != 0 and right_side != 0 and bottom != 10:
                    tup = (min(left_side, right_side), left_index, right_index, bottom)
                    cups.append(tup)
                left_side = 0
                left_index = 0
                right_side = 0
                right_index = 0
                bottom = 10

    def pour_water(self, qp):
        color = QColor(51, 204, 255)
        qp.setPen(color)
        cups = []
        self.find_border(cups)
        for result in cups:
            deep = result[0]
            start = result[1]
            finish = result[2]
            for j in range(len(self.towers))[start+1:finish+1]:
                for i in range(deep)[self.towers[j]:]:
                    qp.setBrush(QColor(51, 204, 255))
                    qp.drawRect(10 + j*40, 380 - 40*i, 40, 40)


def check_args(args):
    try:
        assert len(args) < 11
        for param in args:
            if int(param) > 10 or int(param) < 0:
                raise RuntimeError
    except AssertionError:
        return "Количество башен не должно превышать 10."
    except RuntimeError:
        return "Некорректный ввод.\nВысота башни от 0 до 10."
    except ValueError:
        return "Некорректный ввод.\nВведите целые числовые значения."
    else:
        return True


def main():
    app = QApplication(sys.argv)
    window = MainWindow(sys.argv)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
