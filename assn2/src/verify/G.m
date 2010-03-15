function a = G(n, g)
a = zeros(1,n);
a(1) = 1;
for i=0:n-2,
  a(i+2) = mod(g^i, n)+1;
end
