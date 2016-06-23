//# out[S,V,Z,C,15:0] -> [19:0]
module ALUinSVZC (in,S,V,Z,C,out);
  input [15:0] in;
  input S,Z,C,V;
  output [19:0] out;
  assign out[15:0] = in[15:0];
  assign out[16] = S;
  assign out[17] = V;
  assign out[18] = Z;
  assign out[19] = C;
endmodule

module ALUoutSVZC (in,S,V,Z,C,out);
  input [19:0] in;
  output S,Z,C,V;
  output [15:0] out;
  assign out[15:0] = in[15:0];
  assign S = in[16];
  assign V = in[17];
  assign Z = in[18];
  assign C = in[19];
endmodule

module ALUAdd (in1,in2,out,S,V,Z,C);
	input signed  [15:0] in1,in2;
	output signed [19:0] out;
	output S,Z,C,V;
	
	wire signed [16:0] ans;	
	assign ans = in1 + in2;
	assign out = ans [15:0];
	assign S = ans[15];
	assign Z = !(|ans);
	assign C = ans[16];
	assign V = C;
	
endmodule
	
module ALUNothing (in1,in2,out,S,V,Z,C);
	input signed  [15:0] in1,in2;
	output signed [19:0] out;
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
module ALUSub (in1,in2,out,S,V,Z,C);
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
module ALUMov (in,out,S,V,Z,C);
	input   [15:0] in;
	output  [15:0] out;
	output S,Z,C,V;
	
	wire  [15:0] ans;	
	assign ans = in;
	
	assign out = ans [15:0];
	assign S = ans[15];
	assign Z = !(|ans);
	assign C = 0;
	assign V = C;
	
endmodule
	
//#	
module ALUAnd (in1,in2,out,S,V,Z,C);
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
module ALUOr (in1,in2,out,S,V,Z,C);
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
module ALUXOr (in1,in2,out,S,V,Z,C);
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
//fill 0 ::
	input [15:0] in;
	input [3:0] d;
	output  [15:0] out;
	output S,Z,C,V;
	wire [16:0] ans;	
	
	wire [16:0] tmp [3:1];	
	assign tmp[3] = d[3] ?{in[8:0],8'b0} :{1'b0,in[15:0]};
	assign tmp[2] = d[2] ?{tmp[3][12:0],4'b0} : tmp[3];
	assign tmp[1] = d[1] ?{tmp[2][14:0],2'b0} : tmp[2];
	assign ans    = d[0] ?{tmp[1][15:0],1'b0} : tmp[1];
	
	
	assign out = ans [15:0];
	assign S = ans[15];
	assign Z = !(|ans);
	assign C = ans[16];
	assign V = 0; //always 0
	
	
endmodule

module ALUSLR (in,d,out,S,V,Z,C);
//rotate
	input [15:0] in;
	input [3:0] d;
	output  [15:0] out;
	output S,Z,C,V;
	wire [15:0] ans;	
	
	wire [15:0] tmp [3:1];	
	assign tmp[3] = d[3] ?{in[ 7:0],in[15:8]} : in;
	assign tmp[2] = d[2] ?{tmp[3][ 11:0],tmp[3][15:12]} : tmp[3];
	assign tmp[1] = d[1] ?{tmp[2][ 13:0],tmp[2][15:14]} : tmp[2];
	assign ans    = d[0] ?{tmp[1][ 14:0],tmp[1][15]} : tmp[1];
	
	assign out = ans [15:0];
	assign S = ans[15];
	assign Z = !(|ans);
	assign C = 0; //always 0
	assign V = 0; //always 0
endmodule

//#
module ALUSRL (in,d,out,S,V,Z,C);

	input [15:0] in;
	input [3:0] d;
	output  [15:0] out;
	output S,Z,C,V;
	wire [16:0] ans;
	
	wire [16:0] tmp [3:1];	
	assign tmp[3] = d[3] ?{8'b0,in[15:7]} :{in[15:0],1'b0};
	assign tmp[2] = d[2] ?{4'b0,tmp[3][15:3]} : tmp[3];
	assign tmp[1] = d[1] ?{2'b0,tmp[2][15:1]} : tmp[2];
	assign ans    = d[0] ?{1'b0,tmp[1][15:0]} : tmp[1];
	
	
	assign out[15:0] = ans [16:1];
	assign S = ans[15];
	assign Z = !(|ans);
	assign C = ans[0];
	assign V = 0; //always 0
endmodule

module ALUSRA (in,d,out,S,V,Z,C);
//arithmetic not yet C
	input [15:0] in;
	input [3:0] d;
	output [15:0] out;
	output S,Z,C,V;
	wire [16:0] ans;
	wire sign ;	
	wire [16:0] tmp [3:1];
	
	assign sign = in[15];
	assign tmp[3] = d[3] ?{(sign ? 8'b1:8'b0),in[15:7]} :{in[15:0],1'b0};
	assign tmp[2] = d[2] ?{(sign ? 4'b1:4'b0),tmp[3][15:3]} : tmp[3];
	assign tmp[1] = d[1] ?{(sign ? 2'b1:2'b0),tmp[2][15:1]} : tmp[2];
	assign ans    = d[0] ?{(sign ? 1'b1:1'b0),tmp[1][15:0]} : tmp[1];
	
	
	assign out[15:0] = ans [16:1];
	assign S = ans[15];
	assign Z = !(|ans);
	assign C = ans[0];
	assign V = 0; //always 0
endmodule