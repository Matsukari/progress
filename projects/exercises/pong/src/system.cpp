#include "system.h"

System::System()
{
	sdl = new SDLsys(SDL_INIT_EVERYTHING);
	window = new Window(
		sdl, 
		"Pong",
		BLACK,
		Size(720, 480),
		SDL_WINDOW_SHOWN | SDL_WINDOW_RESIZABLE,
		SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC
	);
	is_running = window->Is_Running();

	pong = new Pong(Recti{0, 0, window->GetSize().w, window->GetSize().h}, window, 1, 1);
}
System::~System()
{
	delete pong;
	delete window;
	delete sdl;

	printf("\nLOG: destroyed game");
}


void System::Run()
{
	while (is_running)
	{
		Handle_Events();
		Update();
		Draw();
	}
}
void System::Handle_Events()
{
	while (SDL_PollEvent(&event))
	{
		if (event.type == SDL_QUIT) is_running = false;
		pong->Handle_Events(event);
	}
}
void System::Update()
{
	window->Update();
	pong->Update();

}
void System::Draw()
{
	window->Draw();
	pong->Draw();

	window->ShowFps();
}
