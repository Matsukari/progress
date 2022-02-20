#include "pong.h"


Actor::Actor(Window* pwin, const ActorProfile* pprofile) : 
	ActorProfile(pprofile->screen, pprofile->rect, pprofile->hue),
	win(pwin),
	vel({0, 0}),
	is_dead(false)
{
	printf("LOG: actor constructed\n");
}
Actor::~Actor()
{
	win = nullptr;
	printf("LOG: actor destructed\n");
}
void Actor::Handle_Events(const SDL_Event& event) 
{
}
void Actor::Update() 
{
}
void Actor::Draw() const 
{
	if (!is_dead) DrawRectFill(win->GetRenderer(), hue, rect);

}



Paddle::Paddle(Window* pwin, const ActorProfile* pprofile) : 
	Actor(pwin, pprofile)
{
	cout << "LOG: paddle constructed\n";
}
Paddle::~Paddle()
{
	printf("LOG: paddle destructed\n");
}
float Differ(float a, float b)
{
	return a - b;
}
void Paddle::Handle_Events(const SDL_Event& event) 
{
	vel.y = 0.0f;

	if (SDL_KEYDOWN && event.key.keysym.sym == SDLK_w) {vel.y = -300.0f;cout << "WWWWWW";}
	if (SDL_KEYDOWN && event.key.keysym.sym == SDLK_s) {vel.y = 300.0f; cout << "SSSSSS";}

}
void Paddle::Update() 
{
	if (!is_dead)
	{
		cout << "\nVel: " << vel.y * win->GetDeltaTime();
		rect.y += vel.y * win->GetDeltaTime();

		// go out of screen
		if (!CheckCollision(rect, Rectf{screen})) 
		{
			rect.y -= Differ(rect.y, screen.y);
		}
	}
}


Ball::Ball(Window* pwin, const ActorProfile* pprofile) : 
	Actor(pwin, pprofile),
	paddles(nullptr)
{
	std::cout << "LOG: ball constructed\n";
}
Ball::~Ball()
{
	paddles = nullptr;
	printf("LOG: ball destructed\n");
}


void Ball::Update() 
{
	if (!is_dead)
	{
		rect.x += vel.x * win->GetDeltaTime();
		rect.y += vel.y * win->GetDeltaTime();

		if (rect.Right() >= screen.Right() || rect.Left() <= screen.Left()) vel.x *= -1; // bounded in x axis
		if (rect.Bottom() >= screen.Bottom() || rect.Top() <= screen.Top()) vel.y *= -1; // bounded in y axis

		for (int i = 0; i < paddles->size(); i++)
		{
			bool has_collide = CheckCollision(rect, Rectf{paddles->at(i).rect});

			// in upper side
			if (has_collide)
			{
				vel.x *= -1.0f;
			}
		}
	}
}





Pong::Pong(Recti pscreen, Window* pwin, uint8_t paddlecount, uint8_t ballcount) :

	screen(pscreen),
	win(pwin),
	is_paused(true)
{
	ActorProfile ballprof(screen, Rectf(pscreen.CenterX()-7.5f, pscreen.CenterY()-15, 15, 15), WHITE);
	paddleprofs = {
		ActorProfile(screen, Rectf(screen.Left()+5.0f, 	  screen.CenterY()-7.5f, 15.0f, 15.0f*4), WHITE), // left
		ActorProfile(screen, Rectf(screen.Right()-20.0f,  screen.CenterY()-7.5f, 15.0f, 15.0f*4), WHITE), // right
		ActorProfile(screen, Rectf(screen.CenterX()-7.5f, screen.Top()+5.0f, 	 15.0f, 15.0f*4), WHITE), // top
		ActorProfile(screen, Rectf(screen.CenterX()-7.5f, screen.Bottom()-5.0f,  15.0f, 15.0f*4), WHITE) // bottom
	};

	if (paddlecount > 4) 
	{
		printf("LOG WARN: paddlecount' var exceed limit(4)\n");
		paddlecount = 4;
	}

	std::cout << "LOG: max size for paddles: " << paddles.max_size() << "\n";
	std::cout << "LOG: max size for balls: " << balls.max_size() << "\n";

	paddles.reserve(paddlecount);
	balls.reserve(ballcount);


	for (int i = 0; i < paddlecount; i++)
		paddles.emplace_back(win, &paddleprofs[i]);

	for (int i = 0; i < paddlecount; i++)
		balls.emplace_back(win, &ballprof);

	for (auto& i : balls)
	{
		i.paddles = &paddles;
	}

}

Pong::~Pong()
{
	win = nullptr;
	printf("LOG: pong destructed\n");
}
void Pong::Handle_Events(const SDL_Event& event)
{
	static bool is_once = true;

	if ((SDL_KEYUP && event.key.keysym.sym == SDLK_j) && timer.SinceStart() > 500)
	{
		timer.Start();
		is_paused = !is_paused;

		if (!is_paused && is_once)
		{
			for (auto& i : balls)
			{
				i.vel.x = RandFloat(-300.0f, 300.0f);
				i.vel.y = RandFloat(-300.0f, 300.0f);
			}
			is_once = false;
		}
	}

	for (int i = 0; i < paddles.size(); i++)
	{
		paddles[i].Handle_Events(event);
	}

}

void Pong::Update()
{
	if (!is_paused)
	{
		for (int i = 0; i < paddles.size(); i++)
		{
			paddles[i].Update();
		}
		for (int i = 0; i < balls.size(); i++)
		{
			balls[i].Update();
		}
	}
}
void Pong::Draw()
{
	for (int i = 0; i < paddles.size(); i++)
	{
		paddles[i].Draw();
	}
	for (int i = 0; i < balls.size(); i++)
	{
		balls[i].Draw();
	}
}