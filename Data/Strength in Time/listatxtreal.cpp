#include <iostream>
#include <boost/filesystem.hpp>

namespace fs = boost::filesystem;

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "Debe proporcionar el nombre de la carpeta como argumento." << std::endl;
        return 1;
    }

    fs::path folderName(argv[1]);

    if (!fs::exists(folderName) || !fs::is_directory(folderName)) {
        std::cout << "La carpeta especificada no existe o no es válida." << std::endl;
        return 1;
    }

    for (const auto& entry : fs::directory_iterator(folderName)) {
        if (fs::is_regular_file(entry)) {
            std::cout << entry.path().filename().string() << std::endl;
        }
    }

    return 0;
}
