import sys
import os
import numpy as np
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) != 3:
        print("Usage: python analyze.py <input_csv> <output_dir>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    os.makedirs(output_dir, exist_ok=True)

    data = np.loadtxt(input_file, delimiter=",")

    mean = np.mean(data)
    std = np.std(data)
    min_val = np.min(data)
    max_val = np.max(data)
    median = np.median(data)

    base = os.path.splitext(os.path.basename(input_file))[0]

    summary_file = os.path.join(output_dir, f"{base}_summary.txt")
    hist_file = os.path.join(output_dir, f"{base}_hist.png")

    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(f"file: {input_file}\n")
        f.write(f"count: {len(data)}\n")
        f.write(f"mean: {mean:.6f}\n")
        f.write(f"std: {std:.6f}\n")
        f.write(f"min: {min_val:.6f}\n")
        f.write(f"max: {max_val:.6f}\n")
        f.write(f"median: {median:.6f}\n")

    plt.figure(figsize=(8, 5))
    plt.hist(data, bins=30)
    plt.title(base)
    plt.xlabel("value")
    plt.ylabel("count")
    plt.tight_layout()
    plt.savefig(hist_file)
    plt.close()

    print(f"Processed: {input_file}")
    print(f"Summary: {summary_file}")
    print(f"Histogram: {hist_file}")

if __name__ == "__main__":
    main()
