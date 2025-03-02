#include <iostream>
#include <thread>
#include <cstdlib>

// Function to run a python script
void runPythonProcess(const std::string& script) {
    std::string command = "python " + script;
    int result = std::system(command.c_str());
    if (result != 0) {
        std::cerr << "Error running " << script << std::endl;
    }
}

int main() {
    std::cout << "Starting EEG processing...\n";

    //create and run threads
    std::thread pcaThread(runPythonProcess, "PCA.py");
    std::thread zscoreThread(runPythonProcess, "Zscore.py");

    //wait for threads to finish
    pcaThread.join();
    zscoreThread.join();

    std::cout << "Processing complete!\n";
    return 0;
}
