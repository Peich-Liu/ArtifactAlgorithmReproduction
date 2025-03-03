#include <iostream>
#include <cstdio>    // for popen, pclose
#include <vector>
#include <string>
#include "edflib.h"


int main() {

    std::string NewFileName = "c://Document//PhD//EEG//Artifact//data//tuh_eeg_artifact//edf//01_tcp_ar//aaaaaaju_s005_t000.edf";
    if (NewFileName.empty()) {
        std::cerr << "No file specified\n";
        return 1;
    }

    edf_hdr_struct edf_struct;
    // open edf file
    int handle = edfopen_file_readonly(NewFileName.c_str(), &edf_struct, EDFLIB_READ_ALL_ANNOTATIONS);


    // Python script path
    std::string command = "python test.py";

    // _popen for pipeline
    FILE *pipe = _popen(command.c_str(), "w");
    if (!pipe) {
        std::cerr << "popen failed!\n";
        return 1;
    }

    int sig_idx = 1;
    int total_samples = edf_struct.signalparam[sig_idx].smp_in_datarecord
    * edf_struct.datarecords_in_file;


    //load data size --> write each data to python
    std::vector<double> buffer(total_samples);
    int samples_read = edfread_physical_samples(handle, sig_idx, total_samples, buffer.data());

    // int size = total_samples;
    int size = buffer.size();
    // std::vector<double> transfer = {buffer[0]};
    std::fprintf(pipe, "%d\n", size);  // tell python data size


    for (double val : buffer) {
        std::fprintf(pipe, "%.6f\n", val);
    }

    // close the pipe
    int status = _pclose(pipe);

    std::cout << "C++ done sending data, pclose status = " << status << std::endl;
    return 0;
}
