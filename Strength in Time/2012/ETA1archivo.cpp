#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

int main() {
    std::ifstream archivo("AR_LIST_2012.01.01_00:00:00.txt"); // Nombre del archivo que deseas leer
    std::vector<std::vector<std::string>> datos; // Vector bidimensional para almacenar los datos de las columnas 3 y 4

    if (archivo.is_open()) {
        std::string linea;
        int fila = 1;
        while (std::getline(archivo, linea)) {
            if (fila >= 8) {
                std::istringstream iss(linea);
                std::vector<std::string> filaDatos;
                std::string dato;
                int columna = 1;
                while (iss >> dato) {
                    if (columna == 4 || columna == 5) {
                        filaDatos.push_back(dato);
                    }
                    columna++;
                }
                datos.push_back(filaDatos);
            }
            fila++;
        }

        archivo.close();

        // Imprimir los datos de la columna 3 y 4 a partir de la octava fila
        for (const std::vector<std::string>& filaDatos : datos) {
            for (const std::string& dato : filaDatos) {
                std::cout << dato << "\t";
            }
            std::cout << std::endl;
        }
    } else {
        std::cout << "No se pudo abrir el archivo." << std::endl;
    }

    return 0;
}
