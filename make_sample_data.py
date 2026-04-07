import os
import numpy as np

def main():
    os.makedirs("sample_data", exist_ok=True)

    np.random.seed(42)

    for i in range(1, 6):
        # データごとに少し平均と分散を変える
        mean = i * 10
        std = i * 2

        data = np.random.normal(loc=mean, scale=std, size=1000)

        filename = f"sample_data/data_{i:02d}.csv"
        np.savetxt(filename, data, delimiter=",", fmt="%.6f")

        print(f"Created: {filename}")

if __name__ == "__main__":
    main()
