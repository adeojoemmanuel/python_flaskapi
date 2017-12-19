def recur_fibo(n):
   if n <= 1:
       return n
   else:
       return(recur_fibo(n-1) + recur_fibo(n-2))

#nterms = 100
nterms = int(raw_input("input value : "))
OCC = 1

if nterms <= 0:
   print("Plese enter a positive integer")
else:
   print("Fibonacci sequence:")
   for i in range(nterms):
       #print(recur_fibo(i))
       idt = occ
       print("Case #{}: {}".format(OCC, recur_fibo(i)))
