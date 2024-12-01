import os
import matplotlib.pyplot as plt

def read_dataset(file_path):

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Can't find dataset: '{file_path}'")

    points = []
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            parts = line.strip().split()
            if len(parts) != 2:
                print(f"Skipping line {line_num}: expected 2 values, got {len(parts)}")
                continue
            try:
                x, y = map(int, parts)
                points.append((x, y))
            except ValueError:
                print(f"Skipping line {line_num}: can't convert coordinates to int")
                continue
    return points

def jarvis_convex_hull(points):

    if len(points) < 3:
        raise ValueError("At least three points are required to compute the convex hull.")

    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - \
              (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # колінеарні
        return 1 if val > 0 else 2 # за годинниковою стрілкою чи проти

    hull = []

    # пошук найлівішої точки (з найменшою коорд. х)
    l = min(range(len(points)), key=lambda i: points[i][0])
    p = l
    # додаємо до оболонки ті точки, що утворюють поворот проти годинникової стрілки від поточної точки
    while True:
        hull.append(points[p])
        q = (p + 1) % len(points)
        for i in range(len(points)):
            if orientation(points[p], points[i], points[q]) == 2:
                q = i
        p = q
        if p == l:
            break

    return hull

def save_convex_hull(hull_points, file_path):

    with open(file_path, 'w') as file:
        for point in hull_points:
            file.write(f"{point[0]} {point[1]}\n")
    print(f"Convex hull dataset saved to '{file_path}'.")

def plot_points_and_hull(dataset_points, hull_points, canvas_width=960, canvas_height=540, output_file='result.png'):

    if not dataset_points:
        raise ValueError("Dataset points list is empty.")
    if not hull_points:
        raise ValueError("Convex hull points list is empty.")

    X_orig, Y_orig = zip(*dataset_points)
    X_hull, Y_hull = zip(*hull_points)

    plt.figure(figsize=(canvas_width/100, canvas_height/100), dpi=100)

    plt.scatter(X_orig, Y_orig, s=10, c='purple', label='Dataset points')

    X_hull_closed = list(X_hull) + [X_hull[0]]
    Y_hull_closed = list(Y_hull) + [Y_hull[0]]
    plt.plot(X_hull_closed, Y_hull_closed, c='blue', linewidth=2, label='Convex hull')

    all_X = X_orig + X_hull
    all_Y = Y_orig + Y_hull
    min_x, max_x = min(all_X), max(all_X)
    min_y, max_y = min(all_Y), max(all_Y)

    padding_x = (max_x - min_x) * 0.05 if max_x != min_x else 10
    padding_y = (max_y - min_y) * 0.05 if max_y != min_y else 10

    plt.xlim(min_x - padding_x, max_x + padding_x)
    plt.ylim(min_y - padding_y, max_y + padding_y)

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Dataset points and convex hull')

    plt.legend()
    plt.grid(True)

    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    print(f"Plot saved as '{output_file}'.")

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    dataset_file = os.path.join(current_dir, 'dataset.txt')
    convex_hull_file = os.path.join(current_dir, 'hull_dataset.txt')
    output_image = os.path.join(current_dir, 'result.png')

    try:
        
        dataset_points = read_dataset(dataset_file)
        print(f"Loaded {len(dataset_points)} points from '{dataset_file}'.")

        hull_points = jarvis_convex_hull(dataset_points)
        print(f"Convex hull consists of {len(hull_points)} points.")

        save_convex_hull(hull_points, convex_hull_file)

        plot_points_and_hull(dataset_points, hull_points, canvas_width=960, canvas_height=540, output_file=output_image)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()