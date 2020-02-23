#include "functions.hpp"


#define DEFAULT_INPUT_FILE_NAME "file2C.txt"
#define DEFAULT_OUTPUT_FILE_NAME "file2Py.txt"


/*

esecuzione programma:
"nome_programma.exe file_input.txt file_output.txt"

*/

int main(int argc, char** argv)
{
	std::cout << "Hello there" << std::endl;

	std::string fileNameIn, fileNameOut;


	// se non ci sono parametri, usa i nomi di default
	if (argc == 1)
	{
		fileNameIn = DEFAULT_INPUT_FILE_NAME;
		fileNameOut = DEFAULT_OUTPUT_FILE_NAME;
	}
	else
	{
		if (argc != 3)
			return EXIT_FAILURE;
		fileNameIn = argv[1];
		fileNameOut = argv[2];
	}

	RunSet set = readFile(fileNameIn);


	//std::cout << set;
	std::cout << set[6].size() << std::endl;
	double tmp=0;
	for (auto& data : set)
		std::cout << "size : " << data.size() << std::endl;

	for (int i = 0; i < 10; i++)
	{
		auto [my, sy, smy] = meanSigma(1.15 + i / 100.0, set[6]);
		std::cout << my << " " << sy << " " << smy << std::endl;
	}
	for (int i = 0; i < 1000*0 + set[6].size(); i++)
	{
		auto [my, sy, smy] = meanSigma(1.3 + i / 10000.0, set[6]);
		//std::cout << my << " " << sy << " " << smy << std::endl;
		tmp += sy;
		if (i % 100 == 0)
			std::cout << (double)i/set[6].size()*100 << std::endl;
	}
	std::cout << "Hello there" << tmp << std::endl;

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





