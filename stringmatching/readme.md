### Used sourses:
* https://numpy.org
* https://www.ncbi.nlm.nih.gov
* https://cyberleninka.ru/article/n/algoritmy-poiska-v-zadachah-analiza-nukleotidnyh-posledovatelnostey-s-tselyu-odnoznachnoy-identifikatsii-genomov/viewer
* https://chromium.googlesource.com/v8/v8.git/+/d123f30b6df5507b2acda8e85ad63e05de8ca8a7/src/string-search.h
* https://en.wikipedia.org/wiki/Fowler%E2%80%93Noll%E2%80%93Vo_hash_function


### How to use:
1. Install proper version of **CUDA** (optional)
2. Install **cupy** for the current CUDA version (optional)


### Results:
* Numpy and cupy probably is bad solution for fast search in text.
* GPU calculations are faster than CPU calculations not at all cases.
* I write a couple original (but not very effective) algorithms for GPU-optimized search
  * ACTGMathing.rk 
  * ACTGMathing.mrk


### Fails:
* Hight-perfomance rolling hash (was deleted by reason of low perfomance)
* Boyer-Moore-Horspool string-searching algorithm haven't realized
* Numpy and cupy aren't good solutions for this type of problems.
* ACTGMathing.rk doesn't work with cuda
* ACTGMathing.mrk works extreamly bad

Actually, it was an experiment. It was kind of a failure, but it was interesting to solve problems with that code.
