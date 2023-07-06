#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

int main(int argc, char **argv) {
  std::string year=argv[1];
  std::ifstream archivo("archivo.txt"); // Nombre del archivo que contiene la lista de nombres de archivos txt
  if (archivo.is_open()) {
    std::string nombreArchivo;
    while (std::getline(archivo, nombreArchivo)) {
      std::string rutaCompleta = "/home/daniel/Documentos/GoSA/Far_Side/FarSide-data/Strength in Time/"+ year + "/"  + nombreArchivo; // Reemplazar con la ruta  donde se encuentran los archivos txt
      std::ifstream archivoTxt(rutaCompleta);
      if (archivoTxt.is_open()) {
	std::string linea;
	int fila = 1;
	std::string primeraLinea;
	while (std::getline(archivoTxt, linea)) {
	  if (fila >= 8) {
	    std::istringstream iss(linea);
	    std::string dato;
	    int columna = 1;
	    while (iss >> dato) {
	      if (columna == 4 || columna == 5) {
		std::cout << dato << "\t";
	      }
	      columna++;
	    }
	    std::cout << "\t" << primeraLinea << "\t" << nombreArchivo << std::endl; // Imprimir la primera línea y el nombre del archivo en columnas adicionales
	  } else if (fila == 1) {
	    primeraLinea = linea; // Guardar la primera línea del archivo
	  }
	  fila++;
	}

	archivoTxt.close();
      } else {
	std::cout << "No se pudo abrir el archivo: " << rutaCompleta << std::endl;
      }
    }

    archivo.close();
  } else {
    std::cout << "No se pudo abrir el archivo 'archivo.txt'." << std::endl;
  }

  return 0;
}

