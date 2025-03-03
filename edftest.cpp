#include <iostream>
#include <thread>
#include <cstdlib>
#include <vector>
#include "edflib.h"

using namespace std;

int main(){
    cout << "Starting EEG processing...\n";
    // 请确保路径正确，且文件存在
    std::string NewFileName = "c://Document//PhD//EEG//Artifact//data//tuh_eeg_artifact//edf//01_tcp_ar//aaaaaaju_s005_t000.edf";
    if (NewFileName.empty()) {
        std::cerr << "No file specified\n";
        return 1;
    }

    edf_hdr_struct edf_struct;
    // 打开 EDF 文件（只读模式），并且加载所有注释
    int handle = edfopen_file_readonly(NewFileName.c_str(), &edf_struct, EDFLIB_READ_ALL_ANNOTATIONS);



    int sig_idx = 1;
    int total_samples = edf_struct.signalparam[sig_idx].smp_in_datarecord
                  * edf_struct.datarecords_in_file;
    std::vector<double> buffer(total_samples);
    int samples_read = edfread_physical_samples(handle, sig_idx, total_samples, buffer.data());
    
    cout<<"buffer"<<buffer[0]<<endl;

    edfclose_file(handle);

    return 0;
}
