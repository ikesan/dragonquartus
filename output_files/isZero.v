module isZero (in,out);
	input [15:0] in;
	output out;
	assign out = !( |in);   	
endmodule
