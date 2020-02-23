#ifndef FUNCTIONS_H
#define FUNCTIONS_H

#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <vector>
#include <array>
#include <chrono>
#include <thread>
#include <random>
#include <tuple>

extern double m_2pi;
extern double normFactor;


// ================================
//            CLASSI
// ================================

// rappresenta una riga del file
class Row
{
public:
	double V = 0, errV = 0, stdV = 0, I = 0, errI = 0, stdI = 0;
};

//using Row = std::array<double, 6>;// una riga è formata da 6 numeri e una ciambella
using RunData = std::vector<Row>;// rappresenta un blocco di dati (1 run)
using RunSet = std::vector<RunData>;// rappresetna un insieme di run

RunSet readFile(std::string fileName);

// stampa una riga
std::ostream& operator<<(std::ostream& stream, const Row& row);

// stampa un blocco
std::ostream& operator<<(std::ostream& stream, const RunData& data);

// stampa un insieme di blocchi separati da "#=======..."
std::ostream& operator<<(std::ostream& stream, const RunSet& set);

// ================================
//            FUNZIONI
// ================================

// quadrato di un DOUBLE (non mettere in template!)
inline double sqr(double x) { return x * x; }

// funzione gaussiana centrata in zero
inline double gaussian(double x, double sx)
{
	return normFactor * exp(-sqr(x/sx) * 0.5) / sx;
}

// ritorna media, varianza y, marianza su media
std::tuple<double, double, double> meanSigma(double x, const RunData& runData);


#endif // !FUNCTIONS_H
