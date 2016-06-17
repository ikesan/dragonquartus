//#
module adder (in1,in2,out,S,V,Z,C);
	input signed  [15:0] in1,in2;
	output signed [15:0] out;
	output S,Z,C,V;
	
	wire signed [16:0] ans;	
	assign ans = in1 + in2;
	assign out = ans [15:0];
	assign S = ans[15];
	assign Z = !(|ans);
	assign C = ans[16];
	assign V = C;
	
endmodule
	
//#
module subber (in1,in2,out,S,V,Z,C);
	input signed  [15:0] in1,in2;
	output signed [15:0] out;
	output S,Z,C,V;
	
	wire signed [16:0] ans;	
	assign ans = in1 - in2;
	
	assign out = ans [15:0];
	assign S = ans[15];
	assign Z = !(|ans);
	assign C = ans[16];
	assign V = C;
	
endmodule
	
//#	
module ALUAnder (in1,in2,out,S,V,Z,C);
	input  [15:0] in1,in2;
	output  [15:0] out;
	output S,Z,C,V;
	
	wire [16:0] ans;	
	assign ans = in1 & in2;
	
	assign out = ans [15:0];
	assign S = ans[15];
	assign Z = !(|ans);
	assign C = 0;
	assign V = 0;
	
endmodule

//#	
module ALUOrer (in1,in2,out,S,V,Z,C);
	input  [15:0] in1,in2;
	output  [15:0] out;
	output S,Z,C,V;
	
	wire [16:0] ans;	
	assign ans = in1 | in2;
	
	assign out = ans [15:0];
	assign S = ans[15];
	assign Z = !(|ans);
	assign C = 0;
	assign V = 0;
	
endmodule
	
//#
module ALUXOrer (in1,in2,out,S,V,Z,C);
	input  [15:0] in1,in2;
	output  [15:0] out;
	output S,Z,C,V;
	
	wire [16:0] ans;	
	assign ans = in1 ^ in2;
	
	assign out = ans [15:0];
	assign S = ans[15];
	assign Z = !(|ans);
	assign C = 0;
	assign V = 0;
	
endmodule

module ALUSLL (in,d,out,S,V,Z,C);
//fill 0 :: not yet C
	input [15:0] in;
	input [3:0] d;
	output  [15:0] out;
	output S,Z,C,V;
	wire [15:0] ans;	
	assign ans = in << d;
	
	assign out = ans [15:0];
	assign S = ans[15];
	assign Z = !(|ans);
	assign C = 0;
	assign V = 0; //always 0
	
	
endmodule

module ALUSLR (in,d,out,S,V,Z,C);
//rotate
	input [15:0] in;
	input [3:0] d;
	output  [15:0] out;
	output S,Z,C,V;
	wire [15:0] ans;	
	assign ans = in <<< d;
	
	assign out = ans [15:0];
	assign S = ans[15];
	assign Z = !(|ans);
	assign C = 0;
	assign V = 0; //always 0
endmodule

//#
module ALUSRL (in,d,out,S,V,Z,C);
//rotate :: OK 
	input [15:0] in;
	input [3:0] d;
	output  [15:0] out;
	output S,Z,C,V;
	wire [15:0] ans;	
	assign ans = in >> d;
	
	assign out = ans [15:0];
	assign S = ans[15];
	assign Z = !(|ans);
	assign C = 0;
	assign V = 0; //always 0
endmodule

module ALUSRA (in,d,out,S,V,Z,C);
//arithmetic not yet C
	input signed [15:0] in;
	input [3:0] d;
	output signed   [15:0] out;
	output S,Z,C,V;
	wire [15:0] ans;	
	assign ans = in >>> d;
	
	assign out = ans [15:0];
	assign S = ans[15];
	assign Z = !(|ans);
	assign C = 0;
	assign V = 0; //always 0
endmodule