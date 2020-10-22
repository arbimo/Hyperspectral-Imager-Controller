classdef region
   properties
       label
       sections = {};
       size = 0;
   end
   methods
       function obj = region(l)
           obj.label=l;
       end
   end
end

