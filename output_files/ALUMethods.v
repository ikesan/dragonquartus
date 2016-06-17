module adder (in1,in2,out,S,V,Z,C);
	input signed  [15:0] in1,in2;
	output signed [15:0] out;
	output S,Z,C,V;
	
	wire signed [16:0] ans;	
	assign ans = in1 + in2;
	
	assign out = ans [15:0];
	assign S = ans[15];
	assign Z = isZero(ans);
	assign C = ans[16];
	assign V = C;
	
endmodule
	
	
module subber (in1,in2,out,S,V,Z,C);
	input signed  [15:0] in1,in2;
	output signed [15:0] out;
	output S,Z,C,V;
	
	wire signed [16:0] ans;	
	assign ans = in1 - in2;
	
	assign out = ans [15:0];
	assign S = ans[15];
	assign Z = isZero(ans);
	assign C = ans[16];
	assign V = C;
	
endmodule
	
	
module ALUAnder (in1,in2,out,S,V,Z,C);
	input  [15:0] in1,in2;
	output  [15:0] out;
	output S,Z,C,V;
	
	wire [16:0] ans;	
	assign ans = in1 & in2;
	
	assign out = ans [15:0];
	assign S = ans[15];
	assign Z = isZero(ans);
	assign C = 0;
	assign V = 0;
	
endmodule
	
module ALUOrer (in1,in2,out,S,V,Z,C);
	input  [15:0] in1,in2;
	output  [15:0] out;
	output S,Z,C,V;
	
	wire [16:0] ans;	
	assign ans = in1 | in2;
	
	assign out = ans [15:0];
	assign S = ans[15];
	assign Z = isZero(ans);
	assign C = 0;
	assign V = 0;
	
endmodule
	
module ALUSLA (in1,in2,out,S,V,Z,C);

end module
	