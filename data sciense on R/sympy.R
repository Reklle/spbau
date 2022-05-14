# install.packages("caracas")
library(caracas)
#caracas::install_sympy()


#########################
#         Note          #
#########################
#  der(f)  --   derivative
#  der(f, c(x, y))
#  subs    --   substitution
#  eval    --   evaluate
#  solve_sys(eq, x)
#  taylor(f, x0 = 0, n = 4+1)

x <- symbol('x')
eq <- 2*x^2 - x
eq <- der(eq, x)
tex(eq)

y <- 10
subs(eq, x, y)
