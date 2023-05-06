CXX=g++
CXXFLAGS=-Wall -Wextra -pedantic -std=c++11
year=2010
MY_ARG_VALUE=$(year)

all: listaurl run_listaurl run_Descargawget run_listatxt run_listadesuma run_sustraerpalabras grafica gitignore

Descargawget: Descargawget.cpp listaurl.txt
	$(CXX) $(CXXFLAGS) -DMY_ARG_VALUE=$(MY_ARG_VALUE) Descargawget.cpp -o Descargawget

listaurl: listaurl.cpp
	$(CXX) $(CXXFLAGS) listaurl.cpp -o listaurl

listatxt: listatxt.cpp
	$(CXX) $(CXXFLAGS) -DMY_ARG_VALUE=$(MY_ARG_VALUE) listatxt.cpp -o listatxt

archivo.txt:
	./listatxt $(MY_ARG_VALUE) > archivo.txt
listadesuma: listadesuma.cpp listasuma.txt
	$(CXX) $(CXXFLAGS) listadesuma.cpp -o listadesuma
sustraerpalabras: sustraerpalabras.cpp listasuma.txt
	$(CXX) $(CXXFLAGS) sustraerpalabras.cpp -o sustraerpalabras
grafica: graphic.gp datos.txt
	gnuplot -e "year='$(MY_ARG_VALUE)'" graphic.gp

.PHONY: clean
clean:
	rm -f download output.txt listatxt

run_listaurl: listaurl.cpp
	./listaurl $(MY_ARG_VALUE) > listaurl.txt
run_Descargawget: Descargawget
	./Descargawget $(MY_ARG_VALUE)

run_listatxt: listatxt
	./listatxt $(MY_ARG_VALUE) >> $(MY_ARG_VALUE)/archivo.txt
run_listadesuma: listadesuma
	./listadesuma $(MY_ARG_VALUE) >> $(MY_ARG_VALUE)/listasuma.txt
run_sustraerpalabras: sustraerpalabras
	./sustraerpalabras $(MY_ARG_VALUE)>> $(MY_ARG_VALUE)/datos.txt
gitignore: listatxt
	./listatxt $(MY_ARG_VALUE) >> $(MY_ARG_VALUE)/.gitignore
