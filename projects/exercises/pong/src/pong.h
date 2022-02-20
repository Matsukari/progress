#pragma once
#define pong_h
#include "/home/amon/programming/lib/SDLU.h"

using namespace SDLU;
using std::cout;


struct Timer
{
	uint32_t last = 0;

	void Start()
	{
		last = SDL_GetTicks();
	}
	uint32_t SinceStart()
	{
		return SDL_GetTicks() - last;
	}

};




struct ActorProfile
{
	ActorProfile(Recti pscreen, Rectf prect, Color phue) : screen(pscreen), rect(prect), hue(phue), id(0) {id++;}
	~ActorProfile() {}
	Recti screen;
	Rectf rect;
	Color hue;

	int id;
};
class Actor : public ActorProfile
{
public:
	Actor(Window* pwin, const ActorProfile* pprofile);
	virtual ~Actor();

	virtual void Handle_Events(const SDL_Event& event);
	virtual void Update();
	virtual void Draw() const;

public:
	Window* win;
	Pointf vel;
	bool is_dead;

};

class Ball;

class Paddle : public Actor
{
public:
	Paddle(Window* pwin, const ActorProfile* pprofile);
	~Paddle() override;

	void Handle_Events(const SDL_Event& event) override;
	void Update() override;
	
};
class Ball : public Actor
{
public:
	Ball(Window* pwin, const ActorProfile* pprofile);
	~Ball() override;

	void Update() override;

public:
	vector<Paddle>* paddles;
};


class Pong
{
public:
	Pong(Recti pscreen, Window* pwin, uint8_t paddlecount, uint8_t ballcount);
	~Pong();
	
	void Handle_Events(const SDL_Event& event);
	void Update();
	void Draw();

public:
	Recti screen;
	Window* win;

	vector<Paddle> paddles;
	vector<Ball> balls;

	bool is_paused;

	vector<ActorProfile> paddleprofs;

	Timer timer;
};

