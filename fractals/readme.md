# libraries
* cairo
* PIL
* numpy

# Introduction
L Systems very useful in generation nature-like objects, like a trees or grass/weeds.
At first, I create a code for generating trees, which base on classical L-systems.
(simple_random_tree.py)

But I really wanted to try some crazy experiment: to merge fractals and cellular automata.
Surprising, but I find something like that in
http://www0.cs.ucl.ac.uk/staff/p.bentley/teaching/L6_reading/lsystems.pdf
It’s not exactly what I was looking for, but it's looks like 1D automata.

I decided to test this experimental technique.
After a lot of hours I finally create a system, which works pretty perfect.
And this is fascinating for me. Because fist tries of merging was failed.
You can see them in *gallery* folder.
Theory of L-systems is way too difficult, thus I don't know what exactly I create, but this looks very interesting.
(main.py)



# Gallery
herbarium.py can generate not only grass, even figures (carpet_0.png) and


# About terminology:
LSystem is algorithm for generation nature-like systems
I used it for generating a graph, which uses in plant drawing

LAutomaton is a special system. A merge between l-systems and cellular automatons
* seed = dictionary for LAutomaton



# Genetics:
As all the parts of my project, this was an experiment. Probably fail, probably successful.
...
* it was generated and rendered above of 1000 random pictures of plants
* after that, I chose ~50 the best seeds
* after that, there are 6 stages of artificial selection of the best seeds
* now I have around 100 good seed 
...
Actually, a percent of good-looking plants now is bigger than before using genetics,
so this is usable enough.

# Rendering
One of the most important parts of rendering is color.
With proper their combinations it's easy to create realistic structure.

# Conclusion
My program can draw nature-like plants with interesting algorithms.
This technique could be used with other for generation fractal structures.