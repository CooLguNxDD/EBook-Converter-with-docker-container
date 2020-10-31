import julia
from julia import *
list = [3,6,8,1,4,6,8,2,5,0]

j = julia.Julia()
j.include('julia/sort.jl')

print(j.sort_list(list))
print(j.add_to_list(10,list))

