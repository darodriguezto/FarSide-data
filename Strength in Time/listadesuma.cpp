#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;

int main() {
    string filename = "archivo.txt";
    ifstream infile(filename);
    string line;

    while (getline(infile, line)) {
        double total = 0.0;
        string datafile = line;
        ifstream datastream(datafile);
        string dataline;
        int line_count = 0;

        while (getline(datastream, dataline)) {
            line_count++;
            if (line_count < 8) {
                continue; // Salta las primeras siete líneas                                                                                                                                                                                  
            }
            // Separa la línea en campos usando el delimitador de espacio en blanco                                                                                                                                                           
            istringstream ss(dataline);
            string field;
            for (int i = 0; i < 3; i++) {
                // Descarta los primeros dos campos                                                                                                                                                                                           
                ss >> field;
            }
            // Si estamos en la octava línea o más, lee el valor de la tercera columna y lo agrega al total                                                                                                                                   
            if (line_count >= 8) {
                double value;
                ss >> value;
                total += value;
            }
        }
        cout << datafile << "\t" << total << endl;
        datastream.close();
    }
    infile.close();
    return 0;
}
