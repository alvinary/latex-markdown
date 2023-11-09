# Median algebras

A median algebra is a pair ~(A, M)~ where A is a nonempty set, M is
a ternary operation over A, and all the following hold:

 ~ for all x, y, z. M(x, y, z) = M(x, z, y) ~

 ~ for all x, y, z. M(x, y, z) = M(y, z, x) ~ 

 ~ for all x, y. M (x, x, y) = x ~

 ~ for all x, y, z, u, v. M (M (x, y, z), u, v)) = M (x, M (y, u, v); M (z, u, v)) ~

For instance, if we define ~M (x, y, z) = (x i y) s (x i z) s (y i z)~, 
for all ~x, y, z in M~, where ~s~ and ~i~ are from some lattice ~(L, s, i)~, then
~(L, M)~ is a median algebra.
