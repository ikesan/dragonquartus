
module VHDL_LI_B (
    input [15:0] PC,
	 input signed [15:0] Rb,
	 input signed [7:0] d,
	 input [2:0] opin2,
	 input isValid,
	 output [15:0] out,
	 output S,V,Z,C,SVZCWriteFlag,IRdWriteFlag,is_10111,is_10100
    );
	 wire [17:0] vcWire;
	 wire signed [15:0] d16;
	 wire [16:0] wout;
	 assign d16 = {(d[7]?8'hff:8'h00),d};
	 assign is_10111 = isValid & (opin2 == 3'b111);
	 assign is_10100 = isValid & (opin2 == 3'b100);
    assign SVZCWriteFlag = isValid & (opin2 != 3'b111) & (opin2 != 3'b100);
	 assign IRdWriteFlag = isValid & ((opin2 == 3'b000) | (opin2 == 3'b001)| (opin2 == 3'b010));
	 assign wout = 
	   opin2 == 3'b000 ? d16 : //Li
	   opin2 == 3'b001 ? Rb + d16 : //Addi
	   opin2 == 3'b010 ? Rb - d16 : //Subi
	   opin2 == 3'b011 ? Rb - d16 : //Cmpi
		PC + 16'h0001 + d16 ; //PC
	assign out = isValid ? wout[15:0]:16'h0000;
	assign Z = isValid & (out==16'h0000);
	assign C = isValid & wout[16];
	assign V = isValid & wout[16];
	assign S = isValid & wout[15];
endmodule