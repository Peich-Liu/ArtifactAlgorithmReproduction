import sys

def main():
    # load data from std, the first int is the data size
    line = sys.stdin.readline()
    if not line:
        print("No input from C++", file=sys.stderr)
        return

    n = int(line.strip())

    # load data
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
