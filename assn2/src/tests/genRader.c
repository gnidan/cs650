#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define BUF_SIZE 2048

void makeW (unsigned int n, unsigned int g1, char *W)
{
  unsigned int i, g;
  char s[10];
  memset (s, 0, 10);
  memset (W, 0, BUF_SIZE);

  strcat (W, "(permute 0");
  g = 1;
  for ( i = 1; i < n; ++i )
    {
      g = g * g1 % n;
      sprintf (s, " %u", g);
      strcat (W, s);
    }
  strcat (W, ")");  
}

void makeWp (unsigned int n, unsigned int g2, char *WP)
{
  unsigned int i, g;
  char s[10];
  memset (s, 0, 10);
  memset (WP, 0, BUF_SIZE);
  
  strcat (WP, "(permute 0");
  g = 1;
  for ( i = 1; i < n; ++i )
    {
      g = g * g2 % n;
      sprintf (s, " %u", g);
      strcat (WP, s);
    }
  strcat (WP, ")");  
}

void makeD (unsigned int n, unsigned int g2, char *D)
{
  char s[BUF_SIZE];
  unsigned int i, g;
  memset (s, 0, BUF_SIZE);
  memset (D, 0, BUF_SIZE);
  strcat (D, "(diagonal");
  g = 1;
  for ( i = 1; i < n - 1; ++i )
    {
      g = g * g2 % n;
      sprintf (s, " WS(%u, %u)", n, g);
      strcat (D, s);
    }
  strcat (D, ")");
}

void makeE (unsigned int n, char *D, char *E)
{
  memset (E, 0, BUF_SIZE);
  sprintf (E, 
	   "(direct_sum (matrix (1 1) (1 WS(%u, 1)) %s))", n, D);
}


/**
 * @brief Stupid function to determine if the given integer is prime.
 *
 * @param n The integer to test for primality.
 *
 * @return 1 if n is prime, 0 otherwise.
 */
unsigned int isprime (unsigned int n)
{
  switch (n)
    {
    case 2:
    case 3:
    case 5:
    case 7:
    case 11:
    case 13:
    case 17:
    case 19:
    case 23:
    case 29:
    case 31:
    case 37:
    case 41:
    case 43:
    case 47:
    case 53:
    case 59:
    case 61:
      return 1;      
    }
  return 0;
}

/**
 * @brief Find two generators for the cyclic multiplicative group 
 *        {1, ..., n -1 }.
 *
 * @param n   The modulus with which we're working.
 * @param g1  The "first" generator.
 * @param g2  The "second" generator.
 */
void FindGenerators (unsigned int n, unsigned int *g1, unsigned int *g2)
{
  unsigned int *perm, i, j, k;

  perm = (unsigned int *) calloc (n - 1, sizeof (unsigned int));

  for ( i = 2; i < n; ++i )
    {
      /* generate the permutation */
      perm[0] = i;
      for ( j = 1; j < n - 1; ++j )
	perm[j] = perm[j - 1] * i % n;
      
      /* check if all values are present */
      for ( k = 1; k < n; ++k )
	{
	  for ( j = 0; j < n - 1; ++j )
	    if ( perm[j] == k )
	      break;
	  if ( j >= n - 1 )
	    break;
	}
      if ( k >= n )
	{
	  *g1 = i;
	  break;
	}
    }
  
  /* found g1, now find g2, which is the multiplicative inverse of g1 ---
     I guess I'll just be naive. */
  for ( i = 2; i < n; ++i )
    if ( *g1 * i % n == 1 )
      {
	*g2 = i;
	break;
      }
  
  free (perm);
}


int main (int argc, char *argv[])
{
  unsigned int n, g1, g2;
  char W[BUF_SIZE], Wp[BUF_SIZE], D[BUF_SIZE], E[BUF_SIZE];
  
  if ( argc != 2 )
    {
      fprintf (stderr, "%s <n>\n", argv[0]);
      fprintf (stderr, "\tgenerate SPL for Rader's Algorithm on vector's\n");
      fprintf (stderr, "\tof length n, where n is prime.\n");
      exit (1);
    }

  /* make sure that "n" is prime */
  sscanf (argv[1], "%u", &n);
  if (!isprime (n))
    {
      fprintf (stderr, "%u is not a prime number ... ABORT!\n", n);
      exit (1);
    }
  
  /* find generator(s) */
  FindGenerators (n, &g1, &g2);

  makeW  (n, g1, W);
  makeWp (n, g2, Wp);
  makeD  (n, g2, D);
  makeE  (n, D, E);
  
  printf ("(compose %s\n", Wp); 
  printf ("         (direct_sum (matrix (1)) (conj_trans F%u))\n", n-1);
  printf ("         %s\n", E);
  printf ("         (direct_sum (matrix (1)) F%u)\n", n - 1);
  printf ("         %s)\n", W);
  
  return 0;  
}
