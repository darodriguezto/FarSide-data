#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <sys/stat.h>

int main(int argc,char **argv) {
  std::string folder_name = argv[1]; //se agregó esta línea para que se descarguen los archivos en una carpeta de nombre igual al año
  std::ifstream infile("listaurl.txt");//MÁS ADELANTE INCLUIR PARA QUE LISTATXT SE DESCARGUE EN EL FOLDER ESPECÍFICO 
  std::string url;

  //* CREAR CARPETA
  int result = mkdir(folder_name.c_str(), 0777);
  if (result != 0) {
    std::cerr << "Error al crear la carpeta " << folder_name << std::endl;
    return 1;
  }

  while (std::getline(infile, url)) {
    std::cout << "Descargando " << url << "..." << std::endl;

    // Obtener el nombre del archivo a partir de la URL
    std::string filename = url.substr(url.find_last_of("/") + 1);

    // Descargar el archivo con wget
    std::string command = "wget " + url + " -P " + folder_name + " -O " + folder_name + "/" + filename;
    system(command.c_str());
  }

  infile.close();

  std::cout << "Descarga completada." << std::endl;

  return 0;
}

