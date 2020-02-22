#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <vector>
#include <array>
#include <chrono>
#include <thread>
#include <random>


using Row = std::array<double, 6>;// una riga è formata da 6 numeri e una ciambella
using RunData = std::vector<Row>;// rappresenta un blocco di dati
using RunSet = std::vector<RunData>;// rappresetna un insieme di run

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
		if (sLine >> row[0] >> row[1] >> row[2] >> row[3] >> row[4] >> row[5])
		{
			data.push_back(row);
		}
	}

	if (data.size() > 0)
		set.push_back(data);

	return set;
}

std::ostream& operator<<(std::ostream& stream, const Row& row)
{
	for (auto x : row)
	{
		stream << x;
		stream << ' ';
	}

	return stream;
}

std::ostream& operator<<(std::ostream& stream, const RunData& data)
{
	for (auto x : data)
	{
		stream << x;
		stream << std::endl;
	}

	return stream;
}

std::ostream& operator<<(std::ostream& stream, const RunSet& set)
{
	for (auto x : set)
	{
		stream << x;
		stream << "========= pippo" << std::endl;
	}

	return stream;
}

int main(void)
{
	std::cout << "Hello there" << std::endl;

	RunSet set = readFile("test.txt");
	std::cout << set;

	std::cout << "Hello there" << std::endl;

	return 0;
}

/*
std::cout << "inizio" << std::endl;
std::default_random_engine generator;
std::uniform_real_distribution<double> distribution(5.0, 10.0);
std::this_thread::sleep_for(std::chrono::seconds((int)distribution(generator)));
std::cout << "fine" << std::endl;
return 0;
*/

/*
......
os.system("test_filtro.exe");
aspetta?????
rileggi file
....

*/





