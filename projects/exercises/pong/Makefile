#OBJS specifies which files to compile as part of the project
OBJS = /home/amon/programming/lib/SDLU.o \
	   /home/amon/programming/projects/exercises/pong/src/pong.cpp \
	   /home/amon/programming/projects/exercises/pong/src/system.cpp \
	   /home/amon/programming/projects/exercises/pong/src/main.cpp

#CC specifies which compiler we're using
CC = g++

#INCLUDE_PATHS specifies the additional include paths we'll need: -IC:<dir>
INCLUDE_PATHS = 

#LIBRARY_PATHS specifies the additional library paths we'll need: -LC:<dir>
LIBRARY_PATHS = 

#COMPILER_FLAGS specifies the additional compilation options we're using
# -w suppresses all warnings
# -Wl,-subsystem,windows gets rid of the console window
COMPILER_FLAGS = -std=c++17 

#LINKER_FLAGS specifies the libraries we're linking against
LINKER_FLAGS = -lSDL2 -lSDL2_image -lSDL2_ttf -lSDL2_mixer

#OBJ_NAME specifies the name of our exectuable
OBJ_NAME = pong!

#This is the target that compiles our executable
all : $(OBJS)
	$(CC) $(OBJS) $(INCLUDE_PATHS) $(LIBRARY_PATHS) $(COMPILER_FLAGS) $(LINKER_FLAGS) -o $(OBJ_NAME)