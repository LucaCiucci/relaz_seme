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

extern double m_2pi;
extern double normFactor;

class Row
{
public:
	double V = 0, errV = 0, stdV = 0, I = 0, errI = 0, stdI = 0;
};



//using Row = std::array<double, 6>;// una riga è formata da 6 numeri e una ciambella
using RunData = std::vector<Row>;// rappresenta un blocco di dati
using RunSet = std::vector<RunData>;// rappresetna un insieme di run

RunSet readFile(std::string fileName);

std::ostream& operator<<(std::ostream& stream, const Row& row);
std::ostream& operator<<(std::ostream& stream, const RunData& data);
std::ostream& operator<<(std::ostream& stream, const RunSet& set);

inline double sqr(double x) { return x * x; }

inline double gaussian(double x, double mx, double sx)
{
	return normFactor * exp(-sqr((x - mx)/sx) * 0.5) / sx;
}

std::tuple<double, double> meanSigma(double x, const RunData& runData);


#endif // !FUNCTIONS_H
