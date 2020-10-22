classdef section 
    properties
        s_label
        s_beg 
        s_end
        s_size 
        s_line
    end
    methods
        function obj = section(lab,b,e,l)
            obj.s_label = lab;
            obj.s_beg = b;
            obj.s_end = e;
            obj.s_size = e - b + 1 ;
            obj.s_line = l;
        end
    end
end        