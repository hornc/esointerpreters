# G_arD^EN CorUtY@rD

This is my attempt at an animated ANSI graphics version of an interpreter for [G_arD^EN CorUtY@rD](https://esolangs.org/wiki/G_arD%5EEN_CorUtY@rD), in Python.

The input command `T` is not yet implemented.

The language was designed by https://esolangs.org/wiki/User:BoundedBeans , not me.

The language appealed to me because it was a bitwise cyclic tag variant, and I have been working with BCT a bit so thought it'd be easy to figure out how it was supposed to work, and because the ASCII garden / grid layout has a pleasing game-like feel, and I could see it working with ANSI colours.

I've made the first fence row update to represent the current datastring / 'soil' as the program runs to indicate the current internal state.
The 'soil' modifies the 'fence' -- not sure that makes sense, but it's more to look at.
The command queue is not represented on screen, that might be nice, but all the current examples never get beyong one item in the command queue anyway.

![image](https://user-images.githubusercontent.com/905545/182751011-082dc6f3-cc7e-428f-a132-2048bf2cd8a3.png)
