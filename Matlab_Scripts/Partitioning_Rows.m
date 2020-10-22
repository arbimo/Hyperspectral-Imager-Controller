function[I_beg,I_end]= Partitioning_Rows(row) 

%We consider each colored pixel P of a row in the image. We look at pixels
%located just before and after P to determine the beginning and the end of
%a section on the line. With this method, sections can be distinguished
%thanks to the 'color' of 2 succeeding pixels and not just the edges
%anymore : we can create a new section even without a clear edge between 2
%regions.

I_beg=[];
I_end=[];

L_row=length(row);

if row(1) ~= 0
    indice_beginning = 1;
    I_beg = [I_beg indice_beginning];
    if row(2) ~= row(1)
        indice_end = 1;
        I_end = [I_end indice_end];
    end  
end    


for i=2:L_row-1
    if row(i) ~= 0
        if row(i-1) == 0
            indice_beginning = i;
            I_beg = [I_beg indice_beginning];
        end
        
        if row(i+1) == 0 
            indice_end = i;
            I_end = [I_end indice_end];
        else 
            if row(i+1) ~= row(i)
                indice_end = i;
                I_end = [I_end indice_end];
                indice_beginning = i+1;
                I_beg = [I_beg indice_beginning];
            end
        end
    end    
end

if row(L_row) ~= 0
    if row(L_row) == row(L_row-1)
        I_end = [I_end L_row];
    else 
        I_end = [I_end L_row];
        I_beg = [I_beg L_row];
    end
end
end