# plots.rb

require 'rubygems'
require 'Tioga/FigureMaker'
require 'plot_styles.rb'

class MyPlots
  include Math
  include Tioga
  include FigureConstants
  include MyPlotStyles
  
  def t
    @figure_maker
  end

  def initialize
    @figure_maker = FigureMaker.default

    t.def_eval_function { |str| eval(str) }
    t.save_dir = 'generated'
    @opacity_data = nil
    
    @image_right_margin = 0.07
    @margin = 0.3
    tmp = File.new('matlab_data_full.sv')
    @table1_headers = tmp.readline.chomp.split(",")
    #print @table1_headers 
    #print "\n"
    @table1_length = 0
    tmp.each {|x| @table1_length = @table1_length + 1; }
    tmp.close
    tmp = File.new('cellml_data_full.sv')
    @table2_headers = tmp.readline.chomp.split(",")
    #print @table2_headers
    #print "\n"
    @table2_length = 0
    tmp.each {|x| @table2_length = @table2_length + 1; }
    tmp.close
    @table1 = Dtable.new(@table1_headers.length, @table1_length) #matlab
    @table1.read('matlab_data_full.sv', 1)
    @table2 = Dtable.new(@table2_headers.length, @table2_length) #cellml
    @table2.read('cellml_data_full.sv', 1)
    @names_to_compare = {
      'y' => 'y', 'w' => 'w', 'x' => 'x', 'z' => 'z', 'v' => 'v', 'Cai' => 'Ca_i', 'Nai' => 'Na_i', 'Vm' => 'V_m', 'time' => 'time',
      #'PKACI' => 'PKAC_I', 
      #'PKACII' => 'PKAC_II',
      'cAMPtot' => 'cAMP_tot', 'm' => 'm'
    }
    @names_to_compare.each {|matlab, cellml|
      t.def_figure(matlab + ' vs ' + cellml) { compare_plot(matlab, cellml, @table1, @table2) }
    }
  end
  def compare_plot(name, n_t_c, d1, d2)
    #t.landscape
    t.do_box_labels("Comparison view", 'Time', nil)
    #t.subplot { t.yaxis_loc = t.ylabel_side = LEFT;
    #    t.right_edge_type = AXIS_HIDDEN; 
    #print @table1_headers.index(name)
    #print "\n"
    #print @table2_headers.index(n_t_c)
    #print "\n"
    part_plot(d1.column(@table1_headers.index(name)), d1.column(@table1_headers.index('time')), name, d2.column(@table2_headers.index(n_t_c)), d2.column(@table2_headers.index('time')), n_t_c) # }
  end
  def part_plot(ys1, xs1, name1, ys2, xs2, name2)
    t.do_box_labels(name1, 'time', '\textcolor{Black}{Values}')
    t.show_plot_with_legend('legend_scale' => 1.3) {
      t.show_plot('boundaries' => plot_boundaries(xs1,ys1,xs2,ys2,@margin)) {
        t.line_width = t.line_width + 3
        t.show_polyline(xs2, ys2, Blue, "CellML: " + name2)
        t.line_width = t.line_width - 3
        t.show_polyline(xs1, ys1, Red, "Matlab: " + name1);
      }
    }
    
  end
    def plot_boundaries(xs1,ys1,xs2,ys2,margin,ymin=nil,ymax=nil,reverse_xaxis=false,reverse_yaxis=false)
        xmin = (xs1.min < xs2.min)? xs1.min: xs2.min
        xmax = (xs1.max > xs2.max)? xs1.max: xs2.max
        ymin = ((ys1.min < ys2.min)? ys1.min: ys2.min) if ymin == nil
        ymax = ((ys1.max > ys2.max)? ys1.max: ys2.max) if ymax == nil
        width = (xmax != xmin)? 1 : xmax - xmin
        height = (ymax != ymin)? 1 : ymax - ymin
        left_boundary = xmin - margin * width
        right_boundary = xmax + margin * width
        top_boundary = ymax + margin * height
        bottom_boundary = ymin - margin * height
        if reverse_xaxis
           tmp = left_boundary; left_boundary = right_boundary; right_boundary = tmp
        end
        if reverse_yaxis
           tmp = top_boundary; top_boundary = bottom_boundary; bottom_boundary = tmp
        end
        return [ left_boundary, right_boundary, top_boundary, bottom_boundary ]
    end
    

end

MyPlots.new
