function ans = L(n, k)
X = zeros(n);
m = n/k;
for i = 1:n,
  for j = 1:n,
    X(i, j) = j == 1 + k*(i-1) - (k*m-1)*floor((i-1)/m);
  end
end
ans = X;
