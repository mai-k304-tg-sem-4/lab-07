import numpy as np
import sys


class Graph:
    def __init__(self, file_path, file_type):
        # Конструктор класса Graph
        # Инициализирует объект графа с указанным путем к файлу и типом файла
        self.file_path = file_path
        self.file_type = file_type
        self.graph = self.load_graph()

    def load_graph(self):
        # Метод загрузки графа в зависимости от типа файла
        if self.file_type == "-e":
            return self.load_list_of_edges()  # Загрузка графа из списка ребер
        elif self.file_type == "-m":
            return self.load_adjacency_matrix()  # Загрузка графа из матрицы смежности
        elif self.file_type == "-l":
            return self.load_adjacency_list()  # Загрузка графа из списка смежности
        else:
            raise ValueError("Invalid file type")  # Вызов исключения, если тип файла некорректен

    def load_adjacency_list(self):
        # Метод загрузки графа из файла в формате списка смежности
        with open(self.file_path, 'r') as file:
            lines = file.readlines()  # Чтение всех строк из файла
        num_vertices = len(lines)  # Количество вершин в графе равно количеству строк
        matrix = np.zeros((num_vertices, num_vertices))  # Создание матрицы с нулевыми значениями
        matrix[:] = np.inf  # Установка всех элементов матрицы в бесконечность
        for i, line in enumerate(lines):
            neighbors = line.strip().split()  # Разделение строки на соседей вершины
            for neighbor in neighbors:
                matrix[i, int(neighbor) - 1] = 1  # Установка значения 1 для соответствующих соседних вершин
        return matrix  # Возвращение матрицы смежности

    def load_adjacency_matrix(self):
        # Метод загрузки графа из файла в формате матрицы смежности
        with open(self.file_path, 'r') as file:
            lines = file.readlines()  # Чтение всех строк из файла
        num_vertices = len(lines)  # Количество вершин в графе равно количеству строк
        matrix = np.zeros((num_vertices, num_vertices))  # Создание матрицы с нулевыми значениями
        matrix[:] = np.inf  # Установка всех элементов матрицы в бесконечность
        for i, line in enumerate(lines):
            row = line.strip().split()  # Разделение строки на элементы строки
            for j, value in enumerate(row):
                matrix[i, j] = int(value) if int(value) != 0 else np.inf  # Заполнение матрицы значениями из файла
        return matrix  # Возвращение матрицы смежности

    def adjacency_matrix(self):
        return self.graph  # Возвращение матрицы смежности графа

    def load_list_of_edges(self):
        # Метод загрузки графа из файла в формате списка ребер
        with open(self.file_path, 'r') as file:
            lines = file.readlines()  # Чтение всех строк из файла
        num_vertices = 0  # Инициализация количества вершин
        edges = []  # Инициализация списка ребер
        for line in lines:
            values = line.strip().split()  # Разделение строки на значения
            if len(values) == 2:
                vertex1, vertex2 = values  # Получение вершин ребра
                weight = 1  # Установка веса ребра по умолчанию
            else:
                vertex1, vertex2, weight = values  # Получение вершин и веса ребра
            edges.append((vertex1, vertex2, int(weight)))  # Добавление ребра в список ребер
            num_vertices = max(num_vertices, int(vertex1), int(vertex2))  # Обновление количества вершин
        matrix = np.zeros((num_vertices, num_vertices))  # Создание матрицы с нулевыми значениями
        matrix[:] = np.inf  # Установка всех элементов матрицы в бесконечность
        for edge in edges:
            vertex1, vertex2, weight = edge  # Получение вершин и веса ребра
            matrix[int(vertex1) - 1, int(vertex2) - 1] = weight  # Заполнение матрицы значениями из списка ребер
            matrix[int(vertex2) - 1, int(
                vertex1) - 1] = weight  # Заполнение матрицы значениями из списка ребер (для неориентированного графа)
        return matrix  # Возвращение матрицы смежности

    def list_of_edges(self, v):
        edges = []  # Инициализация списка ребер
        it = np.nditer(self.graph, flags=['multi_index'])  # Итератор по элементам матрицы
        while not it.finished:
            if it[0] != np.inf:
                i, j = it.multi_index  # Получение индексов элемента
                edges.append((i + 1, j + 1, it[0]))  # Добавление ребра в список ребер
            it.iternext()
        return edges  # Возвращение списка ребер

    def is_directed(self):
        return self.graph.transpose() == self.graph  # Проверка, является ли граф ориентированным

    def johnson(self):
        # Алгоритм Джонсона
        num_vertices = self.graph.shape[0]
        extended_graph = self.extend_graph()
        distance_matrix = np.zeros((num_vertices, num_vertices))
        for source in range(num_vertices):
            shortest_distances, _ = self.bellman_ford(extended_graph, source)
            for target in range(num_vertices):
                distance_matrix[source, target] = shortest_distances[target]
        return distance_matrix

    def extend_graph(self):
        # Расширение графа для алгоритма Джонсона
        num_vertices = self.graph.shape[0]
        extended_graph = np.zeros((num_vertices + 1, num_vertices + 1))
        extended_graph[:-1, :-1] = self.graph
        extended_graph[:-1, -1] = np.inf
        return extended_graph

    def bellman_ford(self, graph, source):
        # Алгоритм Беллмана-Форда
        num_vertices = graph.shape[0]
        distances = np.full(num_vertices, np.inf)
        distances[source] = 0
        for _ in range(num_vertices - 1):
            for u in range(num_vertices):
                for v in range(num_vertices):
                    if graph[u, v] != np.inf:
                        distances[v] = min(distances[v], distances[u] + graph[u, v])
        for u in range(num_vertices):
            for v in range(num_vertices):
                if graph[u, v] != np.inf and distances[u] + graph[u, v] < distances[v]:
                    raise ValueError("Graph contains a negative cycle.")
        return distances, None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Введите ключ параметра:")
    print("-e: list_of edges, \n-m: matrix, \n-l: list_of_adjacency")

    key = input()
    if key not in ['-m', '-e', '-l']:
        print('Неверный тип ключа!')
        sys.exit()
    print("Введите название файла (в текущем каталоге):")
    file = input()
    print('\n')

    g = Graph(file, key)

    adj_matrix = g.adjacency_matrix()
    np.set_printoptions(threshold=np.inf)
    np.set_printoptions(edgeitems=8, suppress=True)

    adj_matrix = g.adjacency_matrix()

    try:
        distance_matrix = g.johnson()
        print("Shortest paths lengths:")
        for source in range(1, distance_matrix.shape[0] + 1):
            for target in range(1, distance_matrix.shape[1] + 1):
                if source != target:
                    distance = distance_matrix[source - 1, target - 1]
                    if distance != np.inf:
                        print(f"{source} - {target}: {int(distance)}")
    except ValueError as e:
        print(e)

    # Запись результатов в файл
    with open("output.txt", 'w') as file:
        file.write("Adjacency matrix:\n")
        for row in adj_matrix:
            row_str = ' '.join(map(str, row))
            file.write(row_str + '\n')
        file.write('\n')

    print("\nРезультаты записаны в файл output.txt")