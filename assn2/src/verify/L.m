function ans = L(n, k)
X = zeros(n);
m = n/k;
for i = 1:n,
  ii = i-1;
  j = floor(ii/m) + k * (mod(ii, m));
  X(i, j+1) = 1;
end
ans = X;
