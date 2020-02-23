#include "functions.hpp"

double m_2pi = 2.0 * acos((double)-1);
double m_pi = acos((double)-1);
double normFactor = 1.0 / sqrt(m_2pi);
double sqrt_3 = sqrt(3.0);
double m_2sqrt_3 = sqrt(3.0) * 2.0;
double sqrt_2 = sqrt(2.0);
constexpr double maxSigma = 20.0;

////////////////////////////////////////////////////////////////
RunSet readFile(std::string fileName)
{
	// file di lettura
	std::ifstream file(fileName, std::ifstream::in);

	std::string line;
	std::istringstream sLine(line);

	// crea oggeti per contenere i dati
	RunSet set;
	RunData data;// run corrente
	Row row;// riga corrente
	data.clear();
	set.clear();

	// finchè posso leggere una riga
	while (std::getline(file, line))
		//while (file >> line)
	{
		// controlla se c'è un nuovo blocco che inizia con "#="
		// in tal caso inserisci i dati finora ottenuti in run e pulisi data
		if (line.size() >= 2 && line[0] == '#' && line[1] == '=')
		{
			if (data.size() > 0)
				set.push_back(data);

			data.clear();

			continue;
		}

		// se la riga inizia con # è un commento
		if (line.size() <= 0 || line[0] == '#')
			continue;

		sLine = std::istringstream(line);
		if (sLine >> row.V >> row.errV >> row.stdV >> row.I >> row.errI >> row.stdI)
		{
			row.stdV *= 2;//!!!!!!!!!!!!!!!!!!!!!!11
			data.push_back(row);
		}
	}

	if (data.size() > 0)
		set.push_back(data);

	return set;
}


////////////////////////////////////////////////////////////////
std::ostream& operator<<(std::ostream& stream, const Row& row)
{
	stream << row.V << "    " << row.errV << "    " << row.stdV << "    " << row.I << "    " << row.errI << "    " << row.stdI;
	return stream;
}

////////////////////////////////////////////////////////////////
std::ostream& operator<<(std::ostream& stream, const RunData& data)
{
	for (auto x : data)
	{
		stream << x;
		stream << std::endl;
	}

	return stream;
}

////////////////////////////////////////////////////////////////
std::ostream& operator<<(std::ostream& stream, const RunSet& set)
{
	for (auto x : set)
	{
		stream << x;
		stream << "#================================================================" << std::endl;
	}

	return stream;
}

////////////////////////////////////////////////////////////////
std::tuple<double, double, double> meanSigma(double x, const RunData& runData)
{
	std::vector<double> w(runData.size());
	for (int i = 0; i < runData.size(); i++)
		if (abs(runData[i].V - x) <= runData[i].stdV * maxSigma)
			w[i] = gaussian(runData[i].V - x, runData[i].stdV);
		else
			w[i] = 0;
	
	double sum_w = 0;
	for (auto _w : w)
		sum_w += _w;

	if (sum_w <= 0)
		return { 0.0, 0.0, 0.0 };

	double my = 0;
	for (int i = 0; i < runData.size(); i++)
	{
		w[i] /= sum_w;
		my += runData[i].I * w[i];
	}

	double var_y = 0;
	for (int i = 0; i < runData.size(); i++)
	{
		var_y += sqr(runData[i].I - my) * w[i];
	}

	double var_my = 0;
	for (int i = 0; i < runData.size(); i++)
	{
		const auto& row = runData[i];

		if (abs(x - row.V) > row.stdV * maxSigma)
			continue;

		double y2 = sqr(x - row.V);
		double s2 = sqr(row.stdV);
		double y2_s2 = y2 / s2;

		var_my += sqr(w[i]) * var_y // pezzo della varianza sulle y
			+ sqr(row.I / sum_w) * (// pezzo varianza x
			exp(-y2_s2*(1.0/3.0)) + sqrt_3 * (exp(-y2_s2) - sqrt_2 * exp(-(3.0/4.0) * y2_s2))// TODO ottimizza
			// (e^(-y^2/(3*s^2))+sqrt(3)*(e^(-y^2/s^2)-sqrt(2)*e^(-(3*y^2)/(4*s^2))))/(2*sqrt(3)*pi*s^2)
			) / (m_2sqrt_3 * s2 * m_pi);
	}
	return {my, sqrt(var_y), sqrt(var_my)};
}
