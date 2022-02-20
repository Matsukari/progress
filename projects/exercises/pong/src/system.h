#pragma once
#define program

#include "pong.h"


class System
{
public:
	System();
	~System();

	void Run();
	void Handle_Events();
	void Update();
	void Render();
	
	void Draw();

private:
	SDLsys* sdl;
	Window* window;
	Pong* pong;
	SDL_Event event;

	bool is_running;
};