#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

int main() {
    std::ifstream archivo("listaETA2012.txt"); // Nombre del archivo que contiene la lista de nombres de archivos txt

    if (archivo.is_open()) {
        std::string nombreArchivo;
        while (std::getline(archivo, nombreArchivo)) {
            std::ifstream archivoTxt(nombreArchivo);
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
                std::cout << "No se pudo abrir el archivo: " << nombreArchivo << std::endl;
            }
        }

        archivo.close();
    } else {
        std::cout << "No se pudo abrir el archivo 'listaETA2012.txt'." << std::endl;
    }

    return 0;
}

