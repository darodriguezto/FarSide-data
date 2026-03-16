
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
  std::string faltante;
  
  double previous_total = 0.0;  // Valor de la suma anterior
  double missing_files_sum = 0.0;  // Suma de los valores de los archivos faltantes
  int missing_files_count = 0;  // Contador de archivos faltantes consecutivos

  while (std::getline(infile, line)) {
    double total = 0.0;
    std::string datafile = folderpath + line;

    if (!fs::exists(datafile)) {
      faltante=datafile;
      //std::cout << "El archivo no existe: " << datafile << std::endl;
      missing_files_sum += previous_total;  // Agrega la suma del archivo anterior a los archivos faltantes
      missing_files_count++;
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

    if (missing_files_count > 0) {
      if (missing_files_count == 1) {
        // Si solo hay un archivo faltante, muestra su valor junto con la suma del anterior y el siguiente
        double average = (total + missing_files_sum) / 2;
        //std::cout << "Valor archivo faltante: " << missing_files_sum << std::endl;
        std::cout << faltante << "\t" << average << std::endl;
      } else {
        // Si hay varios archivos faltantes consecutivos, muestra el promedio
        //double average = (previous_total + missing_files_sum) / (missing_files_count + 1);
        //std::cout << "Valor promedio de archivos faltantes: " << average << std::endl;
      }
      missing_files_count = 0;
      missing_files_sum = 0.0;
    }

    std::cout << datafile << "\t" << total << std::endl;
    previous_total = total;  // Guarda el valor de la suma para el siguiente ciclo
    datastream.close();
  }

  infile.close();
  return 0;
}
