#include <iostream>
#include <thread>
#include <cstdlib>

// 运行 Python 进程的函数
void runPythonProcess(const std::string& script) {
    std::string command = "python " + script;
    int result = std::system(command.c_str());
    if (result != 0) {
        std::cerr << "Error running " << script << std::endl;
    }
}

int main() {
    std::cout << "Starting EEG processing...\n";

    // 启动 PCA 进程
    std::thread pcaThread(runPythonProcess, "PCA.py");

    // 启动 Z-score 进程
    std::thread zscoreThread(runPythonProcess, "Zscore.py");

    // 等待进程完成
    pcaThread.join();
    zscoreThread.join();

    std::cout << "Processing complete!\n";
    return 0;
}
