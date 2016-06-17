module adder (in1,in2,out,c);
	input [15:0] in1,in2;
	output [15:0] out;
	output c;
	
	wire [16:0] ans;
	
	assign ans = in1 + in2;
	
	assign c = ans[16];
	assign out = ans [15:0];
	
endmodule
	