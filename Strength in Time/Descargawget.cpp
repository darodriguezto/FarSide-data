#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <sys/stat.h>
#include <curl/curl.h>

/*bool archivo_existe(const std::string& url) {
CURL* curl = curl_easy_init();
if (curl) {
  // Establecer la URL de la solicitud HTTP GET
  curl_easy_setopt(curl, CURLOPT_URL, url.c_str());

  // Establecer que la solicitud debe ser de tipo HEAD
  curl_easy_setopt(curl, CURLOPT_NOBODY, 1L);

  // Ejecutar la solicitud
  CURLcode res = curl_easy_perform(curl);

  // Verificar si la solicitud se realizó correctamente
  if (res != CURLE_OK) {
    std::cerr << "Error al hacer la solicitud: " << curl_easy_strerror(res) << std::endl;
    curl_easy_cleanup(curl);
    return false;
  }

  // Obtener el código de respuesta HTTP
  long response_code;
  curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);

  // Verificar si el archivo existe
  if (response_code == 200) {
    curl_easy_cleanup(curl);
    return true;
  } else {
    curl_easy_cleanup(curl);
    return false;
  }
 } else {
  std::cerr << "Error al inicializar la librería curl" << std::endl;
  return false;
 }
}
*/ 



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

  /* if (archivo_existe(url)) {
          // Si el archivo existe, descargarlo
	  */
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
