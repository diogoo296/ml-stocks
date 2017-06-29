#!/usr/bin/env ruby
require 'csv'

input     = ARGV[0]
lastDay   = ARGV[1] 
lastStock = ARGV[2]
out = []

def writeOut stock, out
  CSV.open("daily-stocks/#{stock}.daily.csv", 'w', col_sep: ';') do |csv|
    out.map{ |r| csv << r }
  end
  out = []
end

CSV.foreach(input, headers: true) do |row|
  stock = row[0]
  today = row[-1][0..7]

  writeOut(lastStock, out) if stock != lastStock
  out.push row if today != lastDay

  lastDay   = today
  lastStock = stock
end

writeOut lastStock, out
