from bs4 import BeautifulSoup
import re

#Класс для точек
class Point:
    #Инициализация объекта
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.name} ({self.x}, {self.y})"
        
#Класс для прямых
class Line():
    #Инициализация объекта
    def __init__(self, name, point_a, point_b, k, b):
        self.name = name
        self.point_a = point_a
        self.point_b = point_b
        self.k = k
        self.b = b
    
    def __str__(self):
        return f"{self.name} = Прямая ({self.point_a}, {self.point_b}): y = {self.k}x + {self.b}"


#Рассчет интеграла
def linear_integral(a, c, k, b):
    return k / 2 * (a * a - c * c) + b * (a - c)

# Читаем файл в нужной кодировке
with open("input.txt", "r") as f:
    html = f.read()

# Создаем объект BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

#Создаем словарь для хранения точек
points_dict = dict()
#Создаем список для хранения прямых
lines_list = []

point1, point2 = "", ""

# Находим все теги "td" на странице и получаем из них нужную информацию
for tag in soup.find_all("td"):
    #Парсим координаты точки
    if tag.text.find(",") != -1 and tag.text.find("=") != -1 and tag.text.find("(") != -1:
        match = re.match(r"(\w+)\s*=\s*\(([-\d.]+),\s*([-\d.]+)\)", tag.text)
        if match:
            name = match.group(1)
            x = float(match.group(2))
            y = float(match.group(3))
            point = Point(name, x, y)
            #Добавляем точки в словарь
            points_dict[name] = point
    #Парсим точки, через которые проходит прямая        
    elif tag.text.find(",") != -1 and tag.text.find("(") != -1:
        match = re.match(r"Прямая\((\w+), (\w+)\)", tag.text)
        if match:
            point1, point2 = match.group(1), match.group(2)
        else:
            match = re.match(r"Line\((\w+), (\w+)\)", tag.text)
            if match:
                point1, point2 = match.group(1), match.group(2)
    #Парсим прямые
    elif tag.text.find("=") != -1:
        #Удаляем из строки все пробелы
        current_str = str(tag.text).replace(" ", "")
        #Если прямая перепендикулярна оси x, то добавляем нулевые коэффициенты
        if current_str.find("x=") != -1:
            name = current_str.split(":")[0]
            line = Line(name, point1, point2, 0, 0)
            #Добавляем прямую в список
            lines_list.append(line)
        elif current_str.find("y=") != -1:
            name = current_str.split(":")[0]
            #Если строка вида y = kx + b
            if current_str.find("x") != -1:
                k_pos_start = current_str.find("y=")+2
                k_pos_end = current_str.find("x")
                #Если перед x стоит минус и не стоит аргумента (-x)
                if current_str[k_pos_start:k_pos_end] == "-":
                    k=-1
                #Если перед x не стоит аргумента (x)
                elif len(current_str[k_pos_start:k_pos_end]) == 0:
                    k=1
                else:
                    k = float(current_str[k_pos_start:k_pos_end])
                if len(current_str) <= k_pos_end+1:
                    b = 0
                else:
                    b = float(current_str[k_pos_end+1:])
            #Если строка вида y = b
            else:
                k = 0
                k_pos_start = current_str.find("y=")+2
                b = float(current_str[k_pos_start:])
            line = Line(name, point1, point2, k, b)
            #Добавляем прямую в список
            lines_list.append(line)

#Переменная для подсчета площади
square = 0

#Делаем перебор всех прямых
for i in lines_list:
    #Получаем первую точку прямой
    a = points_dict[i.point_a]
    #Получаем сторую точку прямой
    b = points_dict[i.point_b]
    #Считаем интеграл
    res = linear_integral(b.x, a.x, i.k, i.b)
    print("Интеграл прямой", i.name, "равен", res)
    square += res

print("Площадь объекта = ", abs(square))