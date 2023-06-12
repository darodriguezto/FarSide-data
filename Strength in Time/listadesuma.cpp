#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <boost/filesystem.hpp>

namespace fs = boost::filesystem;

int main(int argc, char **argv) {
  std::string year = argv[1];
  std::string folderpath = year + "/";
  std::string filename = folderpath + "archivo.txt";
  std::ifstream infile(filename);
  std::string line;

  double previous_total = 0.0;  // Valor de la suma anterior

  while (std::getline(infile, line)) {
    double total = 0.0;
    std::string datafile = folderpath + line;

    if (!fs::exists(datafile)) {
      // std::cout << "El archivo no existe: " << datafile << std::endl;
      // Calcula el promedio con la suma anterior y la siguiente
      double average = (previous_total + total) / 2;
      std::cout << datafile << average << std::endl;
      continue; // Ignora el archivo y pasa al siguiente
    }

    std::ifstream datastream(datafile);
    std::string dataline;
    int line_count = 0;

    while (std::getline(datastream, dataline)) {
      line_count++;
      if (line_count < 8) {
        continue; // Salta las primeras siete líneas
      }
      std::istringstream ss(dataline);
      std::string field;
      for (int i = 0; i < 3; i++) {
        ss >> field; // Descarta los primeros dos campos
      }
      if (line_count >= 8) {
        double value;
        ss >> value;
        total += value;
      }
    }
    std::cout << datafile << "\t" << total << std::endl;
    previous_total = total;  // Guarda el valor de la suma para el siguiente ciclo
    datastream.close();
  }
  infile.close();
  return 0;
}
