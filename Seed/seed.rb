#!/usr/bin/env ruby

# This seems to give matching seed results on Ruby 2.5
# (Tested on 2.5.1p57), but not on 3 (ruby 3.0.2p107)

# The expected test is:
# srand(1<<32); rand
# >> 0.8444218515250481
# which is equivalent to the reference Python seed of 0

length, seed = ARGV[0..1]
seed = seed.to_i

# Adjust seeds to match Python3 reference seed.py results
if seed < 1<<32
  seed += 1<<32
elsif seed < 1<<33
  seed += 1<<64
end

puts seed
srand(seed)

chars = (' ' .. '~').to_a << "\n"
prog = (1..length.to_i).map {|i| chars[(rand * 96).to_i]}

puts "Your program:\n----------------------------------------\n", prog*"", "----------------------------------------\n"
