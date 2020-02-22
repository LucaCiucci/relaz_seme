#include "functions.hpp"





int main(void)
{
	std::cout << "Hello there" << std::endl;

	RunSet set = readFile("file2C.txt");
	//std::cout << set;
	std::cout << set.size() << std::endl;


	std::cout << gaussian(1, 0, 1) << std::endl;
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





