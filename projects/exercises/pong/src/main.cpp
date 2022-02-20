#include "system.h"

int main(int argc, char** argv)
{
	System* sys = new System();
	sys->Run();

	delete sys;
	return 0;
}