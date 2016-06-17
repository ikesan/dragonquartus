module isZero (in,out);
	input signed [15:0] in;
	output out;
	
	wire [16:0] ans;	
	assign ans = in;
	assign out =!( ans[15] | ans[14] | ans[13] | ans[12] 
				| ans[11] | ans[10] | ans[9] | ans[8] 
				| ans[7] | ans[6] | ans[5] | ans[4] 
				| ans[3] | ans[2] | ans[1] | ans[0]);   	
endmodule
