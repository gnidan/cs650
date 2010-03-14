function ans = T(n, k)
X = zeros(n);
for i = 1:n,
  X(i,i) = exp(-j*2*pi / n) ^ (floor((i-1)/k) * mod((i-1), k));
end
ans = X;
