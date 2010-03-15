function ans = permutation(A)
n = size(A,2);
ans = zeros(size(A));
for i = 1:n,
  ans(i,A(i)) = 1;
end
