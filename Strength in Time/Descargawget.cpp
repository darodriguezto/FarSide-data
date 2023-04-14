#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>

int main() {
    std::ifstream infile("listaurl.txt");
    std::string url;

    while (std::getline(infile, url)) {
        std::cout << "Descargando " << url << "..." << std::endl;

        // Obtener el nombre del archivo a partir de la URL
        std::string filename = url.substr(url.find_last_of("/") + 1);

        // Descargar el archivo con wget
        std::string command = "wget " + url + " -O " + filename;
        system(command.c_str());
    }

    infile.close();

    std::cout << "Descarga completada." << std::endl;

    return 0;
}

