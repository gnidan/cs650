function a = WG(n, g)
a = zeros(n-1, 1);
for i = 0:n-2,
  a(i+1) = W(n, mod(g^i, n));
end
