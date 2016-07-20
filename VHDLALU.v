
module slr(
		input [15:0] in,
		input [3:0] d,
		output [16:0] out);	
	 wire [15:0] tmp [3:1];	
	 assign tmp[3] = d[3] ?{in[ 7:0],in[15:8]} : in;
	 assign tmp[2] = d[2] ?{tmp[3][ 11:0],tmp[3][15:12]} : tmp[3];
	 assign tmp[1] = d[1] ?{tmp[2][ 13:0],tmp[2][15:14]} : tmp[2];
	 assign out = {1'b0, d[0] ? {tmp[1][ 14:0],tmp[1][15]} : tmp[1]};
endmodule

module VHDLALU (AR,BR,d,opselect,isValid,inputFlag,outputFlag,iRdWriteFlag,SZCVWriteFlag,HaltFlag,S,Z,C,V,Out);
  input signed [15:0] AR,BR;
  input signed [3:0] d;
  input [3:0] opselect;
  
  input isValid;
  output inputFlag,outputFlag,iRdWriteFlag,SZCVWriteFlag,HaltFlag,S,Z,C,V;
  output signed [15:0] Out;
  wire signed [17:0] wOp;
  wire [16:0] sllWire,slrWire,srlWire,sraWire;
  wire signed [16:0]  addWire ,subWire;
  assign addWire = AR + BR; 
  assign subWire = BR - AR;
  slr slr0(BR,d,slrWire);
  assign wOp = 
	    opselect == 4'b0000 ? {addWire[16],addWire[16:0]} :
		 opselect == 4'b0001 ? {subWire[16],subWire[16:0]}://
		 opselect == 4'b0010 ? {2'b00,AR & BR}://
		 opselect == 4'b0011 ? {2'b00,AR | BR}://
		 opselect == 4'b0100 ? {2'b00,AR ^ BR}://
		 opselect == 4'b0101 ? {subWire[16],subWire[16:0]}://
		 opselect == 4'b0110 ? {2'b00,AR}://
		 opselect == 4'b1000 ? BR << d: //sll
		 opselect == 4'b1001 ? {1'b0,slrWire}: //slr
		 opselect == 4'b1010 ? BR >> d: //srl
		 opselect == 4'b1011 ? BR >>> d: //sra
		 18'b00_0000_0000_0000_0000; //
  assign inputFlag  = (opselect == 4'b1100) & isValid;
  assign outputFlag = (opselect == 4'b1101) & isValid;
  assign HaltFlag   = (opselect == 4'b1111) & isValid;
  assign SZCVWriteFlag = (opselect != 4'b1111 & opselect != 4'b1101) & isValid;
  assign iRdWriteFlag =  (opselect != 4'b1111 & opselect != 4'b1101 & opselect != 4'b0101) & isValid;
  assign Out = wOp[15:0] & (isValid ? 16'hffff:16'h0000);
  assign S = wOp[15] & isValid;
  assign Z = (wOp[15:0] == 16'h0000)& isValid;
  assign C = wOp[16] & isValid;
  assign V = wOp[17] & isValid;
  
endmodule