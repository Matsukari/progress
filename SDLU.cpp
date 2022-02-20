#include "SDLU.h"


namespace SDLU
{


static std::random_device rd;
static std::mt19937 mt(rd());
int RandInt(int min, int max)
{

	std::uniform_int_distribution<int> range(min, max);

	return range(mt);
}
float RandFloat(float min, float max)
{

	std::uniform_real_distribution<float> range(min, max);

	return range(mt);
}

Color Color::GetValue(float pr, float pg, float pb, float pa)
{
	return Color{
		.r = Abs8(static_cast<int8_t>(pr*255)), 
		.g = Abs8(static_cast<int8_t>(pg*255)), 
		.b = Abs8(static_cast<int8_t>(pb*255)), 
		.a = Abs8(static_cast<int8_t>(pa*255))
	};
}
void Color::GetNormal(float& pr, float& pg, float& pb, float& pa) const
{
	pr = static_cast<float>(r / 255);
	pg = static_cast<float>(g / 255);
	pb = static_cast<float>(b / 255);
	pa = static_cast<float>(a / 255);
}

Recti::Recti(const Rectf& prect) { x = prect.x; y = prect.y; w = prect.w; h = prect.h; }

Recti& Recti::operator=(const Rectf& prect) 
{ 
	x = static_cast<int>(prect.x); 
	y = static_cast<int>(prect.y); 
	w = static_cast<int>(prect.w); 
	h = static_cast<int>(prect.h); 
	return *this; 
}
Rectf& Rectf::operator=(const Recti& prect) 
{ 
	x = static_cast<float>(prect.x); 
	y = static_cast<float>(prect.y); 
	w = static_cast<float>(prect.w); 
	h = static_cast<float>(prect.h); 
	return *this; 
}

Size Size::GetValue(const Recti& screen, float pw, float ph)
{
	return Size{
		.w = static_cast<int>(pw*screen.w), 
		.h = static_cast<int>(ph*screen.h)
	};
}

void Size::GetNormal(const Recti& screen, float& pw, float& ph) const
{
	pw = static_cast<float>(w / screen.w);
	ph = static_cast<float>(h / screen.h);
}


int CheckCollision(const Recti& a, const Recti& b)
{
	// y axis in SDL is inverted
	// a's velocity must never be greater than b's area; a object will pass b.
	// simply checks whether a is inside b.
	
	bool is_x_inside = ((a.Right()  >= b.Left()   &&  a.Right()  <= b.Right() )) ||
					   ((a.Left()   <= b.Right()  &&  a.Left()   >= b.Left()  ));  

	bool is_y_inside = ((a.Bottom() >= b.Top()    &&  a.Bottom() <= b.Bottom())) ||
					   ((a.Top()    <= b.Bottom() &&  a.Top()    >= b.Top()   ));  

	if (is_x_inside && is_y_inside)
	{
		return true;
	}

	return false;
}
int CheckCollision(const Rectf& a, const Rectf& b)
{
	bool is_x_inside = ((a.Right()  >= b.Left()   &&  a.Right()  <= b.Right() )) ||
					   ((a.Left()   <= b.Right()  &&  a.Left()   >= b.Left()  ));  

	bool is_y_inside = ((a.Bottom() >= b.Top()    &&  a.Bottom() <= b.Bottom())) ||
					   ((a.Top()    <= b.Bottom() &&  a.Top()    >= b.Top()   ));  

	if (is_x_inside && is_y_inside)
	{
		return true;
	}

	return false;
}


SDLsys::SDLsys(uint32_t pflags)
{
	is_init = false;

	if (SDL_Init(pflags) == -1) 
	{
		printf("\nLOG ERROR: SDL failed to Initialize. SDL_Error: %s.", SDL_GetError());
	}
	else
	{
		int img_flag = IMG_INIT_PNG | IMG_INIT_JPG;

		if (!IMG_Init(img_flag) & img_flag) 
		{
			printf("\nLOG ERROR: SDL_Image Failed to initialize. IMG_Error: %s.", IMG_GetError());
		}
		else
		{
			if (TTF_Init() == -1) 
			{
				printf("\nLOG ERROR: SDL_ttf failed to initialize. TTF_Error: %s.", TTF_GetError());
			}
			else
			{
				if (Mix_OpenAudio(44100, MIX_DEFAULT_FORMAT, 2, 4096) < 0) 
				{
					printf("\nLOG ERROR: SDL_Mixer Failed to initalize. Mix_Error: %s.", Mix_GetError());
				}
				else
					is_init = true;
			}
			
		}
	}
}
SDLsys::~SDLsys()
{
	SDL_Quit();
	TTF_Quit();
	IMG_Quit();
	Mix_Quit();

	is_init = false;
}




Window::Window(const SDLsys* sdl, string ptitle, Color pbgcol, Size psize, uint32_t pwinflags, uint32_t prenflags) :

	window(nullptr), 
	renderer(nullptr), 
	title(ptitle),
	bgcol(pbgcol),
	size(psize),
	winflags(pwinflags),
	renflags(prenflags),
	fps(0),
	deltatime(0),
	is_running(false),

	lastframe(0),
	curframe(0),
	lastframetick(0)
{

	if (sdl->is_init) 
	{
		Create_Window(winflags);
		Create_Renderer(renflags);

		is_running = true;
	}
	else 
	{
		is_running = false;
		printf("LOG ERROR: SDL not initialize");
	}
}

Window::~Window() 
{
	SDL_DestroyRenderer(renderer);
	SDL_DestroyWindow(window);

	renderer = nullptr;
	window = nullptr;

	printf("\nLOG: Destroyed Game.");
}

void Window::Create_Window(Uint32 flags) 
{
	winflags = flags;

	if (window != nullptr) SDL_DestroyWindow(window);

	window = SDL_CreateWindow(
		title.c_str(), 
		SDL_WINDOWPOS_CENTERED, 
		SDL_WINDOWPOS_CENTERED, 
		size.w, 
		size.h, 
		flags
	);
}
void Window::Create_Renderer(Uint32 flags)  
{
	if (window != nullptr) 
	{
		if (renderer != nullptr) SDL_DestroyRenderer(renderer);

		renderer = SDL_CreateRenderer(window, -1, flags);
		renflags = flags;
	}
	else
		printf("\nLOG ERROR: Create Window First.");
}
void Window::SetIcon(const char *icon)
{
	SDL_Surface *surface = IMG_Load(icon);

	if (surface != NULL) 
	{
		SDL_SetWindowIcon(window, surface);
	}
	else
		printf("\nLOG ERROR: Loaded Surface is NULL.");

	SDL_FreeSurface(surface);
}

void Window::TestFps()
{
	// Count how many time the game looped within a second(1000 ms).
	if (SDL_GetTicks() > lastframe + 1000) 
	{
		lastframe = SDL_GetTicks();

		fps = curframe;
		curframe = 0;
	}

	curframe++;
}
void Window::ShowFps()
{
	TestFps();

	// execute directly only after getting NEW fps
	if (curframe <= 1) printf("\nFps (%2.f)", fps);
}

void Window::Update()
{
	SDL_RenderPresent(renderer);

	deltatime = (SDL_GetTicks() - lastframetick) / 1000.0f;
	lastframetick = SDL_GetTicks();

	if (deltatime >= 0.10f) deltatime = 0.10f;

}
void Window::Draw()
{
	SDL_SetRenderDrawColor(renderer, bgcol.r, bgcol.g, bgcol.b, bgcol.a);
	SDL_RenderClear(renderer);
}






SDL_Texture* LoadTexture(SDL_Renderer* renderer, const char* path) 
{
	SDL_Surface* surface = IMG_Load(path);
	SDL_Texture* texture = nullptr;

	printf("\nLOG: Loaded Path: (%s)", path);


	if (surface != NULL) 
	{
		texture = SDL_CreateTextureFromSurface(renderer, surface);
	}
	else 
	{
		printf("\nLOG ERROR: Loaded Surface is NULL.");
	}

	SDL_FreeSurface(surface);

	return texture;
}

Texture::Texture(Window* pwin, const char* ppath) 
{
	window = pwin;
	Load(ppath);
}
Texture::~Texture()
{
	Destroy();
	window = nullptr;
}


bool Texture::Load(const char* ppath) 
{
	if (is_loaded) Destroy();

	path = ppath;
	texture = LoadTexture(window->GetRenderer(), ppath);
	is_loaded = true;

	return texture != nullptr;
}


void Texture::Draw(Recti prect, Recti* pclip) 
{
	SDL_RenderCopyEx(window->GetRenderer(), texture, pclip, &prect, angle, NULL, flip);
}
void Texture::Draw(Rectf prect, Recti* pclip) 
{
	SDL_RenderCopyExF(window->GetRenderer(), texture, pclip, &prect, angle, NULL, flip);
}


void Texture::SetOpacity(Uint8 pa) 
{
	SDL_SetTextureAlphaMod(texture, pa);
}

void Texture::SetColor(Color pcol) 
{
	SDL_SetTextureColorMod(texture, pcol.r, pcol.g, pcol.b);
}


void Texture::Destroy() 
{
	printf("\nLOG: Destroying Texture: %s...", path.c_str());

	SDL_DestroyTexture(texture); 

	is_loaded = false;
	texture = nullptr;
}



// GFX

void DrawRectFill(SDL_Renderer* ren, const Color& col, const Recti& rect) 
{
	SDL_SetRenderDrawColor(ren, col.r, col.g, col.b, col.a);
	SDL_RenderFillRect(ren, &rect);
}
void DrawRectFill(SDL_Renderer* ren, const Color& col, const Rectf& rect) 
{
	SDL_SetRenderDrawColor(ren, col.r, col.g, col.b, col.a);
	SDL_RenderFillRectF(ren, &rect);
}

void DrawRectEdge(SDL_Renderer* ren, const Color& col, const Recti& rect) 
{
	SDL_SetRenderDrawColor(ren, col.r, col.g, col.b, col.a);
	SDL_RenderDrawRect(ren, &rect);
}
void DrawRectEdge(SDL_Renderer* ren, const Color& col, const Rectf& rect) 
{
	SDL_SetRenderDrawColor(ren, col.r, col.g, col.b, col.a);
	SDL_RenderDrawRectF(ren, &rect);
}

void DrawLine(SDL_Renderer* ren, const Color& col, Pointi a, Pointi b) 
{
	SDL_SetRenderDrawColor(ren, col.r, col.g, col.b, col.a);
	SDL_RenderDrawLine(ren, a.x, a.y, b.x, b.y);
}
void DrawLine(SDL_Renderer* ren, const Color& col, Pointf a, Pointf b) 
{
	SDL_SetRenderDrawColor(ren, col.r, col.g, col.b, col.a);
	SDL_RenderDrawLineF(ren, a.x, a.y, b.x, b.y);
}


void DrawPixel(SDL_Renderer* ren, const Color& col, Pointi pos) 
{
	SDL_SetRenderDrawColor(ren, col.r, col.g, col.b, col.a);
	SDL_RenderDrawPoint(ren, pos.x, pos.y);
}
void DrawPixel(SDL_Renderer* ren, const Color& col, Pointf pos) 
{
	SDL_SetRenderDrawColor(ren, col.r, col.g, col.b, col.a);
	SDL_RenderDrawPointF(ren, pos.x, pos.y);
}

void DrawGridLines(SDL_Renderer* ren, const Color& col, Pointi start, Pointi end, int margin_x, int margin_y)
{
	/*// Vertical Lines.
	for (unsigned short i = start_x; i <= end_x; i += margin_x) {
		Draw_Line(ren, col, i, 0, i, end_y);
	}

	// Horizontal Lines.
	for (unsigned short i = start_y; i <= end_y; i += margin_y) {
		Draw_Line(renderer, col, 0, i, end_x, i);
	}*/
}
}