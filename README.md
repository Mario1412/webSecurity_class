# webSecurity_class
[toc]

## project requirement
1. project 1: /game/proj1.pdf
2. project 2: /xss/proj2.pdf

## Homework 1: Five in a row
### How to run
the content of project does follow:
```
 -- game
    -- app
        helloWorld.py
    -- static
        black.png
        white.png
    -- template
        ai_game.html
        local_game_cavans.html
        server_client_game.html
```
The main function exists in helloWorld.py. So in order to run the whole application, you need to execute the command-line: ```python helloWorld.py``` in your console.

### A javascript client
Open the file 'local_game_cavans.html' and you don't need to start the whole project.

### A server, two javascript client
After starting the whole application, you need to take some actions as follow:
1. Open the browser
2. Type the link: http://127.0.0.1:5000 on two clients
3. You can start the game unless both two clients are ready to play

**note:**There are some limitations when playing the game
1. When there are two players playing the game, no another player can open the browser and play the game, which means only two clients are allowed to connect the server at the same time
2. When two players are playing the game and one of the player refreshes the browser and cause the game stuck, which will send a new request to server for building the connection, you need to restart the server. Otherwise, the game won't continue.

### Ai battle
After starting the whole application, you need to take some actions as follow:
1. Open the browser
2. Type the link: http://127.0.0.1:5000/ai

**note:**There are some limitations when playing the game
1. Only one user is allowed to play the game at the same time
2. If the user refreshes the browser when playing the game, you need to restart the server, otherwise the game won't continue.

## Homework 2: Cross-site Scripting: Attack and Defense
The detail instruction can be found in /xss directory. Please check it 