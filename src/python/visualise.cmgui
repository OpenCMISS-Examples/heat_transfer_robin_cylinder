$root = "expected-results";
$dt = 10;           # frequency
$stop = 10          # stop time
$numProcs = 4;
$in = 0
$Region = 'DiffusionRegion'

# Reading the exnodes
# ===================
for ($i=0;$i<20;$i=$i+$dt) 
#Read in the sequence of nodal positions.
  {  
     for ($j=0; $j < $numProcs; $j=$j+1)
        {
           $filename = sprintf("$root/MainTime_%01d.part%01d.exnode", $i, $j);
           $time = $i
           print "Reading $filename time $time\n";
           gfx read node "$filename" time $i;
        }
  }

#Read in the element description
# Reading the exnodes
# ===================
for ($j=0; $j < $numProcs; $j=$j+1)
   {
       gfx read element $root/MainTime_0.part$j.exelem;
   }

gfx define faces egroup $Region
gfx modify spectrum default clear overwrite_colour
gfx modify spectrum default linear reverse range 34.0 37.0 extend_above extend_below rainbow colour_range 0 1 component 1


gfx modify g_element $Region surfaces select_on material default data U spectrum default selected_material default_selected render_shaded

gfx draw axes
gfx edit scene
gfx create window 1

#gfx modify window 1 background colour 255 255 255

gfx cre mat copper ambient 1 0.2 0 diffuse 0.6 0.3 0 specular 0.7 0.7 0.5 shininess 0.3;
gfx create colour_bar label_material white spectrum default material copper;
gfx modify g_element "/" point glyph colour_bar general size "1*1*1" centre 0,0,0 select_on material copper selected_material copper normalised_window_fit_left;
gfx timekeeper default set 10.0
