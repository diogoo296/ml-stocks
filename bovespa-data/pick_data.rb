#!/usr/bin/env ruby
require 'csv'

folder = ARGV[0]
out = {}
total = 0

Dir["#{folder}/*.saida.csv"].map do |file|
  puts "Picking file #{file}..."
  CSV.foreach(file, headers: true) do |row|
    total += 1
    # row[-1] = row[-1] == '0.0' ? 0 : 1

    row.map do |r|
      r[1] = r[1].to_f.round(3) if !r[1].nil? && r[0] != 'Class'

      if out.has_key?(r[0])
        out[r[0]].push(r[1])
      else
        out[r[0]] = [r[1]]
      end

      if (r[1].nil? || out[r[0]].size != total) &&
      # if (r[1].nil? || out[r[0]].size != total || r[1] == 0) &&
          r[0] != 'Class'
        out.delete(r[0]) 
      end
    end
  end

=begin
  # shift row class
  out['Class'].drop(1)
  out.each_pair do |key, values|
    values.pop if key != 'Class'
  end
  total -= 1
=end
end

# Filter attributes with only zeros
out.each_pair do |key, values|
  out.delete(key) if key != 'Class' && !values.any?{ |v| v != 0 }
end

puts 'Writing output...'
CSV.open("BOVA.picked.csv", 'w') do |csv|
  csv << out.keys()
  for i in 0..(total - 1)
    row = []
    out.each_value{ |val| row.push(val[i]) }
    csv << row
  end
end
