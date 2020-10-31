import julia
julia.install()
list = [3,6,8,1,4,6,8,2,5,0]

j = julia.Julia()
j.include('julia/sort.jl')
j.eval('find_even(list) = filter(iseven, list)')

print(j.sort_list(list))
print(j.add_to_list(10,list))
print(j.find_even(list))

