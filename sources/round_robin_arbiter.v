// Use mask to identify the last grant
// Round robin arbiter

`timescale 1us/1us

module round_robin_arbiter (
  input     wire          clk  ,
  input     wire          rst_n,

  input     wire   [3:0]  req_i,
  output    wire   [3:0]  gnt_o
);

  reg [3:0] mask_q;
  wire [3:0] nxt_mask;

  always@(posedge clk or negedge rst_n)
    if (!rst_n)
      mask_q <= 4'hF;
    else
      mask_q <= nxt_mask;

  // Next mask based on the current grant
  assign nxt_mask = gnt_o[0] ?  4'b1110 : gnt_o[1] ? 4'b1100 : gnt_o[2] ? 4'b1000 :gnt_o[3] ? 4'b0000 : mask_q ;


  // Generate the masked requests
  wire [3:0] mask_req;

  assign mask_req = req_i & mask_q;

  wire [3:0] mask_gnt;
  wire [3:0] raw_gnt;
  // Generate grants for req and masked req
  priority_arbiter #(4) maskedGnt (.req_i (mask_req), .gnt_o (mask_gnt));
  priority_arbiter #(4) rawGnt    (.req_i (req_i),    .gnt_o (raw_gnt));

  // Final grant based on mask req
  assign gnt_o = |mask_req ? mask_gnt : raw_gnt;

endmodule
