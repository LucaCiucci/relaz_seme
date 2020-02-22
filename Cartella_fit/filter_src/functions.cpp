#include "functions.hpp"

double m_2pi = 2.0 * acos((double)-1);
double normFactor = 1.0 / sqrt(m_2pi);

////////////////////////////////////////////////////////////////
RunSet readFile(std::string fileName)
{
	std::ifstream file(fileName, std::ifstream::in);
	std::string line;
	std::istringstream sLine(line);


	RunSet set;
	RunData data;
	Row row;
	data.clear();
	set.clear();

	while (std::getline(file, line))
		//while (file >> line)
	{
		// quando c'è un nuovo blocco
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
	/*for (auto x : row)
	{
		stream << x;
		stream << ' ';
	}*/

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
		stream << "========= pippo" << std::endl;
	}

	return stream;
}

////////////////////////////////////////////////////////////////
std::tuple<double, double> meanSigma(double x, const RunData& runData)
{
	std::vector<double> w(runData.size());
	for (int i = 0; i < runData.size(); i++)
		w[i] = gaussian(x, runData[i].V, runData[i].stdV);
	
	double sum_w = 0;
	for (auto _w : w)
		sum_w += _w;

	double my = 0;
	for (int i = 0; i < runData.size(); i++)
	{
		w[i] /= sum_w;
		my += runData[i].I * w[i];
	}

	double var_y = 0;
	for (int i = 0; i < runData.size(); i++)
		var_y += sqr(runData[i].I - my) * w[i];

	double var_my = 0;
	for (int i = 0; i < runData.size(); i++)
	{
		const auto& row = runData[i];
		var_my += sqr(w[i]) * var_y + sqr(row.I / sum_w) * ((exp(-sqr(x - row.V) / (3.0 * sqr(row.stdV)) / )))
	}

	/*
	for j = 1:numel(xx)
		w(j) = f(x, xx(j), dxx(j));
	end
	sum_w = sum(w);
	w = w / sum_w;

	my = sum(yy .* w);
	var_y = sum(sum((yy - my).^2 .* w));
	%var_my = sum(w.^2 * var_y);
	var_my = 0;
	for j = 1:numel(xx)
		var_my = var_my + w(j)^2 * var_y + (yy(j) / sum_w)^2 * ((exp(-(x - xx(j))^2/...
			(3*dxx(j)^2))/(sqrt(2)*sqrt(3)*sqrt(pi)*dxx(j))-exp(-(3*...
			(x - xx(j))^2)/(4*dxx(j)^2))/(sqrt(pi)*dxx(j))+exp(-...
			(x - xx(j))^2/dxx(j)^2)/(sqrt(2)*sqrt(pi)*dxx(j)))/...
			(sqrt(2)*sqrt(pi)*dxx(j)));
		% NOTA: sarebbbe meglio la versione semplificata
	end
	*/
	return std::tuple<double, double>(my, 0);
}
