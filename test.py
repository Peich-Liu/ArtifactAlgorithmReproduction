# PCA.py

import sys

def main():
    # 从 stdin 读：先读一个整数，表示数据个数
    line = sys.stdin.readline()
    if not line:
        print("No input from C++", file=sys.stderr)
        return

    n = int(line.strip())

    # 依次读取 n 个浮点数
    data = []
    for _ in range(n):
        line = sys.stdin.readline()
        if not line:
            break
        val = float(line.strip())
        data.append(val)

    print(f"[Python] Received {len(data)} data points:", data, file=sys.stderr)

if __name__ == "__main__":
    main()
