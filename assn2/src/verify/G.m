function a = G(n, g)
a = zeros(n);
a(1,1) = 1;
for i=0:n-2,
  a(i+2, mod(g^i, n)+1) = 1;
end
