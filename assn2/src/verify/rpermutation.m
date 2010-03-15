function ans = rpermutation(A)
n = size(A,2);
ans = zeros(size(A));
for i = 1:n,
  ans(A(i),i) = 1;
end
