#include "functions.hpp"


/*

esecuzione programma:
"filtro.exe --in file_in.txt --out file_out.txt --maxRatio 3 --minV 0.2"

*/

int main(int argc, char** argv)
{
	std::cout << "Hello there!" << std::endl;

	std::string fileNameIn = DEFAULT_INPUT_FILE_NAME;
	std::string fileNameOut = DEFAULT_OUTPUT_FILE_NAME;
	double maxRatio = DEFAULT_MAX_RATIO;
	double minV = DEFAULT_MIN_V;

	// parsing parametri
	for (int i = 1; i < argc; ++i)
	{
		if (std::string(argv[i]) == "-in")
			if (i + 1 < argc) // Make sure we aren't at the end of argv!
				fileNameIn = argv[++i]; // Increment 'i' so we don't get the argument as the next argv[i].

		if (std::string(argv[i]) == "-out")
			if (i + 1 < argc)
				fileNameOut = argv[++i];

		if (std::string(argv[i]) == "-maxRatio")
			if (i + 1 < argc)
				maxRatio = std::stod(argv[++i]);

		if (std::string(argv[i]) == "-minV")
			if (i + 1 < argc)
				minV = std::stod(argv[++i]);
	}


	// legge file di dati da analizzare
	std::cout << "Lettura file: " << fileNameIn << std::endl;
	RunSet set = readFile(fileNameIn);

	// esegue la selezione dei dati
	std::cout << "Selezione dati... " << std::endl;
	auto [out, out_bad] = selectData(set, maxRatio, minV);

	// salva su file
	std::cout << "Salva file: " << fileNameOut << std::endl;
	std::ofstream outFile(fileNameOut, std::ifstream::out);
	outFile << out << std::endl;
	std::cout << "Salva file: " << fileNameOut+".bad" << std::endl;
	std::ofstream outFile_bad(fileNameOut + ".bad", std::ifstream::out);
	outFile_bad << out_bad << std::endl;

	return 0;
}




/*


std::ofstream outFile(fileNameOut, std::ifstream::out);
	std::cout << set[6].size() << std::endl;
	for (double x = 0; x < 1.5; x += 0.0001)
	{
		auto [my, sy, smy] = meanSigma(x, set[6]);

		outFile << x << "    ";
		outFile << my << "    ";
		outFile << sy << "    ";
		outFile << smy << std::endl;
	}
	return 0;


*/











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





