#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main(int argc,char **argv) {
  std::string year =argv[1];
  std::string folderpath= year +"/";
  ifstream archivo(folderpath + "listasuma.txt");
  string linea;

  // Lee cada línea del archivo                                                                                                                                                                                                             
  while (getline(archivo, linea)) {
    // Busca la posición de la palabra "AR_LIST_"                                                                                                                                                                                         
    size_t posicion_ar_list = linea.find(year +"/AR_LIST_");

    // Busca la posición de la palabra ".txt"                                                                                                                                                                                             
    size_t posicion_txt = linea.find(".txt");

    // Si ambas palabras se encuentran en la línea                                                                                                                                                                                        
    if (posicion_ar_list != string::npos && posicion_txt != string::npos) {
      // Obtiene una subcadena que excluye las palabras "AR_LIST_" y ".txt"                                                                                                                                                             
      string linea_final = linea.substr(0, posicion_ar_list) + linea.substr(posicion_ar_list + 13, posicion_txt - posicion_ar_list - 13) + linea.substr(posicion_txt + 4);

      cout << linea_final << endl;
    }
  }

  archivo.close();

  return 0;
}
