#!/usr/bin/ruby
#
# fix the timings format for feeding into a spreadsheet
# yay, graphs!
#
# PAPI_TOT_CYC
#  $3 avg
#  $4 min
#  $5 max
# PAPI_TOT_INS
#  $6 avg
#  $7 min
#  $8 max
# PAPI_FP_OPS
#  $9 avg
#  $10 min
#  $11 max
# PAPI_L1_DCM
#  $12 avg
#  $13 min
#  $14 max

events = [:PAPI_TOC_CYC, :PAPI_TOT_INS, :PAPI_FP_OPS, :PAPI_L1_DCM]
values = [:avg, :min, :max]
data = {}

while gets()
  $F = $_.split(' ')

  $function = $F[0]
  $k = $F[1].to_i

  event_no = 0
  value_no = 0
  2.upto $F.size-1 do |column|
    data[events[event_no]] = {} unless data.include? events[event_no]
    stat = values[value_no]
    event = data[events[event_no]]
    event[stat] = [] unless event.include? stat

    event[stat][$k] = {} unless event[stat][$k]
    event[stat][$k][$function] = $F[column]
    
    value_no += 1
    value_no %= 3
    event_no += 1 if value_no == 0
  end
end

data.each do |event_name, stats|
  stats.each do |stat_type, values|
    puts "Report for " + event_name.to_s + ", " + stat_type.to_s

    functions = []

    values[2].each do |column, value|
      functions << column unless functions.include? column
      print "\t" + column
    end
    puts

    1.upto values.size-1 do |k|
      print k.to_s
      functions.each do |function|
        if values[k][function]
          print "\t" + values[k][function]
        else
          print "\t" + values[k+1][function]
        end
      end
      puts
    end


    puts
  end
end

