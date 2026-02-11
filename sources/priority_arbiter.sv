// Priority arbiter
// port[0] - highest priority

`timescale 1us/1us

module priority_arbiter #(
  parameter NUM_PORTS = 4
)(
    input  logic [NUM_PORTS-1:0] req_i,
    output logic [NUM_PORTS-1:0] gnt_o   // One-hot grant signal
);

//insert the logic here

endmodule