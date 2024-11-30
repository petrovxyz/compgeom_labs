import os
import matplotlib.pyplot as plt

def read_dataset(file_path):

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Can't find dataset: '{file_path}'")

    X = []
    Y = []
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            parts = line.strip().split()
            if len(parts) != 2:
                print(f"Skipping line {line_num}: waiting for 2 values, but getting {len(parts)}")
                continue
            try:
                x, y = map(int, parts)
                X.append(x)
                Y.append(y)
            except ValueError:
                print(f"Skipping line {line_num}: can't convert coordinates to int value")
                continue
    return X, Y

def plot_points(X, Y, canvas_width=960, canvas_height=540, output_file='output.png'):

    if not X or not Y:
        raise ValueError("Coordinates X, Y can't be empty")

    min_x, max_x = min(X), max(X)
    min_y, max_y = min(Y), max(Y)

    padding_x = (max_x - min_x) * 0.05
    padding_y = (max_y - min_y) * 0.05

    plt.figure(figsize=(canvas_width/100, canvas_height/100), dpi=100)
    plt.scatter(X, Y, s=10, c='purple', marker='o')

    plt.xlim(min_x - padding_x, max_x + padding_x)
    plt.ylim(min_y - padding_y, max_y + padding_y)

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Points from dataset')

    plt.grid(True)

    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    print(f"Image saved as '{output_file}'.")

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    dataset_file = os.path.join(current_dir, 'dataset.txt')
    output_file = os.path.join(current_dir, 'result.png')

    try:
        X, Y = read_dataset(dataset_file)
        plot_points(X, Y, canvas_width=960, canvas_height=540, output_file=output_file)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()