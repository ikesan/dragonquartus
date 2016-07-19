module BCmd (cond,S,V,Z,C,out);
  input [2:0] cond;
  input S,Z,C,V;
  output out;
  function select;
    input [2:0] cond;
    input S,Z,C,V;
    case (cond)
	 3'b000 : select = Z;
	 3'b001 : select =  V ;
	 3'b010 : select = Z || V;
	 3'b011 : select = !Z;
	 default: select = 0;
	 endcase
  endfunction
  assign out = select(cond,S,Z,C,V);
endmodule