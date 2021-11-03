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
My program can generate not only grass, but even other interesting figures.


# About terminology:
LSystem is algorithm for generation nature-like systems
I used it for generating a graph, which uses in plant drawing

LAutomaton is a special system: a merge between l-systems and cellular automatons
* seed = dictionary for LAutomaton



# Genetics:
As all the parts of my project, this was an experiment. Probably fail, probably successful.
...
Process of selections of good seeds:
* it was generated and rendered above of 1000 random pictures of plants
* after that, I chose ~50 the best seeds
* after that, there are 6 stages of artificial selection of the best seeds
* now, there is around 100 good seed 
...
A percent of good-looking plants now is bigger than before using genetics,
so this is usable enough technique.

# Rendering
One of the most important parts of rendering is color.
With proper their combinations it's easy to create realistic structure.
* The render uses a lot of normal distributions for computing properies, probably, 
* Settings for drawing saved in .json format.

# Conclusion
My program can draw nature-like plants with an interesting algorithms.
This technique could be used with other for generation fractal structures.
