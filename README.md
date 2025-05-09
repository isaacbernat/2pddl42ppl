# 2pddl42ppl
2 paddles for (up to) 2 people to play on a single console.

Proof of concept implementation in [Thumby](https://thumby.us/) which uses familiar Pong mechanics. Has Versus, Coop and Solo modes. Physics, paddle, balls and up to 8 parameters are easily adjusted using the game settings menu. All this well under 0x100 (255) lines of code.

## Footage
<iframe width="80%" height="auto" src="https://www.youtube.com/embed/K-yZ11NldGY" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Do you think [Thumby](https://thumby.us/) is too small to be played by an adult. Well, here is proof it can be played by 2 at the same time with a single device! Notice that the ball gets smaller (and faster) on each bounce to keep it challenging (and one may configure this among other params).

## How to play?
- Player 1 controls the leftmost paddle using up and down arrows from D-pad (as expected).
- Player 2 controls the other paddle using A and B buttons, the topmost to move the paddle up, the other down.
- The goal is to keep the ball bouncing on the paddles for as long as possible.
- You can try it on a [Thumby emulator here](https://code.thumby.us/)

## Why?
I wanted to show it's possible to have real-time multiplayer games under the restrictions of a simple handheld console.

I remember as a kid I watched my older brother play on a GameBoy over his shoulder. We only had one console, but multiplayer games required two (plus a Game Link Cable). Consoles connected to a tv display usually have 2+ independent controllers. But computers with a single keyboard already allowed multiple players! They have many keys, but pressing more than 3 keys at once wasn't supported (a meta-strategy could be to press many keys at once to lock the keyboard and prevent your opponent from doing anything (e.g. moving away from a bomb in Bomberman)). Not as challenging as just having a D-pad and 2 buttons, but enough to push me in that direction.

## See also
Feel free to contact me if you'd like to push this proof of concept further, or if this inspired you (e.g. to build similar projects).

Another "proof of concept" game I created, soon after I got my Thumby from Kickstarter, is [tinymem](https://github.com/isaacbernat/tinymem). The goal here was to showcase a game programmed under 50 lines of (clean) Python code that used most of the console's capabilities.
