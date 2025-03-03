#include <iostream>
#include <cstdio>    // for popen, pclose
#include <vector>
#include <string>

int main() {
    // 一些要传给Python脚本的测试数据
    std::vector<double> mydata = {1.1, 2.2, 3.3, 4.4, 5.5};

    // 要执行的Python脚本，比如 "python PCA.py"
    // 也可以加上解释器路径，如 "/usr/bin/python3 PCA.py"
    std::string command = "python test.py";

    // 使用 popen，以“写”模式打开管道
    FILE *pipe = _popen(command.c_str(), "w");
    if (!pipe) {
        std::cerr << "popen failed!\n";
        return 1;
    }

    // 把数据以某种协议写入管道
    // 这里演示最简单的：先写一个数据量，然后逐个写浮点数
    // Python那边按相同的格式去读
    int size = mydata.size();
    // fprintf 可以写文本格式，也可以尝试写二进制
    std::fprintf(pipe, "%d\n", size);  // 先告诉Python有几个数据
    for (double val : mydata) {
        std::fprintf(pipe, "%.6f\n", val);
    }

    // 结束写入
    // 关闭管道，等待python脚本执行完
    int status = _pclose(pipe);

    std::cout << "C++ done sending data, pclose status = " << status << std::endl;
    return 0;
}