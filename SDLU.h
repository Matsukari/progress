#pragma once
#define SDLU_h

#include <iostream>
#include <cstdlib>
#include <cctype>
#include <cstdint>
#include <cmath>
#include <string>
#include <vector>
#include <array>
#include <map>
#include <fstream>
#include <sstream>
#include <iterator>
#include <sys/time.h>
#include <random>
#include <functional>


#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <SDL2/SDL_ttf.h>
#include <SDL2/SDL_mixer.h>

using std::string;
using std::vector;
using std::array;

namespace SDLU
{
#define PI 3.1415

enum EAlignment
{
	ALIGN_LEFT,
	ALIGN_RIGHT,
	ALIGN_CENTER
};
enum EDirection
{
	DIR_LEFT,
	DIR_RIGHT,
	DIR_TOP,
	DIR_BOTTOM,
	DIR_NONE
};

uint32_t Abs(int n);
uint8_t Abs8(int8_t n);


int RandInt(int min, int max);
float RandFloat(float min, float max);

struct Timer
{
	uint32_t last = 0;

	void Start() { last = SDL_GetTicks(); }
	uint32_t SinceStart() { return SDL_GetTicks() - last; }

};


struct Color;

struct Color : public SDL_Color
{
	Color(uint8_t pr, uint8_t pg, uint8_t pb, uint8_t pa = 255) { r = pr; g = pg; b = pb; a = pa; }
	~Color() = default;

	Color& operator=(const Color& color)=default;

	static Color GetValue(float pr, float pg, float pb, float pa = 255.0f);
	void GetNormal(float& pr, float& pg, float& pb, float& pa) const;
};
static const Color
	GREY(192, 192, 192), 	DARK_GREY(128, 128, 128), 	VERY_DARK_GREY(64, 64, 64),
	RED(255, 0, 0), 		DARK_RED(128, 0, 0), 		VERY_DARK_RED(64, 0, 0),
	YELLOW(255, 255, 0), 	DARK_YELLOW(128, 128, 0), 	VERY_DARK_YELLOW(64, 64, 0),
	GREEN(0, 255, 0), 		DARK_GREEN(0, 128, 0), 		VERY_DARK_GREEN(0, 64, 0),
	CYAN(0, 255, 255), 		DARK_CYAN(0, 128, 128), 	VERY_DARK_CYAN(0, 64, 64),
	BLUE(0, 0, 255), 		DARK_BLUE(0, 0, 128), 		VERY_DARK_BLUE(0, 0, 64),
	MAGENTA(255, 0, 255), 	DARK_MAGENTA(128, 0, 128), 	VERY_DARK_MAGENTA(64, 0, 64),
	WHITE(255, 255, 255), 	BLACK(0, 0, 0), 			BLANK(0, 0, 0, 0);

struct Rectf;
struct Recti;
struct Recti : public SDL_Rect
{
	Recti(int px, int py, int pw, int ph) { x = px; y = py; w = pw; h = ph; }
	Recti(const Rectf& prect);

	~Recti() = default;

	Recti& operator=(const Rectf& prect);

	int Top()    const 	{ return y; }
	int Bottom() const  { return y + h; }
	int Left()   const 	{ return x; }
	int Right()  const  { return x + w; }

	float CenterX() const { return (float)(x + (w / 2)); }
	float CenterY() const { return (float)(y + (h / 2)); }
}; 

struct Rectf : public SDL_FRect
{
	Rectf(float px, float py, float pw, float ph) { x = px; y = py; w = pw; h = ph; }
	Rectf(const Recti& prect) { x = prect.x; y = prect.y; w = prect.w; h = prect.h; }

	~Rectf() = default;

	Rectf& operator=(const Recti& prect);

	float Top() 	const { return y; }
	float Bottom() 	const { return y + h; }
	float Left() 	const { return x; }
	float Right() 	const { return x + w; }

	float CenterX() const { return (float)(x + (w / 2)); }
	float CenterY() const { return (float)(y + (h / 2)); }


}; 


struct Pointi : public SDL_Point
{
	Pointi(int px, int py) { x = px; y = py; }
};
struct Pointf : public SDL_FPoint
{
	Pointf(float px, float py) { x = px; y = py; }
};
struct Size
{
	Size(const Recti& screen, float pw, float ph) { *this = GetValue(screen, pw, ph); }
	Size(int pw, int ph) { w = pw; h = ph; }
	~Size() = default;

	int w; 
	int h;

	 // Get value of normalized pw and ph based of screen
	static Size GetValue(const Recti& screen, float pw, float ph);
	 // Get normalized value of pw and ph based of screen
	void GetNormal(const Recti& screen, float& pw, float& ph) const;

};
struct Circle
{
	Circle(float px, float py, float pr) {x = px; y = py; r = pr;}
	~Circle() = default;
	// center x, y
	float x;  float y;
	float r;

	float TopLeftX() const { return x - r; }
	float TopLeftY() const { return y - r; }

	float Diameter() const { return (r + r ); }
};

struct Text
{
	Recti rect;

	vector<string> lines = {};
	vector<Color> color = {};

	int space_margin = 0;
	EAlignment alignment = ALIGN_LEFT;
};


// return as x and y.
// -1 for left and top, 1 for right and bottom, and 0 which is null( collided not )
int CheckCollision(const Recti& a, const Recti& b);
int CheckCollision(const Rectf& a, const Rectf& b);


class SDLsys
{
public:
	SDLsys(uint32_t pflags);
	~SDLsys();

public:
	bool is_init;
};



class Window 
{
public:
	Window(const SDLsys* sdl, string ptitle, Color pbgcol, Size psize, uint32_t pwinflag, uint32_t prenflag);
	~Window();

	void TestFps();
	void ShowFps();

	void SetIcon(const char *icon);
	void Create_Window(Uint32 pflags);
	void Create_Renderer(Uint32 pflags);

	void Update();
	void Draw();


	SDL_Window* GetWindow() 	{ return window; }
	SDL_Renderer* GetRenderer() { return renderer; }

	Size GetSize() const { return size; }
	double GetDeltaTime() const { return deltatime; }
	float GetFPS() const { return fps; }
	bool Is_Running() const { return is_running; }

private:
	SDL_Window* window;
	SDL_Renderer* renderer;

	string title;
	Color bgcol;

	Size size;
	uint32_t winflags;
	uint32_t renflags;

	bool is_running;
	double deltatime;
	float fps;

private:
	int lastframe;
	int curframe;
	float lastframetick;

};


SDL_Texture* LoadTexture(SDL_Renderer* renderer, const char* path);

class Texture 
{
public:
	Texture(Window* pwin, const char* ppath);
	~Texture();

	SDL_Texture* GetTexture() 	const { return texture; }
	SDL_RendererFlip GetFlip() 	const { return flip; }
	string GetPath() 	const { return path; }
	double GetAngle() 	const { return angle; }


	bool Load(const char* ppath);

	void Draw(Recti prect, Recti* pclip = nullptr);
	void Draw(Rectf prect, Recti* pclip = nullptr);


	void SetOpacity(Uint8 pa);
	void SetColor(Color pcol);

	void Destroy();

private:
	Window* window;
	SDL_RendererFlip flip {SDL_FLIP_NONE};
	SDL_Texture* texture {nullptr};

	string path;
	bool is_loaded {false};
	double angle {360.0f};
};


// draw
void DrawRectFill(SDL_Renderer* ren, const Color& col, const Recti& rect);
void DrawRectFill(SDL_Renderer* ren, const Color& col, const Rectf& rect);

void DrawRectEdge(SDL_Renderer* ren, const Color& col, const Recti& rect);
void DrawRectEdge(SDL_Renderer* ren, const Color& col, const Rectf& rect);

void DrawLine 	 (SDL_Renderer* ren, const Color& col, Pointi a, Pointi b);
void DrawLine 	 (SDL_Renderer* ren, const Color& col, Pointf a, Pointf b);

void DrawPixel	 (SDL_Renderer* ren, const Color& col, Pointi pos);
void DrawPixel	 (SDL_Renderer* ren, const Color& col, Pointf pos);


void DrawGridLines(SDL_Renderer* ren, const Color& color, Pointi start, Pointi end, int margin_x, int margin_y);


}


